#!/bin/bash
SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
SRCPATH=$SCRIPTPATH/src/retrain/retrain_mod.py
echo SRCPATH: $SRCPATH 
# image_dir: $SCRIPTPATH/data/input/train_input/for_training/(30 50 100)/(50 100 200 400)
# output_path: (30 50 100)_(50 100 200 400)
DATAPATH=$SCRIPTPATH/data/input/train_input/for_training

for SEG in $DATAPATH/*; do
	SEGNUMBER=${SEG##*for_training/}
	for DATACOUNT in $SEG/*; do
		if [ $SEGNUMBER != "base" ]; then
		DATACOUNTNUMBER=${DATACOUNT##*$SEGNUMBER/}
			echo SEGNUM: $SEGNUMBER DATACOUNTNUMBER $DATACOUNTNUMBER
			echo imagedir: $DATACOUNT 
			echo modelpath: ${SEGNUMBER}/${DATACOUNTNUMBER}
			python $SRCPATH --image_dir $DATACOUNT --output_path ${SEGNUMBER}/${DATACOUNTNUMBER}
		fi
	done
done
