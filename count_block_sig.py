"""
This script counts the number of events for each signature in the dataset.
The script outputs a TSV file where each row ... and has the following fields:
1) ...
2) ...

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/block_sig.tsv"
count_map = dict()

start = time.time()

for e in read_utils.pool_data_reader():
    block_number = e['block_number']
    block_timestamp = e['block_timestamp']
    signature = e['topics'][0]
    signature_type = read_utils.SIGNATURE_TYPES[signature]
    key = (block_number, block_timestamp, signature_type)
    current_count = count_map.get(key, 0)
    current_count += 1
    count_map[key] = current_count
    
with open(OUTPUT_FILE, "w") as fh:
    fh.write("block_number\tblock_timestamp\tsignature_type\tcount\n")
    for key, value in count_map.items():
        block_number, block_timestamp, signature_type = key
        fh.write(f"{block_number}\t{block_timestamp}\t{signature_type}\t{value}\n")

end = time.time()
elapsed = end - start
print(f"{elapsed:.2f}")