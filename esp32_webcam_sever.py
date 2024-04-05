# Chương trình này nhận dữ liệu hình ảnh từ client và hiển thị lên màn hình
# Ngày 5 tháng 4 năm 2024
# Tác giả: Nguyễn Thanh Nhân

import cv2  # Import thư viện OpenCV để làm việc với hình ảnh
import socket  # Import thư viện socket để giao tiếp qua mạng
import pickle  # Import thư viện pickle để mã hóa và giải mã dữ liệu
import numpy as np  # Import thư viện numpy để làm việc với mảng nhiều chiều

# Tạo socket UDP
s  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Địa chỉ IP và cổng của server
ip = "192.168.4.2"
port = 6666
# Bind địa chỉ IP và cổng với socket
s.bind((ip, port))

while True:
    # Nhận dữ liệu từ client
    x = s.recvfrom(1000000)
    # Lấy địa chỉ IP của client
    clientip = x[1][0]
    # Nhận dữ liệu hình ảnh được gửi từ client
    data = x[0]
    # Giải mã dữ liệu thành hình ảnh
    data = pickle.loads(data)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # Hiển thị hình ảnh
    cv2.imshow('imgsever', img)
    # Đợi 5ms để người dùng có thể tắt chương trình bằng cách nhấn phím ESC
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Đóng cửa sổ hiển thị
cv2.destroyAllWindows()
