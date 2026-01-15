"""
This script uses the Alchemy API to fetch metadata for a list of Ethereum ERC-20 token addresses.
It reads the addresses from a TSV file, retrieves the metadata, and writes the results to another TSV file.

Author: Matteo Loporchio
"""

import csv
import json
import os
import requests
import time
from dotenv import load_dotenv

load_dotenv() # Load .env into os.environ

INPUT_FILE = "results/swap_token_list.tsv"
OUTPUT_FILE = "results/swap_token_metadata.tsv"

API_KEY = os.getenv("ALCHEMY_API_KEY")
BASE_URL = f"https://eth-mainnet.g.alchemy.com/v2/{API_KEY}"
HEADERS = {"Content-Type": "application/json"}

def get_token_metadata(address):
    response = requests.post(BASE_URL, headers={}, json={
        "jsonrpc": "2.0",
        "method": "alchemy_getTokenMetadata",
        "params": [address],
        "id": 1
    })
    if response.status_code != 200:
        raise Exception(f"Error in response for {address}: {response.text}")
    res = response.json()
    if "error" in res:
        raise Exception(f"Error in response for {address}: {res['error']['message']}")
    return res["result"]

if __name__ == "__main__":
    input_fh = open(INPUT_FILE, "r")
    lines = input_fh.readlines()
    input_fh.close()
    count = 1
    total = len(lines)
    address = None
    with open(OUTPUT_FILE, "w", newline='') as output_fh:
        output_writer = csv.writer(output_fh, delimiter='\t')
        output_writer.writerow(["address", "name", "symbol", "decimals", "logo"])
        for line in lines:
            address = line.strip()
            name = None
            symbol = None
            decimals = None
            logo = None
            print(f"Downloading address {address}... ({count}/{total})")
            try:
                result = get_token_metadata(address)
                name = result.get("name")
                symbol = result.get("symbol")
                decimals = result.get("decimals")
                logo = result.get("logo")
            except Exception as e:
                print(e)
            output_writer.writerow([address, name, symbol, decimals, logo])
            time.sleep(0.5)
            count += 1