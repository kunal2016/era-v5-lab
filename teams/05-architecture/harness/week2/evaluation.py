"""Heldout sum-of-loss / sum-of-raw-bytes scorer, never batch-mean BPB."""
import math
import torch
from torch.nn import functional as F

def token_nll(logits,targets):
    return F.cross_entropy(logits.float().reshape(-1,logits.shape[-1]),targets.reshape(-1),ignore_index=-100,reduction="none").reshape(targets.shape)

@torch.no_grad()
def evaluate(model,dataset,batch_size,device,autocast_context):
    training=model.training;cpu_rng=torch.get_rng_state();cuda_rng=torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None
    values=[];byte_count=0;token_count=0
    try:
        model.eval()
        for start in range(0,len(dataset.windows),batch_size):
            x,y,lengths=dataset.batch(range(start,min(start+batch_size,len(dataset.windows))),device)
            with autocast_context():nll=token_nll(model(x,y!=-100),y)
            if not torch.isfinite(nll).all():raise ValueError("Nonfinite heldout NLL")
            values.append(math.fsum(nll[y!=-100].double().cpu().tolist()))
            byte_count+=int(lengths.sum());token_count+=int((y!=-100).sum())
        if byte_count!=dataset.raw_bytes:raise ValueError("Heldout denominator failed byte conservation")
        total=math.fsum(values)
        return {"val/nll_nats":total,"val/utf8_bytes":byte_count,"val/scored_tokens":token_count,
                "val/bpb":total/math.log(2)/byte_count,"val/perplexity":math.exp(total/token_count)}
    finally:
        model.train(training);torch.set_rng_state(cpu_rng)
        if cuda_rng is not None:torch.cuda.set_rng_state_all(cuda_rng)
