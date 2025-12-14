#!/bin/bash
#
#   This script uses the plfit utility to fit a power law function to the number of swaps performed by Uniswap pools.
#
#   Author: Matteo Loporchio
#

PLFIT_EXEC="~/plfit-1.0.1/build/src/plfit"
TEMP_DIR="tmp"
TEMP_FILE="${TEMP_DIR}/input.txt"
OUTPUT_FILE="results/fit_swaps.tsv"

mkdir -p $TEMP_DIR

# Preparing input data for plfit.
echo "Preparing input data..."
START_TIME=$EPOCHSECONDS
python3 - <<END
import polars as pl
cdf = pl.read_csv("data/pool_creations.tsv", separator="\t").select("pool_address").rename({"pool_address":"address"})
tmp = pl.read_csv("results/pool_events.tsv", separator="\t").select("address", "SWAP").rename({"SWAP":"num_swap"})
sdf = cdf.join(tmp, on="address", how="left").fill_null(0).select("num_swap")
sdf.write_csv('${TEMP_FILE}', include_header=False)
END
echo "Done in $((EPOCHSECONDS - START_TIME)) seconds."

# Fitting power law to input data.
echo "Fitting power law..."
START_TIME=$EPOCHSECONDS
printf "alpha\tx_min\tL\tD\tp_value\telapsed_time\n" > $OUTPUT_FILE
if PLFIT_OUT=$((eval ${PLFIT_EXEC} -p exact -b ${TEMP_FILE}) 2>/dev/null); then
    ELAPSED_TIME=$((EPOCHSECONDS - START_TIME))
    echo "Done in ${ELAPSED_TIME} seconds."
    echo "Result: ${PLFIT_OUT}"
    # Fitted exponent, minimum X value, log-likelihood (L), Kolmogorov-Smirnov statistic (D) and p-value (p)
    ALPHA=$(echo $PLFIT_OUT | cut -d' ' -f3)
    X_MIN=$(echo $PLFIT_OUT | cut -d' ' -f4)
    LL=$(echo $PLFIT_OUT | cut -d' ' -f5)
    KS=$(echo $PLFIT_OUT | cut -d' ' -f6)
    P_VALUE=$(echo $PLFIT_OUT | cut -d' ' -f7)
    printf "%s\t%s\t%s\t%s\t%s\t%s\n" "$ALPHA" "$X_MIN" "$LL" "$KS" "$P_VALUE" "$ELAPSED_TIME" >> $OUTPUT_FILE
else
    echo "Error: fitting failure for model $MODEL and metric $METRIC."
    rm -rf $TEMP_DIR
    exit 1
fi
rm -rf $TEMP_DIR
exit 0