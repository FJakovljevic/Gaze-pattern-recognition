# lstm autoencoder recreate sequence
from numpy import array, argmax
from keras import optimizers
from keras.models import Sequential, Model
from keras.layers import LSTM, Dense, RepeatVector, TimeDistributed
from keras.utils import plot_model
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from keras.models import model_from_json
from keras.callbacks import ModelCheckpoint
# from sklearn.model_selection import train_test_split

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
# define model
model = Sequential()
model.add(LSTM(512, activation='tanh', input_shape=(reg_num,one_hot_len), return_sequences=True))
model.add(LSTM(64, activation='tanh', input_shape=(reg_num,one_hot_len), return_sequences=True))
model.add(LSTM(5, activation='tanh', return_sequences=False))
model.add(RepeatVector(reg_num))
model.add(LSTM(5, activation='tanh', return_sequences=True))
model.add(LSTM(64, activation='tanh', input_shape=(reg_num,one_hot_len), return_sequences=True))
model.add(LSTM(512, activation='tanh', return_sequences=True))
model.add(TimeDistributed(Dense(one_hot_len)))

checkpoint = ModelCheckpoint('rnn_512_64_5-{epoch:03d}-{acc:03f}-{val_acc:03f}.h5', verbose=0, monitor='val_loss',save_best_only=True, mode='auto') 
model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])
print(model.summary())

# fit model
# model.fit(sequence, sequence, epochs=1000, verbose=1, validation_split=0.3, shuffle=True, batch_size=512)
history  = model.fit(sequence, sequence, epochs=300, verbose=1, batch_size=128, validation_split=0.1, shuffle=True, callbacks=[checkpoint])

print(history.history.keys())
# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

yhat = model.predict(sequence[:10], verbose=0)
# print(yhat)
for y in yhat:
    pom = ''
    for k in y:
        pom += str(argmax(k))
    
    print(pom)