# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import cv2
import numpy as np
import tensorflow as tf
import os
import argparse

parent_path = '/home/luar7olye/Dropbox/Projects/crack/train_result'
path_under_path = 'sizeeq,noeq/100x100'
dataPath = os.path.join(parent_path, path_under_path)
modelFullPath = os.path.join(dataPath, 'output_graph.pb')
# 읽어들일 graph 파일 경로
labelsFullPath = os.path.join(dataPath, 'output_labels.txt')
# 읽어들일 labels 파일 경로


def create_graph():
    """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
    # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath, sess):
    answer = None
    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return None

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


def run_no_segs(path):
	sess = tf.Session()
	create_graph()
	print(run_inference_on_image(path,sess).__str__())


def run_segs(path, seg):
	original_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
#original_image = cv2.equalizeHist()
	original_image = cv2.cvtColor(original_image, cv2.COLOR_GRAY2BGR)
	h, w = original_image.shape[:2]
	if h > w:
		h = 800
		w = w*800/h
	else:
		h = h*800/w
		w = 800
	original_image = cv2.resize(original_image, (w, h))
	overlay = np.zeros((h, w, 3), np.uint8)

	x, y = 0, 0
	next_x, next_y = seg, seg
	sess = tf.Session()
	create_graph()
	while x<w:
		while y<h:
			segment = original_image[y:next_y, x:next_x]
			segimg = cv2.imwrite('seg.jpg', segment)
			prediction = run_inference_on_image('seg.jpg', sess)
			if prediction > 0.9:
				overlay[y:next_y, x:next_x] = (0,0,255*prediction/2) 
			elif prediction > 0.7:
				overlay[y:next_y, x:next_x] = (0,255*prediction/2,0)
			elif prediction >= 0:
				overlay[y:next_y, x:next_x] = (255*prediction/2,0,0)
			elif prediction == None:
				print("Prediction is NONE")
				return
			if prediction > 0.3:
				cv2.putText(overlay, "{0:.3f}".format(prediction), \
						(x, y+seg/2),\
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255))
			print(x.__str__() +','+ y.__str__() + ": " + prediction.__str__())
			y = y + seg
			next_y = next_y + seg
			if next_y > h:
				next_y = h
		x = x + seg
		next_x = next_x + seg
		if next_x > w:
			next_x = w
		y = 0
		next_y = seg
	os.remove('seg.jpg')
	rsltimg = cv2.addWeighted(original_image, 0.5, overlay, 0.5, 0)
	rsltpath = path[0:-4] + path_under_path.replace("/", "_") + ',' + seg.__str__() + '.jpg'
	cv2.imwrite(rsltpath, rsltimg)
	print(rsltpath)


def main(path, seg):
	filelist = list()
	if not os.path.isfile(path):
		if not os.path.isdir(path):
			print("NOT FILE NOR DIR ERROR: "+path)
			return
		else:
			for file in os.listdir(path):
				filepath = os.path.join(path,file)
				if os.path.isfile(filepath):
					filelist.append(os.path.join(path,file))
	else:
		filelist.append(path)
    
	for filepath in filelist:
		if seg == 0:
		    run_no_segs(filepath)
		else:
		    run_segs(filepath, seg)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--path',
		action='store'
	)
	parser.add_argument(
		'--seg',
		action='store',
		type=int
	)
	arg = parser.parse_args()
	main(arg.path, arg.seg)
