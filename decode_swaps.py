"""
This script reads the Uniswap v3 pool event dataset, filters the SWAP events and decodes their parameters.
The SWAP event is defined as follows:

event Swap(
    address indexed sender,
    address indexed recipient,
    int256 amount0,
    int256 amount1,
    uint160 sqrtPriceX96,
    uint128 liquidity,
    int24 tick
);

The decoded SWAP events are written to a compressed TSV file for further analysis.
The output file contains the following columns:
- address: The address of the Uniswap v3 pool contract.
- transaction_index: The index of the transaction within the block.
- log_index: The index of the log within the transaction.
- transaction_hash: The hash of the transaction.
- block_number: The number of the block containing the transaction.
- block_timestamp: The timestamp of the block containing the transaction.
- sender: The address of the sender of the swap.
- recipient: The address of the recipient of the swap.
- amount0: The amount of token0 involved in the swap.
- amount1: The amount of token1 involved in the swap.
- sqrtPriceX96: The square root of the price after the swap, multiplied by 2^96.
- liquidity: The liquidity of the pool after the swap.

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

if __name__ == "__main__":
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