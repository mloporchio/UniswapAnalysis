#!/bin/bash
#
#   This script uses the plfit utility to fit power law functions to the event frequency distributions of Uniswap pools.
#
#   Author: Matteo Loporchio
#

EVENT_TYPES=("INITIALIZE" "MINT" "SWAP" "BURN" "COLLECT" "IOCN" "FLASH")
PLFIT_EXEC="~/plfit-1.0.1/build/src/plfit"
TEMP_DIR="tmp"
OUTPUT_FILE="results/fit.tsv"

mkdir -p $TEMP_DIR

printf "event_type\talpha\tx_min\tL\tD\tp_value\telapsed_time\n" > $OUTPUT_FILE
for EVENT_TYPE in "${EVENT_TYPES[@]}"; do
    TEMP_FILE="${TEMP_DIR}/input_${EVENT_TYPE}.txt"
    # Preparing input data for plfit.
    echo "Preparing input data for ${EVENT_TYPE}..."
    START_TIME=$EPOCHSECONDS
    python3 - <<END
import polars as pl
cdf = pl.read_csv("data/pool_creations.tsv", separator="\t").select("pool_address").rename({"pool_address":"address"})
tmp = pl.read_csv("results/pool_events.tsv", separator="\t").select("address", "${EVENT_TYPE}")
sdf = cdf.join(tmp, on="address", how="left").fill_null(0).select("${EVENT_TYPE}")
sdf.write_csv('${TEMP_FILE}', include_header=False)
END
    echo "Done in $((EPOCHSECONDS - START_TIME)) seconds."
    # Fitting power law to input data.
    echo "Fitting power law for ${EVENT_TYPE}..."
    START_TIME=$EPOCHSECONDS
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
        printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$EVENT_TYPE" "$ALPHA" "$X_MIN" "$LL" "$KS" "$P_VALUE" "$ELAPSED_TIME" >> $OUTPUT_FILE
    else
        echo "Error: fitting failure for ${EVENT_TYPE}."
        rm -rf $TEMP_DIR
        exit 1
    fi
    rm -f $TEMP_FILE
done
echo "All event types completed!"
rm -rf $TEMP_DIR
exit 0