import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import matplotlib.pyplot as plt

# Load data from Excel file
file_path = 'data.csv'
df = pd.read_csv(file_path)

# Giả sử cột cuối cùng chứa nhãn
x = df.iloc[:, :4].values.astype(float)  # Chuyển đổi dữ liệu đầu vào thành float
y_ = df.iloc[:, -1].values.reshape(-1, 1)

# chuyển đổi dữ liệu máy học
encoder = OneHotEncoder(sparse=False)
y = encoder.fit_transform(y_)

#Tách dữ liệu để đào tạo và kiểm tra
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.20, random_state=42)

#Xây dựng mô hình mạng nơ ron
model = Sequential()
model.add(Dense(10, input_shape=(x.shape[1],), activation='relu', name='fc1'))
model.add(Dense(10, activation='relu', name='fc2'))
model.add(Dense(y.shape[1], activation='softmax', name='output'))

# Trình tối ưu hóa Adam với tỷ lệ học là 0,001
optimizer = Adam(lr=0.001)
model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

print('Neural Network Model Summary: ')
print(model.summary())

# máy học
history = model.fit(train_x, train_y, verbose=2, batch_size=7, epochs=200, validation_data=(test_x, test_y))
# model.fit(train_x, train_y, verbose=2, batch_size=7, epochs=200)
model.save("data.h5")

# Kiểm tra dữ liệu chưa nhìn thấy
results = model.evaluate(test_x, test_y)

print('Final test set loss: {:4f}'.format(results[0]))
print('Final test set accuracy: {:4f}'.format(results[1]))

# Biểu đồ loss và accuracy
plt.figure(figsize=(12, 4))

# Biểu đồ Loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

# Biểu đồ Accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()

# Hiển thị biểu đồ
plt.show()