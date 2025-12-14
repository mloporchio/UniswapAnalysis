"""
This script counts the number of events for each block in the dataset.
The script outputs a TSV file where each row represents a block and has the following fields:
1)
2)
3)

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/block_events.tsv"
count_map = dict()
num_events = 0

start = time.time()

for e in read_utils.pool_data_reader():
    block_number = e['block_number']
    block_timestamp = e['block_timestamp']
    key = (block_number, block_timestamp)
    current_count = count_map.get(key, 0)
    current_count += 1
    count_map[key] = current_count
    num_events += 1
    
with open(OUTPUT_FILE, "w") as fh:
    fh.write("block_number\tblock_timestamp\tnum_events\n")
    for key, value in count_map.items():
        block_number, block_timestamp = key
        fh.write(f"{block_number}\t{block_timestamp}\t{value}\n")

end = time.time()
elapsed = end - start
print(f"{num_events}\t{elapsed:.2f}")