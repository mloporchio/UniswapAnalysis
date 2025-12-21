"""
Docstring per count_swap_txs
Author: Matteo Loporchio
"""

import polars as pl
import time

INPUT_FILE = "results/swaps.tsv.gz"
OUTPUT_FILE = "results/swap_txs.tsv"

start = time.time()
df = pl.read_csv(INPUT_FILE, separator="\t", schema_overrides={
    "amount0" : pl.Utf8,
    "amount1" : pl.Utf8,
    "sqrtPriceX96" : pl.Utf8,
    "liquidity" : pl.Utf8,
    "tick" : pl.Utf8
})
res = df.group_by("transaction_hash").len(name="num_swap")
res.write_csv(OUTPUT_FILE, separator="\t", include_header=True)
total_count = len(df)
elapsed = time.time() - start
print(f"{total_count}\t{elapsed:.3f}")

