"""
Author: Matteo Loporchio
"""

from pathlib import Path
import tarfile
import json

YEARS = range(2021, 2025 + 1)

SIGNATURE_TYPES = {
    "0x98636036cb66a9c19a37435efc1e90142190214e8abeb821bdba3f2990dd4c95":"INITIALIZE",
    "0x7a53080ba414158be7ec69b987b5fb7d07dee101fe85488f0853ae16239d0bde":"MINT",
    "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67":"SWAP",
    "0x0c396cd989a39f4459b5fa1aed6a9a8dcdbc45908acfd67e028cd568da98982c":"BURN",
    "0x70935338e69775456a85ddef226c395fb668b63fa0115f5f20610b388e6ca9c0":"COLLECT",
    "0xac49e518f90a358f652e4400164f05a5d8f7e35e7747279bc3a93dbf584e125a":"IOCN",
    "0xbdbdb71d7860376ba52b25a5028beea23581364a40522f6bcfb86bb1f2dca633":"FLASH"
}

TYPE_SIGNATURES = dict(zip(SIGNATURE_TYPES.values(), SIGNATURE_TYPES.keys()))

# Source: https://www.nintoracaudio.dev/data-eng,python/2024/11/06/tar-stream
def iter_tar_gz(file_path):
    tfile = tarfile.open(file_path, 'r:gz')
    for t in tfile:
        if not t.isfile(): continue
        path = Path(t.path)
        f = tfile.extractfile(t)
        yield path, f


def pool_data_reader():
    for year in YEARS:
        archive_path = f"data/pool_events_{year}.tar.gz"
        for file_path, file in iter_tar_gz(archive_path):
            if not file_path.suffix.endswith(".json"): continue # skip all non-JSON files
            file_content = file.read().decode('utf-8')
            for event_string in file_content.splitlines(): # each line is a Uniswap pool event
                event = json.loads(event_string)
                yield event