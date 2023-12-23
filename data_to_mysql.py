import pandas as pd
import mysql.connector
import uuid

# Thay các giá trị sau bằng thông tin kết nối cơ sở dữ liệu MySQL của bạn
db_config = {
    'user': 'root',
    'password': '123456',
    'host': 'localhost',
    'database': 'ai-iot'
}

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('DataHuanLuyen.csv')

# Kết nối đến cơ sở dữ liệu MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Tên bảng bạn muốn tạo và đổ dữ liệu vào
table_name = 'data_traning'

# Tạo bảng với cấu trúc dựa trên cấu trúc dữ liệu từ tệp CSV
create_table_query = f"CREATE TABLE {table_name} (id VARCHAR(36) DEFAULT '{str(uuid.uuid4())}', {', '.join([f'{col} VARCHAR(255)' for col in data.columns])})"
cursor.execute(create_table_query)

# Đẩy dữ liệu vào cơ sở dữ liệu MySQL
for index, row in data.iterrows():
    sql = f"INSERT INTO {table_name} ({', '.join(data.columns)}) VALUES ({', '.join(['%s']*len(data.columns))})"
    values = tuple(row)
    cursor.execute(sql, values)

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()
