# -*- coding: utf-8 -*-
"""deeplearning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B4Tw8KLkIrYsDeB7UYl331ayjDJ1hSM4
"""

!pip install tensorflow-gpu===2.8.0

import tensorflow as tf
print(tf.__version__)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataset=pd.read_csv('Churn_Modelling.csv')
dataset.head()

## Divide the dataset into independent and dependent feature
x=dataset.iloc[:,3:13].values
y=dataset.iloc[:,13].values

x.head()

y

##feature engineering
geography = pd.get_dummies(dataset,columns=['Geography'],drop_first=True)
gender = pd.get_dummies(dataset,columns=['Gender'],drop_first=True)

## concatenate these variable with dataframes
dataset=pd.concat([dataset,geography,gender],axis=1)

dataset

## feature engineering
geography = pd.get_dummies(dataset,columns=['Geography'],drop_first=True)
gender = pd.get_dummies(dataset,columns=['Gender'],drop_first=True)

# Assuming 'dataset' is your original DataFrame
x = dataset.copy()  # Create a copy of your DataFrame

## concatenate these variable with dataframe
X = x.drop(['Geography','Gender'],axis=1)

X.head()

X=pd.concat([X,geography,gender],axis=1)

#splitting the dataset into training set and test set
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=0)

#for which all algorithms feature engineering is required
#ANN , Linear Regression , Logistic Regression , Desent

#feature scalling
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

## Parts 2 Now lets create the ANN
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LeakyReLU,PReLU,ELU
from tensorflow.keras.layers import Dropout

## lets initialize the ANN
classifier=Sequential()

## Adding the input Layer
classifier.add(Dense(units=11,activation='relu'))
classifier.add(Dropout(0.3))

## adding thefirestlayer
classifier.add(Dense(units=7,activation='relu'))
classifier.add(Dropout(0.3))

## addint the six layer
classifier.add(Dense(units = 6 , activation = 'relu'))
classifier.add(Dropout(0.3))

##adding the output layer
classifier.add(Dense(units=1,activation='sigmoid'))
classifier.add(Dropout(0.3))

## Compiling the ANN
classifier.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

import tensorflow

opt = tensorflow.keras.optimizers.Adam(learning_rate=0.01)

##Early Stopping
import tensorflow as tf

# Instantiate the EarlyStopping callback and assign it to the variable 'early_stopping'
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=0.0001,
    patience=20,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=False,
)

X_train_numeric = X_train.select_dtypes(include=np.number).astype(np.float32)  # Select numeric columns and convert to float32
y_train = y_train.astype(np.float32)  # Convert to float32

model_history = classifier.fit(
    X_train_numeric.values, # Use .values to get the underlying NumPy array
    y_train,
    validation_split=0.33,
    batch_size=10,
    epochs=1000,
    callbacks=[early_stopping] # Pass the instantiated callback as a list
)

model_history.history.keys()

plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# part 3 : Making the predictions and evaluting the model

# predicting the Test set Results
X_test_numeric = X_test.select_dtypes(include=np.number).astype(np.float32) # Select numeric columns and convert to float32 to match the model's input
y_pred = classifier.predict(X_test_numeric)
y_pred = (y_pred > 0.5)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

## calculate the acuracy score
  from sklearn.metrics import accuracy_score
  score=accuracy_score(y_pred,y_test)

score

## get the weight
classifier.get_weights()

