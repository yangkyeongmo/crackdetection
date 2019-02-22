# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import cv2
import numpy as np
import tensorflow as tf
import os
import argparse

parent_dataPath = 'C:\\Users\\HP\\Dropbox\\Projects\\crack\\data\\output\\train_result'

def create_graph(modelFullpath):
	"""저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
	# 저장된(saved) graph_def.pb로부터 graph를 생성한다.
	with tf.gfile.FastGFile(modelFullpath, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

def run_inference_on_image(imagepath, sess, labelsFullpath):
	answer = None
	if not tf.gfile.Exists(imagepath):
		tf.logging.fatal('File does not exist %s', imagepath)
		return None

	image_data = tf.gfile.FastGFile(imagepath, 'rb').read()
	softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
	predictions = sess.run(softmax_tensor,
 	                      {'DecodeJpeg/contents:0': image_data})
	predictions = np.squeeze(predictions)

	top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
	f = open(labelsFullpath, 'rb')
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


def run_no_segs(filepath, arg):
	path = filepath
	path_under_path = arg.model_path
	datapath = os.path.join(parent_dataPath, path_under_path)
	sess = tf.Session()
	create_graph(os.path.join(datapath, 'output_graph.pb'))

	f_path = os.path.join(os.path.dirname(path), 'record.txt')
	print(f_path)
	f = open(f_path, 'a+')
	f.write(path + '\n' + path_under_path + '\n')
	line = 'crack: ' + run_inference_on_image(path,sess).__str__() + '\n'
	print(line)
	f.write(line)


def record_result(rslt_path, start_time):
	record_path = os.path.join(os.path.dirname(rslt_path), 'record.txt')
	f = open(record_path, 'a+')
	print(os.path.join(os.path.dirname(rslt_path), 'record.txt'))
	f.write(rslt_path+'\n')
	f.write("Total running time: " + (time.time()-start_time).__str__() + '\n')
	f.close()


import time
def run_segs(filepath, arg):
	path = filepath
	seg = arg.seg
	dest = arg.dest
	start_time = time.time()
	path_under_path = arg.model_path
	datapath = os.path.join(parent_dataPath, path_under_path)
	original_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
	# original_image = cv2.equalizeHist()
	original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
	h, w = original_image.shape[:2]
	if h > w:
		w = w*800//h
		h = 800
	else:
		h = h*800//w
		w = 800
	original_image = cv2.resize(original_image, (w, h))
	overlay = np.zeros((h, w, 3), np.uint8)

	x, y = 0, 0
	intv = seg // 3
	next_x, next_y = seg, seg
	sess = tf.Session()
	create_graph(os.path.join(datapath, 'output_graph.pb'))
	end_x, end_y = False, False
	while x<w:
		while y<h:
			segment = original_image[y:next_y, x:next_x]
			segimg = cv2.imwrite(arg.segname + '.jpg', segment)
			prediction = run_inference_on_image(arg.segname + '.jpg', sess,
												os.path.join(datapath, 'output_labels.txt'))
			is_red = False
			for i in range(y, next_y):
				for j in range(x, next_x):
					if overlay[i,j][2] > 0:
						is_red = True
						break
                            
			if prediction > 0.9:
				overlay[y:next_y, x:next_x] = (0,0,255*prediction/2) 
			elif prediction > 0.7 and not is_red:
				overlay[y:next_y, x:next_x] = (0,255*prediction/2,0)
			elif prediction >= 0 and not is_red:
				overlay[y:next_y, x:next_x] = (255*prediction/2,0,0)
			elif prediction is None:
				print("Prediction is NONE")
				return
			if prediction > 0.9:
				print(x.__str__() +':'+ next_x.__str__() +','+y.__str__() +
                                        ':' + next_y.__str__() + ' :: ' + prediction.__str__())
			y = y + intv
			next_y = next_y + intv
			if end_y:
				break
			if next_y > h:
				y = h - seg
				next_y = h
				end_y = True
		x = x + intv
		next_x = next_x + intv
		if end_x:
			break
		if next_x > w:
			x = w - seg
			next_x = w
			end_x = True
		y = 0
		next_y = seg
		end_y = False
	os.remove(arg.segname + '.jpg')
	rsltimg = cv2.addWeighted(original_image, 0.5, overlay, 0.5, 0)
	# write result
	rsltpath = os.path.join(dest, path[-6:-4] + '_' + path_under_path.replace("\\", "_")
							+ ',' + seg.__str__() + '.jpg')
	if not os.path.exists(os.path.dirname(rsltpath)):
		os.makedirs(os.path.dirname(rsltpath))
	cv2.imwrite(rsltpath, rsltimg)
	# write overlay
	ovpath = rsltpath[0:-4] + '_' + 'overlay.jpg'
	cv2.imwrite(ovpath, overlay)
	print(rsltpath)
	record_result(rsltpath, start_time)


def main(arg):
	path = arg.path
	seg = arg.seg
	dest = arg.dest
	filelist = list()
	if not os.path.isfile(path):
		if not os.path.isdir(path):
			print("NOT FILE NOR DIR ERROR: "+path)
			return
		else:
			for file in os.listdir(path):
				filepath = os.path.join(path,file)
				if os.path.isfile(filepath):
					if filepath[-4:] == '.jpg':
						filelist.append(os.path.join(path,file))
	else:
		filelist.append(path)
		filelist.sort()
	for filepath in filelist:
		if seg == 0:
			run_no_segs(filepath, arg)
		else:
			run_segs(filepath, arg)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--path',
		action='store'
	)
	parser.add_argument(
		'--seg',
		action='store',
        default=0,
		type=int
	)
	parser.add_argument(
        "--dest",
        action='store',
	)
	parser.add_argument(
        "--model_path",
		action='store'
	)
	parser.add_argument(
		"--segname",
		default="seg"
	)
	arg = parser.parse_args()
	main(arg)
