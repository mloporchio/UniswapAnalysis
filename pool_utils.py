import read_utils
import polars as pl

def pool_event_frequency(event_type):
    assert event_type in read_utils.EVENT_TYPES
    cdf = pl.read_csv("data/pool_creations.tsv", separator="\t").select("pool_address").rename({"pool_address":"address"})
    tmp = pl.read_csv("results/pool_events.tsv", separator="\t").select("address", event_type)
    return cdf.join(tmp, on="address", how="left").fill_null(0).sort(event_type, descending=True)