from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import cv2
import sys

class Image_in(QObject):
    image_data = Signal(QImage)
    status_changed = Signal(str)  # Tín hiệu để thay đổi trạng thái

    def __init__(self):
        super(Image_in, self).__init__()
        self.en = False  # Biến để kiểm tra trạng thái của việc lấy ảnh từ webcam

    def start_webcam(self):
        cap = cv2.VideoCapture(0)
        self.en = True  # Bắt đầu lấy ảnh từ webcam
        if cap.isOpened():  # Kiểm tra xem có mở được camera không
            self.status_changed.emit("Lấy ảnh từ webcam thành công")  # Phát tín hiệu trạng thái
            while True:
                ret, frame = cap.read()
                if ret:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, ch = rgb_image.shape
                    bytes_per_line = ch * w
                    convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                    p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                    self.image_data.emit(p)
                if not self.en:  # Kiểm tra nếu biến en là False thì dừng lấy ảnh từ webcam
                    break
            cap.release()
            cv2.destroyAllWindows()
        else:
            self.status_changed.emit("Không thể mở camera")  # Phát tín hiệu trạng thái lỗi

    def stop_webcam(self):
        self.en = False  # Ngưng lấy ảnh từ webcam
        self.status_changed.emit("Ngưng lấy ảnh, vui lòng khởi động lại cửa sổ")


class Ui_Console(object):
    def setupUi(self, Console):
        if not Console.objectName():
            Console.setObjectName(u"Console")
        Console.resize(1035, 729)
        self.centralwidget = QWidget(Console)
        self.centralwidget.setObjectName(u"centralwidget")
        self.img_csl_label = QLabel(self.centralwidget)
        self.img_csl_label.setObjectName(u"img_csl_label")
        self.img_csl_label.setGeometry(QRect(30, 30, 201, 31))
        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.img_csl_label.setFont(font)
        self.img_output = QLabel(self.centralwidget)
        self.img_output.setObjectName(u"img_output")
        self.img_output.setGeometry(QRect(30, 70, 671, 391))
        self.output_csl = QListView(self.centralwidget)
        self.output_csl.setObjectName(u"output_csl")
        self.output_csl.setGeometry(QRect(30, 530, 671, 131))
        self.output_label = QLabel(self.centralwidget)
        self.output_label.setObjectName(u"output_label")
        self.output_label.setGeometry(QRect(30, 490, 201, 31))
        self.output_label.setFont(font)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(770, 30, 241, 161))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75)
        self.groupBox.setFont(font1)
        self.cam_in = QPushButton(self.groupBox)
        self.cam_in.setObjectName(u"cam_in")
        self.cam_in.setGeometry(QRect(10, 40, 221, 28))
        self.esp_in = QPushButton(self.groupBox)
        self.esp_in.setObjectName(u"esp_in")
        self.esp_in.setGeometry(QRect(10, 80, 221, 28))
        self.end_crawl = QPushButton(self.groupBox)
        self.end_crawl.setObjectName(u"end_crawl")
        self.end_crawl.setGeometry(QRect(10, 120, 221, 28))
        Console.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Console)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1035, 26))
        Console.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Console)
        self.statusbar.setObjectName(u"statusbar")
        Console.setStatusBar(self.statusbar)

        self.retranslateUi(Console)

        QMetaObject.connectSlotsByName(Console)
    # setupUi

    def retranslateUi(self, Console):
        Console.setWindowTitle(QCoreApplication.translate("Console", u"MainWindow", None))
        self.img_csl_label.setText(QCoreApplication.translate("Console", u"IMAGE RECEIVED", None))
        self.img_output.setText("")
        self.output_label.setText(QCoreApplication.translate("Console", u"OUTPUT", None))
        self.groupBox.setTitle(QCoreApplication.translate("Console", u"B\u1ea3ng \u0111i\u1ec1u khi\u1ec3n h\u00ecnh \u1ea3nh", None))
        self.cam_in.setText(QCoreApplication.translate("Console", u"Webcam crawl", None))
        self.esp_in.setText(QCoreApplication.translate("Console", u"Webserver crawl", None))
        self.end_crawl.setText(QCoreApplication.translate("Console", u"End crawling", None))
    # retranslateUi

class ConsoleMainWindow(QMainWindow):
    def __init__(self):
        super(ConsoleMainWindow, self).__init__()
        self.ui = Ui_Console()
        self.ui.setupUi(self)

        self.image_in = Image_in()
        self.image_in.image_data.connect(self.display_image)
        self.image_in.status_changed.connect(self.update_status)  # Kết nối tín hiệu thay đổi trạng thái
        self.ui.cam_in.clicked.connect(self.start_webcam)
        self.ui.end_crawl.clicked.connect(self.stop_webcam)
        self.image_thread = QThread()

         # Khởi tạo model cho QListView
        self.model = QStandardItemModel()
        self.ui.output_csl.setModel(self.model)

    def start_webcam(self):
        self.image_in.moveToThread(self.image_thread)
        self.image_thread.started.connect(self.image_in.start_webcam)
        self.image_thread.start()

    def stop_webcam(self):
        self.image_in.stop_webcam()

    def display_image(self, img):
        self.ui.img_output.setPixmap(QPixmap.fromImage(img))

    def update_status(self, message):
        # Thêm một item mới vào model của QListView
        item = QStandardItem(message)
        self.model.insertRow(0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwin = ConsoleMainWindow()
    mainwin.show()
    sys.exit(app.exec_())
