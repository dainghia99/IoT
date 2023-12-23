import requests
import time
from keras.models import load_model
import pygame

import numpy as np

dweet_url = "https://dweet.io/get/latest/dweet/for/Nhom_5"

tinh_trang = ""

model = load_model("data.h5")

def play_mp3(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    time.sleep(6)
    pygame.mixer.music.stop()

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
            play_mp3("amthanh.mp3")

        print(prediction[0, 0])
        print(f"Nhiệt độ: {temperature}°C")
        print(f"Độ ẩm: {humidity}%")
        print(f"Âm thanh: {sound}")
        print(f"Gas: {gas}%")
        print("Tình trạng: ", tinh_trang)
        time.sleep(1)
    else:
        print("Không thể kết nối!")