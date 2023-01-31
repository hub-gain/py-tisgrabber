import sys
from ctypes import Structure, pointer

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from tisgrabber.wrapper import ImageControl

ic = ImageControl()


class CallbackUserData(Structure):
    new_image = pyqtSignal(object)
    image_data = None


def frame_ready_callback(grabber, ptr: pointer, n_frame: int, data: CallbackUserData):
    data.image_data = ic.get_image_data(grabber)
    data.new_image.emit(data)


def on_close_button_clicked():
    app.quit()


def on_camera_selection_clicked(index):
    print(index)


def on_camera_properties_clicked(index):
    print(index)


if __name__ == "__main__":

    n_cameras = ic.get_device_count()
    cameras = []

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.resize(1280, 480)
    main_window.move(300, 300)
    main_window.setWindowTitle("Stereo")

    main_menu = main_window.menuBar()
    file_menu = main_menu.addMenu("&File")

    exit_action = QAction("&Exit", app)
    exit_action.setStatusTip("Exit program")
    exit_action.triggered.connect(on_close_button_clicked)
    file_menu.addAction(exit_action)

    camera_menu = main_menu.addMenu("&Cameras")
    property_menu = main_menu.addMenu("&Properties")
    for i in range(n_cameras):
        dev_selection_action = QAction(f"&Select {i+1}", app)
        dev_selection_action.triggered.connect(lambda: on_camera_selection_clicked(i))
        camera_menu.addAction(dev_selection_action)

        dev_property_action = QAction(f"&Camera {i+1}", app)
        dev_property_action.triggered.connect(lambda: on_camera_properties_clicked(i))
        property_menu.addAction(dev_property_action)

    main_widget = QWidget()

    video_widgets = []
    outer_hbox_layout = QHBoxLayout()
    for _ in range(n_cameras):
        inner_vbox_layout = QVBoxLayout()
        video_widget = QWidget()
        inner_vbox_layout.addWidget(video_widget)
        outer_hbox_layout.addLayout(inner_vbox_layout)

    main_widget.setLayout(outer_hbox_layout)
    main_window.setCentralWidget(main_widget)

    main_window.show()

    app.exec()
