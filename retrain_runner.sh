#!/bin/bash
# run python ./src/retrain/retrain_run_mod.py
# args: --path 'path to base image' --seg 'segment size'
# args: --dest 'result saving path' --model_path 'path of model to use'
# --path = ${BASEIMG}
# --seg = ${FOLDERNAME}
# --dest = ${FOLDER} (not base)
# --model_path = ${FOLDERNAME}/[50 100 200 400]

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
EXAMINEPATH=$SCRIPTPATH/data/input/examine/img
SRCPATH=$SCRIPTPATH/src/retrain/retrain_run_mod.py

for TN in $EXAMINEPATH/*/; do
	# $TNFOLDERNAME: [t1 t2 t3 t4 t5]
	TNFOLDERNAMERAW=${TN##*img/}
	TNFOLDERNAME=${TNFOLDERNAMERAW:0:2}
	echo ON EXMDATA : $TNFOLDERNAME 
	# org: TNTAIL=${TN##*img/t}
	# org: TNNUMBER=${TNTAIL:0:1}
	# org: echo $TNNUMBER : $TN
	# $BASEIMG is path to base img.
	# $BASEIMG: $FOLDER[t1_ovl.jpg t2_ovl.jpg ... t5_ovl.jpg]
	BASEIMG=$SCRIPTPATH/data/input/examine/examine_data/${TNFOLDERNAME}.jpg
	echo $BASEIMG
	# FOLDER is path to folder under $TN.
	for FOLDER in $TN*; do
		# FOLDERNAME is name of folder, not path.
		# $FOLDERNAME: [base 30 50 100]
		FOLDERNAME=${FOLDER##*$TNFOLDERNAME/}
		# org: FOLDERNAME=${FOLDER##*t$TNNUMBER//}
		echo FOLDER: $FOLDERNAME
		if [ $FOLDERNAME != "base" ]; then
			# $FOLDER: path to [30 50 100]
			# $FOLDERNAME: [30 50 100]
			for DATAPERCLASS in 50 100 200 400; do
				python ${SRCPATH} --path ${BASEIMG} --dest ${FOLDER}/ --seg ${FOLDERNAME} --model_path ${FOLDERNAME}/${DATAPERCLASS}
				echo path: $BASEIMG
				echo dest: ${FOLDER}/
				echo seg: ${FOLDERNAME}
				echo mpath: ${FOLDERNAME}/${DATAPERCLASS}
			done
		fi
	done
done
