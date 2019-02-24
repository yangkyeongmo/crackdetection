#!/bin/bash
# Find fn and fp from result of runner
# source: quantititive_validator.py
# args:
# --expected: result img overlay path
# --real: baseimg overlay path
# --seg: segment size of expected img

SOURCEPATH=`realpath $0`
SOURCEDIRPATH=`dirname $SOURCEPATH`
EXAMINEPATH=$SOURCEDIRPATH/data/input/examine/img
RECORDPATH=$SOURCEDIRPATH/data/output/examine

# $TN=path to [t1 t2 t3 t4 t5]
for TN in $EXAMINEPATH/*/; do
        TNNAME=`basename $TN`
        BASEOVERLAYIMG=${TN}base/${TNNAME}_ovl.jpg
        # $SEG=path to [30 50 100]
        for SEG in $TN*/; do
                # $SEGSIZE=[30 50 100]
                SEGSIZE=`basename $SEG`
                if [ $SEGSIZE != "base" ]; then
                        for EXPECTED_OVERLAY in $SEG*_overlay.jpg; do
                                echo real               : $BASEOVERLAYIMG
                                echo expected           : $EXPECTED_OVERLAY
                                echo seg                : $SEGSIZE
                                python $SOURCEDIRPATH/src/quantititive_validator_new.py --expected $EXPECTED_OVERLAY --real $BASEOVERLAYIMG --seg $SEGSIZE --record $RECORDPATH
                        done
                fi
        done
done
