import copy
import math
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import json
import shutil
import tempfile
from contextlib import contextmanager
import yaml
import numpy as np
import torch
from torch.nn import functional as F
TEAM=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(TEAM/"harness"))
from week2.model import KE2,codec,GQA,MoE,LanguageModel,SwiGLU
from week2.config import load,load_runtime,merge,validate
from train_week2 import apply_resolution

def fixture(head="untied_dense",mtp=False):
    c=merge(load_runtime(TEAM/"configs/arms/t1.yaml"),load(TEAM/"configs/small/smoke_resolution.yaml"))
    c["optim"]["lr"]=1e-3;m=c["model"]
    m.update(vocab_size=31,n_embd=16,n_layer=2,n_head=4,n_kv_head=2,block_size=8,head_mode=head,tie_embeddings=head=="projected_ke2_tied",mtp=mtp,mtp_weight=1.0 if mtp else 0.0,head_weight_chunk_size=8)
    m["moe"].update(num_experts=4,top_k=2,num_shared=1,ffn_hidden=24)
    rng=np.random.default_rng(7)
    rows=rng.integers(0,256,(31,4),dtype=np.uint8);lengths=rng.integers(1,5,31,dtype=np.int16)
    return c,rows,lengths

class CodecTests(unittest.TestCase):
    def setUp(self):torch.manual_seed(1234);self.c,self.rows,self.lengths=fixture()
    def test_sparse_projection_against_independent_f64_reference(self):
        layer=KE2(self.rows,self.lengths,16)
        ids=torch.arange(31);reference=[]
        for row,length in zip(self.rows,self.lengths):
            a=np.zeros(1024,dtype=np.float64)
            for p in range(int(length)):a[int(row[p])*4+p]=1/math.sqrt(int(length))
            a=(a-a.mean())/(a.std(ddof=1)+1e-6);reference.append(a)
        expected=torch.tensor(np.array(reference),dtype=torch.float32)@layer.projection.weight.t()
        actual=layer.projected(ids)
        torch.testing.assert_close(actual,expected,rtol=2e-5,atol=3e-6)
    def test_projection_gradients_match_dense(self):
        a=KE2(self.rows,self.lengths,16);b=copy.deepcopy(a);ids=torch.arange(31)
        weights=torch.randn(31,16)
        (a.projected(ids)*weights).sum().backward()
        dense=codec(torch.tensor(self.rows),torch.tensor(self.lengths))
        ((dense@b.projection.weight.t())*weights).sum().backward()
        torch.testing.assert_close(a.projection.weight.grad,b.projection.weight.grad,rtol=3e-5,atol=3e-5)
    def test_tied_head_has_no_independent_weight_and_refreshes(self):
        m=LanguageModel(self.c["model"]|{"head_mode":"projected_ke2_tied"},self.rows,self.lengths)
        self.assertIsNone(m.head)
        before=m.embedding.vocabulary_weight().detach().clone()
        with torch.no_grad():m.embedding.projection.weight.add_(torch.randn_like(m.embedding.projection.weight)*0.01)
        self.assertFalse(torch.equal(before,m.embedding.vocabulary_weight()))
    def test_checkpointed_tied_weight_gradient(self):
        layer=KE2(self.rows,self.lengths,16);layer.train()
        layer.vocabulary_weight(8).square().sum().backward()
        self.assertTrue(torch.isfinite(layer.projection.weight.grad).all())

class BackboneTests(unittest.TestCase):
    def setUp(self):torch.manual_seed(1234);self.c,self.rows,self.lengths=fixture()
    def test_attention_causality(self):
        a=GQA(self.c["model"]);x=torch.randn(2,8,16);y=x.clone();y[:,4:]+=100
        torch.testing.assert_close(a(x)[:,:4],a(y)[:,:4],rtol=0,atol=0)
    def test_rope_preserves_pair_norm(self):
        a=GQA(self.c["model"]);x=torch.randn(2,4,8,4)
        torch.testing.assert_close(a.rotary(x).square().sum(-1),x.square().sum(-1),rtol=2e-6,atol=2e-6)
    def test_gqa_matches_per_head_attention_reference(self):
        a=GQA(self.c["model"]);x=torch.randn(2,8,16)
        q=a.rotary(a.q(x).reshape(2,8,4,4).transpose(1,2))
        k=a.rotary(a.k(x).reshape(2,8,2,4).transpose(1,2))
        v=a.v(x).reshape(2,8,2,4).transpose(1,2)
        heads=[]
        for head in range(4):
            scores=q[:,head]@k[:,head//2].transpose(-2,-1)/2
            scores=scores.masked_fill(~torch.ones(8,8,dtype=torch.bool).tril(),float("-inf"))
            heads.append(scores.softmax(-1)@v[:,head//2])
        expected=a.o(torch.stack(heads,dim=2).reshape(2,8,16))
        torch.testing.assert_close(a(x),expected)
    def test_swiglu_branch_widths(self):
        s=SwiGLU(16,24)
        self.assertEqual(tuple(s.gate.weight.shape),(24,16));self.assertEqual(tuple(s.up.weight.shape),(24,16))
        self.assertEqual(tuple(s.down.weight.shape),(16,24));self.assertIsNone(s.up.bias)
    def test_dispatch_outputs_and_gradients_match_dense_reference(self):
        a=MoE(self.c["model"]);b=copy.deepcopy(a);x=torch.randn(2,8,16,requires_grad=True);y=x.detach().clone().requires_grad_()
        valid=torch.ones(2,8,dtype=torch.bool);valid[:,-2:]=False
        actual=a(x,valid)
        flat=y.reshape(-1,16);scores=b.router(flat).softmax(-1);weights,choice=scores.topk(2,dim=-1);weights=weights/weights.sum(-1,keepdim=True)
        ref=torch.zeros_like(flat)
        for i,e in enumerate(b.experts):ref=ref+e(flat)*((choice==i)*weights).sum(-1,keepdim=True)
        for e in b.shared:ref=ref+e(flat)
        ref=(ref*valid.reshape(-1,1)).reshape(2,8,16)
        torch.testing.assert_close(actual,ref,rtol=2e-5,atol=1e-6)
        actual.square().sum().backward();ref.square().sum().backward()
        torch.testing.assert_close(x.grad,y.grad,rtol=3e-5,atol=1e-6)
        for p,q in zip(a.parameters(),b.parameters()):
            if p.grad is not None:torch.testing.assert_close(p.grad,q.grad,rtol=3e-5,atol=2e-6)
    def test_forward_backward_repeatability_both_heads(self):
        for head in ["untied_dense","projected_ke2_tied"]:
            c,rows,lengths=fixture(head);traces=[]
            for _ in range(2):
                torch.manual_seed(1234);m=LanguageModel(c["model"],rows,lengths);opt=torch.optim.AdamW(m.parameters(),lr=1e-3)
                ids=torch.arange(16).reshape(2,8)%31;values=[]
                for _ in range(3):
                    opt.zero_grad();loss=F.cross_entropy(m(ids,torch.ones_like(ids,dtype=torch.bool)).reshape(-1,31),(ids+1).reshape(-1)%31)
                    loss.backward();opt.step();values.append(float(loss).hex())
                traces.append(values)
            self.assertEqual(*traces)
    def test_mtp_head_initialized_once(self):
        c,rows,lengths=fixture(head="projected_ke2_tied",mtp=True)
        linear=torch.nn.Linear
        with patch("week2.model.nn.Linear",side_effect=linear) as constructor:
            model=LanguageModel(c["model"],rows,lengths)
        calls=[call for call in constructor.call_args_list if call.args[:2]==(16,31)]
        self.assertEqual(len(calls),1,"MTP must not allocate/discard a duplicate head or consume extra RNG")
        self.assertIsNotNone(model.mtp_head)

    def test_mtp_is_explicit_and_gets_gradients(self):
        c,rows,lengths=fixture(mtp=True);m=LanguageModel(c["model"],rows,lengths)
        ids=torch.arange(8).reshape(1,8);n,t=m(ids,torch.ones_like(ids,dtype=torch.bool),return_mtp=True)
        (n.square().mean()+t.square().mean()).backward();self.assertIsNotNone(m.mtp_head.weight.grad)

@contextmanager
def copied_contract():
    with tempfile.TemporaryDirectory() as tmp:
        team=Path(tmp)/"teams/05-architecture"
        shutil.copytree(TEAM/"configs/arms",team/"configs/arms")
        (team/"configs/small").mkdir(parents=True,exist_ok=True)
        shutil.copy2(TEAM/"configs/runtime.yaml",team/"configs/runtime.yaml")
        shutil.copy2(TEAM/"configs/open_choices.json",team/"configs/open_choices.json")
        shutil.copy2(TEAM/"configs/small/smoke_resolution.yaml",team/"configs/small/smoke_resolution.yaml")
        (team/"experiments").mkdir()
        shutil.copy2(TEAM/"experiments/plan_v1.md",team/"experiments/plan_v1.md")
        yield team

class ConfigTests(unittest.TestCase):
    def resolved(self,path="t1.yaml",team=TEAM):
        c=load_runtime(team/"configs/arms"/path,team/"configs/runtime.yaml")
        c=merge(c,load(team/"configs/small/smoke_resolution.yaml"));c["optim"]["lr"]=1e-3
        return c
    def test_lead_pins_and_inactive_mtp_weight(self):
        c=load_runtime(TEAM/"configs/arms/t1.yaml")
        self.assertIs(c["model"]["reversible"],False)
        self.assertIs(c["model"]["mtp"],False)
        self.assertIsNone(c["model"]["mtp_weight"])
        self.assertEqual(c["model"]["moe"]["dispatch"],"loop")
        self.assertEqual(c["model"]["ce_impl"],"torch")
        self.assertEqual(c["optim"]["lr"],0.001)
        self.assertFalse(any("MTP" in e for e in validate(c)))
    def test_muon_rate_and_comparison_remain_pending(self):
        c=load_runtime(TEAM/"configs/arms/exp2_muon.yaml")
        self.assertIsNone(c["optim"]["muon_lr"])
        self.assertIsNone(c["optim"]["lr"])
        a=load_runtime(TEAM/"configs/arms/exp2_adamw.yaml")
        self.assertIs(a["intended"]["comparison_final"],False)
    def test_open_choice_metadata_matches_current_schema(self):
        metadata=json.loads((TEAM/"configs/open_choices.json").read_text())
        config=load_runtime(TEAM/"configs/arms/t1.yaml")
        for path in metadata:
            node=config
            for component in path.split("."):
                self.assertIn(component,node,path);node=node[component]
        self.assertEqual(metadata["evaluation.boundary_policy"]["supported"],[config["evaluation"]["boundary_policy"]])
    def test_all_profiles_resolve_to_tied_baseline(self):
        for name in ["t1","t2","t3"]:
            c=self.resolved(name+".yaml")
            self.assertIs(c["model"]["tie_embeddings"],True)
            self.assertEqual(c["model"]["head_mode"],"projected_ke2_tied")
            self.assertEqual(validate(c),[])
    def test_untied_baseline_rejected(self):
        c,_,_=fixture(head="untied_dense")
        self.assertTrue(any("baseline requires tied" in e for e in validate(c)))
    def test_exp5_untied_is_explicit_t2_exception(self):
        c=self.resolved("t2.yaml");c["intended"]["experiment"]="EXP-5"
        c["model"].update(head_mode="untied_dense",tie_embeddings=False)
        self.assertEqual(validate(c),[])
        c["intended"]["profile"]="T1"
        self.assertTrue(any("baseline requires tied" in e for e in validate(c)))
    def test_unresolved_baseline_rejected(self):
        self.assertTrue(validate(load_runtime(TEAM/"configs/arms/t1.yaml")))
    def test_all_five_lead_lr_arms(self):
        for filename,expected in [("lr_1e-4.yaml",1e-4),("lr_3e-4.yaml",3e-4),("lr_1e-3.yaml",1e-3),("lr_3e-3.yaml",3e-3),("lr_1e-2.yaml",1e-2)]:
            c=load_runtime(TEAM/"configs/arms/exp1"/filename)
            self.assertEqual(c["optim"]["lr"],expected);self.assertEqual(c["model"]["moe"]["ffn_hidden"],512)
    def test_lead_expert_override_preserves_shared_topk(self):
        c=load_runtime(TEAM/"configs/arms/exp3_experts_32.yaml")
        self.assertEqual((c["model"]["moe"]["num_experts"],c["model"]["moe"]["num_shared"],c["model"]["moe"]["top_k"],c["model"]["moe"]["ffn_hidden"]),(32,1,2,768))
        c=load_runtime(TEAM/"configs/arms/exp3_shared_0.yaml")
        self.assertEqual((c["model"]["moe"]["num_experts"],c["model"]["moe"]["num_shared"]),(16,0))
    def test_resolution_cannot_change_sizes(self):
        with self.assertRaises(ValueError):apply_resolution(self.resolved(),{"model":{"n_embd":128}})
    def test_muon_not_silently_adamw(self):
        c=self.resolved("exp2_muon.yaml")
        self.assertEqual(c["optim"]["name"],"muon")
        self.assertTrue(any("Muon" in e for e in validate(c)))
    def test_instructor_dimensions_and_lead_budgets(self):
        for name,w,l,h,kv,e,ffn,ctx,steps in [("t1",256,6,4,2,8,512,1024,245),("t2",512,8,8,2,16,768,2048,1221),("t3",640,10,10,2,16,896,2048,1221)]:
            c=load_runtime(TEAM/f"configs/arms/{name}.yaml");m=c["model"]
            self.assertEqual((m["n_embd"],m["n_layer"],m["n_head"],m["n_kv_head"],m["moe"]["num_experts"],m["moe"]["ffn_hidden"],m["block_size"]),(w,l,h,kv,e,ffn,ctx))
            self.assertEqual(c["run"]["steps"],steps)
    def test_canonical_lead_edit_changes_runtime(self):
        with copied_contract() as team:
            p=team/"configs/arms/t1.yaml";d=yaml.safe_load(p.read_text())
            d["model"]["n_layer"]=7;p.write_text(yaml.safe_dump(d))
            self.assertEqual(self.resolved(team=team)["model"]["n_layer"],7)
    def test_g6_default_changes_cannot_move_native_model(self):
        with copied_contract() as team:
            before=self.resolved(team=team)
            p=team.parent/"06-performance/configs/base.yaml";p.parent.mkdir(parents=True)
            p.write_text("model: {n_embd: 999, reversible: true}\noptim: {lr: 7.0}\n")
            self.assertEqual(before,self.resolved(team=team))
    def test_absolute_width_required_no_ratio_fallback(self):
        with copied_contract() as team:
            p=team/"configs/arms/t1.yaml";d=yaml.safe_load(p.read_text());d["intended"].pop("instructor_expert_ffn");p.write_text(yaml.safe_dump(d))
            with self.assertRaisesRegex(ValueError,"absolute expert width"):self.resolved(team=team)
    def test_new_absolute_width_key_is_supported(self):
        with copied_contract() as team:
            p=team/"configs/arms/t2.yaml";d=yaml.safe_load(p.read_text());d["model"]["moe"]["ffn_hidden"]=768;p.write_text(yaml.safe_dump(d))
            c=self.resolved("t2.yaml",team)
            self.assertEqual(c["provenance"]["expert_width_source"],"model.moe.ffn_hidden")
    def test_conflicting_widths_rejected(self):
        with copied_contract() as team:
            p=team/"configs/arms/t2.yaml";d=yaml.safe_load(p.read_text());d["model"]["moe"]["ffn_hidden"]=1024;p.write_text(yaml.safe_dump(d))
            with self.assertRaisesRegex(ValueError,"disagrees"):self.resolved("t2.yaml",team)
    def test_plan_change_requires_contract_review(self):
        with copied_contract() as team:
            p=team/"experiments/plan_v1.md";p.write_bytes(p.read_bytes()+b"\n")
            with self.assertRaisesRegex(ValueError,"plan changed"):self.resolved(team=team)
    def test_plan_line_endings_are_portable(self):
        with copied_contract() as team:
            before=self.resolved(team=team)
            p=team/"experiments/plan_v1.md";text=p.read_text(encoding="utf8")
            p.write_bytes(text.replace("\n","\r\n").encode("utf8"))
            self.assertEqual(before,self.resolved(team=team))

    def test_runtime_cannot_duplicate_lead_dimensions(self):
        with copied_contract() as team:
            p=team/"configs/runtime.yaml";d=yaml.safe_load(p.read_text());d["model"]["n_embd"]=128;p.write_text(yaml.safe_dump(d))
            with self.assertRaisesRegex(ValueError,"unsupported fields"):self.resolved(team=team)
    def test_smoke_cannot_override_explicit_lead_choice(self):
        with copied_contract() as team:
            p=team/"configs/arms/t1.yaml";d=yaml.safe_load(p.read_text());d["model"]["rope_theta"]=500000.0;p.write_text(yaml.safe_dump(d))
            c=load_runtime(p,team/"configs/runtime.yaml")
            self.assertEqual(c["model"]["rope_theta"],500000.0)
            with self.assertRaisesRegex(ValueError,"conflicts with explicit lead choice"):
                apply_resolution(c,load(team/"configs/small/smoke_resolution.yaml"))

    def test_unsupported_cached_ke_mode_is_not_ignored(self):
        with copied_contract() as team:
            p=team/"configs/arms/t1.yaml";d=yaml.safe_load(p.read_text());d["model"]["ke_mode"]="cached";p.write_text(yaml.safe_dump(d))
            with self.assertRaisesRegex(ValueError,"cached mode"):self.resolved(team=team)

    def test_unknown_lead_field_fails_instead_of_being_ignored(self):
        with copied_contract() as team:
            p=team/"configs/arms/t1.yaml";d=yaml.safe_load(p.read_text());d["model"]["unsupported_attention"]=True;p.write_text(yaml.safe_dump(d))
            with self.assertRaisesRegex(ValueError,"unsupported fields"):self.resolved(team=team)

if __name__=="__main__":unittest.main()
