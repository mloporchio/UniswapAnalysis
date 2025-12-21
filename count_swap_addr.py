"""
Counts the frequency of sender and recipient addresses in swap events.
Author: Matteo Loporchio
"""
import gzip
import time

INPUT_FILE = "results/swaps.tsv.gz"
OUTPUT_FILE = "results/swap_addr.tsv"

count_map = dict()

start = time.time()
total_count = 0
with gzip.open(INPUT_FILE, "rt") as input_fh:
    line = input_fh.readline() # Skip header
    for line in input_fh:
        parts = line.strip().split("\t")
        sender = parts[6]
        recipient = parts[7]
        # Update sender count
        s_count, r_count = count_map.get(sender, (0, 0))
        s_count += 1
        count_map[sender] = (s_count, r_count)
        # Update recipient count
        s_count, r_count = count_map.get(recipient, (0, 0))
        r_count += 1
        count_map[recipient] = (s_count, r_count)
        total_count += 1

with open(OUTPUT_FILE, "w") as output_fh:
    output_fh.write("address\tnum_sender\tnum_recipient\n")
    for address in count_map.keys():
        s_count, r_count = count_map.get(address)
        output_fh.write(f"{address}\t{s_count}\t{r_count}\n")

elapsed = time.time() - start
print(f"{total_count}\t{elapsed:.3f}")

