# -*- coding: utf-8 -*-

import os 
import numpy as np
import tensorflow as tf


def predict(input1, input2):

    input_dim = 2
    output_dim = 1
    hidden_dim = 4

    tf.reset_default_graph()

    x = tf.placeholder(tf.float32, [None, input_dim])
    w1 = tf.Variable(tf.random_uniform([input_dim, hidden_dim], minval=-0.9, maxval=0.9), name='w1')
    b1 = tf.Variable(tf.random_uniform([hidden_dim], minval=-0.9, maxval=0.9), name='b1')
    w2 = tf.Variable(tf.random_uniform([hidden_dim, output_dim], minval=-0.9, maxval=0.9), name='w2')
    b2 = tf.Variable(tf.random_uniform([output_dim], minval=-0.9, maxval=0.9), name='b2')
    hidden_layer = tf.sigmoid(tf.matmul(x, w1) + b1)
    y = tf.sigmoid(tf.matmul(hidden_layer, w2) + b2)
    prediction = tf.round(y)

    saver = tf.train.Saver()

    with tf.Session() as sess:

        #cwd = os.getcwd()
        script_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(script_path, 'model.ckpt')    

        sess.run(tf.initialize_all_variables())
        saver.restore(sess, model_path)

        test_data = np.array([[input1,input2]])
        feed_dict = {x: test_data}

        result = prediction.eval(feed_dict=feed_dict)[0][0]

        return result

    return None










