import os
from keras.models import load_model, Model
from numpy import array
import numpy as np

from sklearn.cluster import DBSCAN
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

sequence = []
with open('../data/scaled_data.txt', encoding="utf8") as fp:
    for line in fp:
        pom = []
        for s in line:
            if s == '0':
                pom.append([1,0,0,0,0])
            elif s == '1':
                pom.append([0,1,0,0,0])
            elif s == '2':
                pom.append([0,0,1,0,0])
            elif s == '3':
                pom.append([0,0,0,1,0])
            elif s == '4':
                pom.append([0,0,0,0,1])
        sequence.append(pom)

one_hot_len = 5
reg_num = 30
example_num = len(sequence)
sequence = array(sequence)
sequence = sequence.reshape((example_num, reg_num, one_hot_len))
print(sequence.shape)
print("Mesec")

model = load_model('../autoencoder/best/rnn_512_64_8-086-0.731802-0.701754.h5')
encoder_model = Model(inputs = model.input, outputs = model.layers[2].output)
encoder_model_out = encoder_model.predict(sequence)

print(encoder_model_out.shape)

ret = []
for x in encoder_model_out:
    dist_to_5th = np.array([99999.99 for x in range (0,6)])

    for y in encoder_model_out:
        dist = euclidean(x, y)
        if dist_to_5th[5] > dist:
            dist_to_5th[5] = dist
            dist_to_5th = np.sort(dist_to_5th)

    ret.append(dist_to_5th[5])

plt.figure(figsize=(7, 7))
plt.plot(range(len(ret)), np.sort(array(ret)))
plt.grid(True)
plt.show()

clustering = DBSCAN(eps=0.6, min_samples=5).fit(encoder_model_out)
print(clustering.labels_)
print(len(clustering.labels_[clustering.labels_ == 0]))
print(len(clustering.labels_[clustering.labels_ == 1]))
print(len(clustering.labels_[clustering.labels_ == 2]))
print(len(clustering.labels_[clustering.labels_ == 3]))
