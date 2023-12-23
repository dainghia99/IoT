import requests
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

# Sử dụng hàm để tạo ra một chuỗi ngẫu nhiên có độ dài 8 ký tự
historyId = generate_random_string(16)


# API endpoint để thực hiện POST
api_url = "http://localhost:3000/api/training"

# Dữ liệu bạn muốn gửi qua API
data_to_send = {
    "nhietDo": "",
    "doAm": "",
    "amThanh": "",
    "gas": "",
    "tinhTrang": "",
    "historyId": "",
}

import requests
import time

dweet_url = "https://dweet.io/get/latest/dweet/for/Nhom_5"

tinh_trang = ""

with open('data.csv', mode='a', encoding='utf-8') as file:
  file.write("nhietDo"+"," + "doAm," + "amThanh," + "Gas, " + "tinhTrang" + "\n")
  while True:
    response = requests.get(dweet_url)
    if response.status_code == 200:
        data = response.json()
        
        temperature = data['with'][0]['content']['Nhietdo']
        humidity = data['with'][0]['content']['Doam']
        sound = data['with'][0]['content']["Amthanh"]
        gas = data['with'][0]['content']["gas"]
        
        if temperature > 30 and sound > 380: 
           tinh_trang = "Cao" 
        else: 
           tinh_trang = "binhThuong"
        file.write(str(temperature) + ',' + str(humidity) +"," + str(sound) + "," + str(gas) + ',' + tinh_trang  + '\n')
        print(f"Nhiệt độ: {temperature}°C")
        print(f"Độ ẩm: {humidity}%")
        print(f"Âm thanh: {sound}")
        print(f"Gas: {gas}%")
        print("Tình trạng: ", tinh_trang)


        data_to_send["nhietDo"] = str(20)
        data_to_send["doAm"] = str(220)
        data_to_send["amThanh"] = str(245)
        data_to_send["gas"] = str(2)
        data_to_send["tinhTrang"] = tinh_trang
        data_to_send["historyId"] = historyId

        # Gửi yêu cầu POST đến API
        response = requests.post(api_url, json=data_to_send)


        time.sleep(1)
    else:
        print("Không thể kết nối!")




