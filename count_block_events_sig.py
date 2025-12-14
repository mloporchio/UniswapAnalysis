"""
This script counts the number of pool events for each block in the dataset.

The script outputs a TSV file where each row represents a block and has the following fields:
1) block_number: the height of the block;
2) block_timestamp: the timestamp of the block;
3) 
4)
5)
6)
7)
8)
9)

The script prints the following values to stdout:
1) number of events read;
2) elapsed time (in seconds).

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/block_events_sig.tsv"
result_map = dict()

start = time.time()

num_events = 0
for e in read_utils.pool_data_reader():
    block_number = e['block_number']
    block_timestamp = e['block_timestamp']
    key = (block_number, block_timestamp)
    event_type = read_utils.get_event_type(e)
    current_dict = result_map.get(key, dict())
    current_count = current_dict.get(event_type, 0)
    current_count += 1
    current_dict[event_type] = current_count
    result_map[key] = current_dict
    num_events += 1
    
with open(OUTPUT_FILE, "w") as fh:
    header_str = '\t'.join(read_utils.EVENT_TYPES)
    fh.write(f"block_number\tblock_timestamp\t{header_str}\n")
    for key, value in result_map.items():
        block_number, block_timestamp = key
        current_dict = value
        counts = []
        for event_type in read_utils.EVENT_TYPES:
            counts.append(str(current_dict.get(event_type, 0)))
        counts_str = '\t'.join(counts)
        fh.write(f"{block_number}\t{block_timestamp}\t{counts_str}\n")

end = time.time()
elapsed = end - start
print(f"{num_events}\t{elapsed:.3f}")