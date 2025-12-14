"""
This script counts the number of events for each signature in the dataset.
The script outputs a TSV file where each row represents a signature and has the following fields:
1) Signature
2) Number of occurrences

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/sig_count.tsv"
count_map = dict()
num_signatures = 0

start = time.time()

for e in read_utils.pool_data_reader():
    signature = e['topics'][0]
    current_count = count_map.get(signature, 0)
    current_count += 1
    count_map[signature] = current_count
    
with open(OUTPUT_FILE, "w") as fh:
    fh.write("signature\tcount\n")
    for key, value in count_map.items():
        fh.write(f"{key}\t{value}\n")
        num_signatures += 1

end = time.time()
elapsed = end - start
print(f"{num_signatures}\t{elapsed:.2f}")