import requests
import time
import pygame
import string
from keras.models import load_model
import numpy as np
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

dweet_url = "https://dweet.io/get/latest/dweet/for/Nhom_5"

api_url = "http://localhost:3000/api/training"

def play_mp3(file_path):
   pygame.init()
   pygame.mixer.init()
   pygame.mixer.music.load(file_path)
   pygame.mixer.music.play()
   time.sleep(5)
   pygame.mixer.music.stop()


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def push_data_to_api_and_csv_file():
   tinh_trang = ""
   data_to_send = {
    "nhietDo": "",
    "doAm": "",
    "amThanh": "",
    "gas": "",
    "tinhTrang": "",
    "historyId": "",
   }

   with open('data.csv', mode='a', encoding='utf-8') as file:
      # file.write("nhietDo"+"," + "doAm," + "amThanh," + "Gas, " + "tinhTrang" + "\n")
      while True:
         historyId = generate_random_string(16)
         response = requests.get(dweet_url)
         if response.status_code == 200:
            data = response.json()
            
            temperature = data['with'][0]['content']['Nhietdo']
            humidity = data['with'][0]['content']['Doam']
            sound = data['with'][0]['content']["Amthanh"]
            gas = data['with'][0]['content']["gas"]
            
            if temperature > 29 and sound > 300: 
               tinh_trang = "Cao" 
            else: 
               tinh_trang = "binhThuong"
            file.write(str(temperature) + ',' + str(humidity) +"," + str(sound) + "," + str(gas) + ',' + tinh_trang  + '\n')

            data_to_send["nhietDo"] = str(temperature)
            data_to_send["doAm"] = str(humidity)
            data_to_send["amThanh"] = str(sound)
            data_to_send["gas"] = str(gas)
            data_to_send["tinhTrang"] = tinh_trang
            data_to_send["historyId"] = historyId

            response = requests.post(api_url, json=data_to_send)

            print(f"Nhiệt độ: {temperature}°C")
            print(f"Độ ẩm: {humidity}%")
            print(f"Âm thanh: {sound}")
            print(f"Gas: {gas}%")
            print("Tình trạng: ", tinh_trang)
            time.sleep(1)
         else:
            print("Không thể kết nối!")

def test_data():
   model = load_model("data.h5")
   while True:
    response = requests.get(dweet_url)
    if response.status_code == 200:
        data = response.json()
        temperature = data['with'][0]['content']['Nhietdo']
        humidity = data['with'][0]['content']['Doam']
        sound = data['with'][0]['content']["Amthanh"]
        gas = data['with'][0]['content']["gas"]

        prediction = model.predict(np.array([[temperature,humidity, sound, gas]]))
        
        threshold = 0.75
        if prediction[0, 0] > threshold:
          print("Cảnh báo")
          play_mp3("amthanh.mp3")
        print(prediction[0,0])
        print(f"Nhiệt độ: {temperature}°C")
        print(f"Độ ẩm: {humidity}%")
        print(f"Âm thanh: {sound}")
        print(f"Gas: {gas}%")
        time.sleep(1)
    else:
        print("Không thể kết nối!")

def training_data(data_file_name):
   file_path = data_file_name
   df = pd.read_csv(file_path)

   # Giả sử cột cuối cùng chứa nhãn
   x = df.iloc[:, :4].values.astype(float)
   y_ = df.iloc[:, -1].values.reshape(-1, 1)

   encoder = OneHotEncoder(sparse=False)
   y = encoder.fit_transform(y_)

   train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.20, random_state=42)
   
   model = Sequential()
   model.add(Dense(10, input_shape=(x.shape[1],), activation='relu', name='fc1'))
   model.add(Dense(10, activation='relu', name='fc2'))
   model.add(Dense(y.shape[1], activation='softmax', name='output'))
   optimizer = Adam(lr=0.001)
   model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
   model.fit(train_x, train_y, verbose=2, batch_size=7, epochs=200, validation_data=(test_x, test_y))
   model.save("data.h5")

def main():
   # push_data_to_api_and_csv_file()
   # training_data("data.csv")
   test_data()
   
main()
