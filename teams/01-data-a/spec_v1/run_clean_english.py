"""Kept so the old command still works. clean_english.py is no longer used: clean.py is the one cleaner, so this runs
run_clean.py, which runs clean.py. The options and the outputs are run_clean.py's.

  python run_clean_english.py --pack en-dclm.parquet --out out     (the same as: python run_clean.py --pack en-dclm.parquet --out out)
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / "run_clean.py"), run_name="__main__")
