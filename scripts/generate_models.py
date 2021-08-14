#!/usr/bin/env python
#mandatory imports
import logging as log
import os

#script imports
import pickle
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense

log.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=log.INFO, datefmt='%d-%b-%y %H:%M:%S', handlers=[log.FileHandler(f"logs/{os.path.basename(__file__)[:-3]}.log"), log.StreamHandler()])

#global variables
PICKLE_FILE_PATH = "assets/chatbot.pickle"
JSON_FILE_PATH = "assets/chatbotmodel.json"
HDF5_FILE_PATH = "assets/chatbotmodel.h5"

def generate():

    log.info('Initializing script.')

    log.info(f'Loading data from pickle: {PICKLE_FILE_PATH}')
    try:
        with open(PICKLE_FILE_PATH, "rb") as file:
            words, labels, training, output = pickle.load(file)
    except:
        log.exception('Error loading data from pickle')
        exit()

    log.info('Data loaded from pickle.')

    log.info('Creating neural network.')
    chat_model = Sequential()
    chat_model.add(Dense(8, input_shape=[len(words)], activation='relu'))
    chat_model.add(Dense(len(labels), activation='softmax'))

    log.info('Optimizing the model.')
    chat_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    log.info('Training the model.')
    chat_model.fit(training, output, epochs=1000, batch_size=8)

    log.info(f'Serializing model to yaml and exporting to {JSON_FILE_PATH}')
    model_json = chat_model.to_json()
    with open(JSON_FILE_PATH, "w") as file:
        file.write(model_json)

    log.info(f'Serializing model to HDF5 and exporting to {HDF5_FILE_PATH}')
    chat_model.save(HDF5_FILE_PATH)

    log.info('Finished training model.')

if __name__ == '__main__':
    generate()