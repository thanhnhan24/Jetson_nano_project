# Chương trình này sử dụng để truyền dữ liệu hình ảnh từ camera lên Webserver
# Ngày 5 tháng 4 năm 2024
# Tác giả: Nguyễn Thanh Nhân

import cv2  # Import thư viện OpenCV để làm việc với hình ảnh
import socket  # Import thư viện socket để giao tiếp qua mạng
import pickle  # Import thư viện pickle để mã hóa và giải mã dữ liệu
import os  # Import thư viện os để làm việc với hệ thống tập tin
import numpy as np  # Import thư viện numpy để làm việc với mảng nhiều chiều

# Tạo socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Tăng kích thước buffer để tránh mất mát dữ liệu khi truyền
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000)

# Địa chỉ IP và cổng của server
server_ip = "192.168.1.1"
sever_port = 6666

# Khởi tạo camera
cap = cv2.VideoCapture(0)
# Thiết lập kích thước khung hình
cap.set(3, 640)
cap.set(4, 480)

while cap.isOpened():
    # Đọc frame từ camera
    ret, img = cap.read()
    # Chuyển đổi frame thành định dạng JPEG để truyền đi
    ret, buffer = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    # Mã hóa dữ liệu thành dạng bytes để gửi đi
    x_as_bytes = pickle.dumps(buffer)
    # Gửi dữ liệu đến server
    s.sendto((x_as_bytes), (server_ip, sever_port))
    # Hiển thị frame
    cv2.imshow('data', img)
    # Đợi 5ms để người dùng có thể tắt chương trình bằng cách nhấn phím ESC
    if cv2.waitKey(5) & 0xFF == 27:
        break

# Đóng cửa sổ hiển thị và giải phóng tài nguyên camera
cv2.destroyAllWindows()
cap.release()
