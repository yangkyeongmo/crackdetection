# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서
이미지에 대한 추론(inference)을 진행하는 예제"""

import os
import numpy as np
import tensorflow as tf
import argparse


model_result_dir_root = '/home/luar7olye/Dropbox/Projects/crack/train_result'


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

    # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
    top_k = predictions.argsort()[-5:][::-1]
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


def get_write_path_and_add_count(prediction, path_dict, filename, crack_count):
    _path = ''
    if prediction > 0.95:
        _path = os.path.join(path_dict['crack'], filename)
        crack_count[0] += 1
        print(": crack")
    else:
        _path = os.path.join(path_dict['not_crack'], filename)
        crack_count[1] += 1
        print(": not_crack")
    return _path


def iterate_through_filelist(filelist, path_dict):
    sess = tf.Session()
    create_graph(os.path.join(path_dict['model'], 'output_graph.pb'))

    items_left = len(filelist)
    # crack_count[0] = crack, crack_count[1] = not_crack
    crack_count = [0, 0]
    for filepath in filelist:
        filename = os.path.basename(filepath)
        print(str(items_left), 'items left, currently:', filename)
        prediction = run_inference_on_image(filepath, sess,
                                            os.path.join(path_dict['model'],
                                                         'output_labels.txt'))
        writepath = get_write_path_and_add_count(prediction, path_dict,
                                                 filename, crack_count)
        os.rename(filepath, writepath)
        items_left = items_left - 1
    print("Cracks:", str(crack_count[0]))
    print("Not Cracks:", str(crack_count[1]))


def mkdir_if_not_exists(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_path_dict(arg):
    _dict = {}
    path_dir = os.path.dirname(arg.path)
    _dict['crack'] = os.path.join(path_dir, 'crack')
    _dict['not_crack'] = os.path.join(path_dir, 'not_crack')
    _dict['model'] = os.path.join(model_result_dir_root, arg.model_dirname)

    # create crack and not crack dir if doesn't exist
    mkdir_if_not_exists(_dict['crack'])
    mkdir_if_not_exists(_dict['not_crack'])

    return _dict


def main(arg):
    filelist = get_file_list(arg.path)
    path_dict = get_path_dict(arg)
    iterate_through_filelist(filelist, path_dict)


def get_file_list(path):
    filelist = list()
    if not os.path.exists(path):
        print("NO PATH ERROR:", path)
        return
    if not os.path.isfile(path):
        if not os.path.isdir(path):
            print("NOT FILE NOR DIR ERROR:", path)
            return
        else:
            for file in os.listdir(path):
                filepath = os.path.join(path, file)
                if os.path.isfile(filepath):
                    filelist.append(filepath)
    else:
        filelist.append(path)
    filelist.sort()
    return filelist


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p', '--path',
    )
    parser.add_argument(
        '-md', '--model_dirname',
        default='base'
    )
    arg = parser.parse_args()
    main(arg)
