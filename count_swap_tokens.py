"""

OUTPUT:
1) TSV file with the ranking of pools by number of swap events
2) TSV file with the list of unique tokens involved in swap events

PRINT:
1) Number of pools
2) Number of unique tokens involved in swap events
3) Time taken to perform the computation

Author: Matteo Loporchio
"""

import polars as pl
import time
import pool_utils

POOL_CREATION_FILE = "data/pool_creations.tsv"
OUTPUT_FILE_1 = "results/swap_pool_rank.tsv"
OUTPUT_FILE_2 = "results/swap_token_list.tsv"

start = time.time()
pool_rank = pool_utils.pool_event_frequency("SWAP").sort("SWAP", descending=True).join(
    pl.read_csv(POOL_CREATION_FILE, separator="\t").select("pool_address", "token_0", "token_1").rename({"pool_address":"address"}), 
    on="address", 
    how="left"
).select("address", "token_0", "token_1", "SWAP")
pool_rank.write_csv(OUTPUT_FILE_1, separator="\t", include_header=True)

token_list = pl.concat([pool_rank.select("token_0").rename({"token_0":"token"}), 
                        pool_rank.select("token_1").rename({"token_1":"token"})]).unique()
token_list.write_csv(OUTPUT_FILE_2, separator="\t", include_header=False)

elapsed = time.time() - start
print(f"{len(pool_rank)}\t{len(token_list)}\t{elapsed:.3f}")
