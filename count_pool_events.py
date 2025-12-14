"""
This script ...

Author: Matteo Loporchio
"""

import read_utils
import time

OUTPUT_FILE = "results/pool_events.tsv"
result_map = dict()

start = time.time()

for e in read_utils.pool_data_reader():
    address = e['address']
    event_type = read_utils.get_event_type(e)
    current_dict = result_map.get(address, dict())
    current_count = current_dict.get(event_type, 0)
    current_count += 1
    current_dict[event_type] = current_count
    result_map[address] = current_dict
    
with open(OUTPUT_FILE, "w") as fh:
    header_str = '\t'.join(read_utils.EVENT_TYPES)
    fh.write(f"address\t{header_str}\n")
    for key, value in result_map.items():
        current_dict = value
        counts = []
        for event_type in read_utils.EVENT_TYPES:
            counts.append(str(current_dict.get(event_type, 0)))
        counts_str = '\t'.join(counts)
        fh.write(f"{key}\t{counts_str}\n")

end = time.time()
elapsed = end - start
print(f"{elapsed:.2f}")