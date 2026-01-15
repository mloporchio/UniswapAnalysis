"""
This script counts the number of swaps triggered by each transaction.
It reads the dataset of decoded Uniswap v3 SWAP events and groups them by transaction hash.

Author: Matteo Loporchio
"""

import polars as pl
import time
import gzip

INPUT_FILE = "results/swaps.tsv.gz" # Input file with decoded swap events
OUTPUT_FILE = "results/swap_txs.tsv.gz" # Output file with counts of swaps per transaction

start = time.time()
df = pl.read_csv(INPUT_FILE, separator="\t", schema_overrides={
    "amount0" : pl.Utf8,
    "amount1" : pl.Utf8,
    "sqrtPriceX96" : pl.Utf8,
    "liquidity" : pl.Utf8,
    "tick" : pl.Utf8
})
res = df.group_by("transaction_hash").len(name="num_swap")
with gzip.open(OUTPUT_FILE, "wb") as fh:
    res.write_csv(fh, separator="\t", include_header=True)
total_count = len(df)
elapsed = time.time() - start
print(f"{total_count}\t{elapsed:.3f}")

