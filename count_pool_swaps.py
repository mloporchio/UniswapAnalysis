"""
This script ...

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/pool_swaps.tsv"
count_map = dict()

start = time.time()

for e in read_utils.pool_data_reader():
    address = e['address']
    signature = e['topics'][0]
    if signature != read_utils.TYPE_SIGNATURES['SWAP']: 
        if count_map.get(address, -1) == -1:
            count_map[address] = 0
        continue
    current_count = count_map.get(address, 0)
    current_count += 1
    count_map[address] = current_count
    
with open(OUTPUT_FILE, "w") as fh:
    fh.write("address\tnum_swap\n")
    for key, value in count_map.items():
        fh.write(f"{key}\t{value}\n")

end = time.time()
elapsed = end - start
print(f"{elapsed:.2f}")