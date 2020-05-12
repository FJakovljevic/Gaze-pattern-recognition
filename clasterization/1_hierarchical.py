import os
from keras.models import load_model, Model
from numpy import array, argwhere, argmax

import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
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

print(encoder_model_out)
print(encoder_model_out.shape)

plt.figure(figsize=(7, 7))
dend = shc.dendrogram(shc.linkage(encoder_model_out, method='ward'))
plt.show()

cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
cluster.fit_predict(encoder_model_out)
print(cluster.labels_)
print(len(cluster.labels_[cluster.labels_ == 0]))
print(len(cluster.labels_[cluster.labels_ == 1]))
print(len(cluster.labels_[cluster.labels_ == 2]))
print(len(cluster.labels_[cluster.labels_ == 3]))

zero = argwhere(cluster.labels_ == 0)
one = argwhere(cluster.labels_ == 1)
two = argwhere(cluster.labels_ == 2)
three = argwhere(cluster.labels_ == 3)

print()
zero_cluster = sequence[zero]
for y in zero_cluster[:20]:
    pom = ''
    for j in y:
        for k in j:
            pom += str(argmax(k))
    
    print(pom)


print()
one_cluster = sequence[one]
for y in one_cluster[:20]:
    pom = ''
    for j in y:
        for k in j:
            pom += str(argmax(k))
    
    print(pom)

print()
two_cluster = sequence[two]
for y in two_cluster[:20]:
    pom = ''
    for j in y:
        for k in j:
            pom += str(argmax(k))
    
    print(pom)

print()
three_cluster = sequence[three]
for y in three_cluster[:20]:
    pom = ''
    for j in y:
        for k in j:
            pom += str(argmax(k))
    
    print(pom)