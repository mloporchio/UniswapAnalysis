"""
This script ...

event Swap(
    address indexed sender,
    address indexed recipient,
    int256 amount0,
    int256 amount1,
    uint160 sqrtPriceX96,
    uint128 liquidity,
    int24 tick
);

Author: Matteo Loporchio
"""

import gzip
import read_utils
import time
from eth_abi import decode

OUTPUT_FILE = "results/swaps.tsv.gz"

def decode_swap(event):
    # Swap(address,address,int256,int256,uint160,uint128,int24)
    sender = event['topics'][1]
    recipient = event['topics'][2]
    decoded = decode(['int256','int256','uint160','uint128','int24'], bytes.fromhex(event['data'][2:]))
    result = {
        "sender" : sender,
        "recipient" : recipient,
        "amount0" : decoded[0],
        "amount1" : decoded[1],
        "sqrtPriceX96" : decoded[2],
        "liquidity" : decoded[3],
        "tick" : decoded[4]
    }
    return result

start = time.time()
total_count = 0
swap_count = 0
with gzip.open(OUTPUT_FILE, "wt") as fh:
    fh.write("address\ttransaction_index\tlog_index\ttransaction_hash\tblock_number\tblock_timestamp\tsender\trecipient\tamount0\tamount1\tsqrtPriceX96\tliquidity\ttick\n")
    for e in read_utils.pool_data_reader():
        event_type = read_utils.get_event_type(e)
        if event_type == "SWAP":
            address = e['address']
            transaction_index = e['transaction_index']
            log_index = e['log_index']
            transaction_hash = e['transaction_hash']
            block_number = e['block_number']
            block_timestamp = e['block_timestamp']
            d = decode_swap(e)
            sender = d['sender']
            recipient = d['recipient']
            amount0 = d['amount0']
            amount1 = d['amount1']
            sqrtPriceX96 = d['sqrtPriceX96']
            liquidity = d['liquidity']
            tick = d['tick']
            # 
            if sender.startswith("0x"):
                sender = "0x" + sender[-40:]
            if recipient.startswith("0x"):
                recipient = "0x" + recipient[-40:]
            fh.write(f"{address}\t{transaction_index}\t{log_index}\t{transaction_hash}\t{block_number}\t{block_timestamp}\t{sender}\t{recipient}\t{amount0}\t{amount1}\t{sqrtPriceX96}\t{liquidity}\t{tick}\n")
            swap_count += 1
        total_count += 1

end = time.time()
elapsed = end - start
print(f"Processed {total_count} events, found {swap_count} swaps in {elapsed:.2f} seconds.")