# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import cv2
import os
import numpy as np
import tensorflow as tf
import argparse
import shutil


def create_graph(modelFullPath):
	"""저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
	# 저장된(saved) graph_def.pb로부터 graph를 생성한다.
	with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath, sess, labelsFullPath):
	answer = None

	if not tf.gfile.Exists(imagePath):
		tf.logging.fatal('File does not exist %s', imagePath)
		return answer

	image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

	# 저장된(saved) GraphDef 파일로부터 graph를 생성한다.

	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	predictions = sess.run(softmax_tensor,
                           {'DecodeJpeg/contents:0': image_data})
	predictions = np.squeeze(predictions)

	top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
	f = open(labelsFullPath, 'rb')
	lines = f.readlines()
	labels = [str(w).replace("\n", "") for w in lines]
	ref_labels = list(labels)
	ref_labels.sort()
	for node_id in top_k:
		human_string = labels[node_id]
		score = predictions[node_id]
		if human_string == ref_labels[0]:
			answer = score
	return answer


def main(path, model_path):
	if not os.path.exists(path):
		print("NO PATH ERROR: "+path)
		return
	filelist = list()
	if not os.path.isfile(path):
		if not os.path.isdir(path):
			print("NOT FILE NOR DIR ERROR: "+path)
			return
		else:
			for file in os.listdir(path):
				filepath = os.path.join(path, file)
				if os.path.isfile(filepath):
					filelist.append(filepath)
	else:
		filelist.append(path)
	filelist.sort()
	items_left = len(filelist)
	parent_dir = os.path.dirname(path)
	crackpath = os.path.join(parent_dir, 'crack')
	notcrackpath = os.path.join(parent_dir, 'not_crack')
	if not os.path.exists(crackpath):
		os.mkdir(crackpath)
	if not os.path.exists(notcrackpath):
		os.mkdir(notcrackpath)

	parent_dataPath = 'C:\\Users\\HP\\Dropbox\\Projects\\crack\\data\\output\\train_result'
	path_under_path = model_path
	dataPath = os.path.join(parent_dataPath, path_under_path)

	sess = tf.Session() 
	create_graph(os.path.join(dataPath, 'output_graph.pb'))
	cracknum = 0
	notcracknum = 0
	for filepath in filelist:
		items_left = items_left - 1
		filename = os.path.basename(filepath)
		print(items_left.__str__() + ' items left, currently: ' + filename),
		prediction = run_inference_on_image(filepath, sess, os.path.join(
											dataPath, 'output_labels.txt'))
		if prediction > 0.95:
			writepath = os.path.join(crackpath, filename)
			cracknum = cracknum + 1
			print(": crack")
		else:
			writepath = os.path.join(notcrackpath, filename)
			notcracknum = notcracknum + 1
			print(": not_crack")
		os.rename(filepath, writepath)
	print("Cracks: "+cracknum.__str__())
	print("Not Cracks: "+notcracknum.__str__())

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
        '--path',
        action='store'
    )
	parser.add_argument(
    	'--model_path',
    	action='store',
    	default='base'
    )
	arg = parser.parse_args()
	main(arg.path, arg.model_path)
