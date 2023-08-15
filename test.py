import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from keras.optimizers import Adam
from keras.models import load_model
import tensorflow as tf

def rmse(predictions, y_test):
    rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
    return rmse

def LSTM_mod(x_train, y_train, x_test):
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape= (x_train.shape[1], 1)))
    model.add(LSTM(128, return_sequences=False))
    #model.add(Dense(80))
    model.add(Dense(60))
    model.add(Dense(40))
    model.add(Dense(20))
    model.add(Dense(1))
    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    # Train the model
    model.fit(x_train, y_train, batch_size=32, epochs=30)
    predictions_scaled = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions_scaled)
    return predictions, model

def LSTM_model(x_test):
    predictions = model1.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    return predictions

def plot_model(predictions, training_data_len):
    # Plot the data
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    # Visualize the data
    plt.figure(figsize=(10,4))
    plt.title('Model')
    plt.xlabel('Date', fontsize=14)
    plt.ylabel('Close Price USD ($)', fontsize=14)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=60))  # Adjust interval as needed
    plt.gcf().autofmt_xdate()
    plt.plot(train['Close'], linewidth=1)
    plt.plot(valid[['Close', 'Predictions']], linewidth=1)
    plt.legend(['Train', 'Val', 'Predictions'], loc='lower right')
    plt.show()

def training(training_data_len, train_data):
    x_train = []
    y_train = []

    for i in range(60, len(train_data)):
        x_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
            
    # Convert the x_train and y_train to numpy arrays 
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    test_data = scaled_data[training_data_len - 60: , :]
    # Create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i-60:i, 0])
        
    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    return x_train, y_train, x_test, y_test

def save_model(model):
    model.save('my_model.h5')

model1 = load_model('model_rmse_3.010_amazon.h5')

# Read data from CSV file
df = pd.read_csv('.\\CSV Files\\NVD.DE.csv')

df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

data = df.filter(['Close']) 

dataset = data.values

training_data_len = int(np.ceil( len(dataset) * .8 ))

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0:int(training_data_len), :]
# Split the data into x_train and y_train data sets

# Get the models predicted price values 
x_train, y_train, x_test, y_test = training(training_data_len, train_data)

#LSTM_predictions = LSTM_model(x_test)

LSTM_preds, model = LSTM_mod(x_train, y_train, x_test)

#plot_model(LSTM_predictions, training_data_len)

plot_model(LSTM_preds, training_data_len)

#LSTM_predictions_list = LSTM_predictions.tolist()
LSTM_preds_list = LSTM_preds.tolist()
y_test = y_test.tolist()

#l = list(zip(LSTM_predictions_list, y_test))

m = list(zip(LSTM_preds, y_test))

'''print("\n\n\nPrice predictions and actual comparison from model loaded\n\n")

for i in range(len(l)):
    print(l[i][0][0], l[i][1][0], sep = ' ')
'''
print("\n\n\nPrice predictions and actual comparison from the model built\n\n")

for i in range(len(m)):
    print(m[i][0][0], m[i][1][0], sep = ' ')

build_mod_rmse = rmse(LSTM_preds, y_test)
#save_model_rmse = rmse(LSTM_predictions, y_test)

'''if build_mod_rmse < save_model_rmse:
    save_model(model)'''

#print("\n\nPrint Root mean squared error from model loaded", save_model_rmse)
print("\n\nPrint Root mean squared error from model built", build_mod_rmse)