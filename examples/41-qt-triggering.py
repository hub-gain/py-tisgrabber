import sys
from ctypes import Structure

import cv2
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)

from tisgrabber.cam import Camera
from tisgrabber.wrapper import ImageControl

ic = ImageControl()


class CallbackPayload(Structure):
    new_image_ready = pyqtSignal(object)
    image_data = None

    def __init__(self, index: int):
        self.index = index
        print(f"CallbackPayload {index} created")


def frame_ready_callback(grabber, ptr, n_frame, data: CallbackPayload):
    print(f"Frame ready callback {data.index}")
    data.image_data = cameras[data.index].get_image_data()
    # data.new_image_ready.emit(data.image_data)


frame_ready_callback_pointer = ic.create_frame_ready_callback(frame_ready_callback)


def on_close_button_clicked():
    for cam in cameras:
        if cam is not None:
            cam.stop_live()
    app.quit()


def on_camera_selection_clicked(index):
    print(f"Camera {index} clicked")
    grabber = ic.show_device_selection_dialog()
    if ic.is_dev_valid(grabber):
        cam = Camera(grabber)
        cam.set_frame_ready_callback(
            frame_ready_callback_pointer,
            callback_payloads[index],
        )
        cam.set_window_handle(video_widgets[index].winId())
        cam.set_continuous_mode(False)
        cam.start_live()
        cameras[index] = cam


def on_camera_properties_clicked(index):
    if cameras[index] is not None:
        cameras[index].show_property_dialog()
    else:
        on_camera_selection_clicked(index)


def on_new_image(payload: CallbackPayload):
    print(f"New image received from camera {payload.index}")
    gray = cv2.cvtColor(payload.image_data, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(gray)
    brightness_bar[payload.index].setValue(int(mean[0]))


if __name__ == "__main__":
    n_cameras = max(ic.get_device_count(), 1)
    cameras = n_cameras * [None]

    app = QApplication(sys.argv)

    main_window = QMainWindow()
    main_window.resize(1280, 480)
    main_window.move(300, 300)
    main_window.setWindowTitle("Trigger Demo")

    main_menu = main_window.menuBar()
    file_menu = main_menu.addMenu("&File")

    exit_action = QAction("&Exit", app)
    exit_action.setStatusTip("Exit program")
    exit_action.triggered.connect(on_close_button_clicked)
    file_menu.addAction(exit_action)

    camera_menu = main_menu.addMenu("&Cameras")
    property_menu = main_menu.addMenu("&Properties")
    callback_payloads = []
    for i in range(n_cameras):
        device_selection_action = QAction(f"&Select {i}", app)
        device_selection_action.triggered.connect(
            lambda clicked, index=i: on_camera_selection_clicked(index)
        )
        camera_menu.addAction(device_selection_action)

        dev_property_action = QAction(f"&Camera {i}", app)
        dev_property_action.triggered.connect(
            lambda clicked, index=i: on_camera_properties_clicked(index)
        )
        property_menu.addAction(dev_property_action)

        callback_payloads.append(CallbackPayload(i))

    main_widget = QWidget()

    video_widgets = []
    brightness_bars = []
    outer_hbox_layout = QHBoxLayout()
    for _ in range(n_cameras):
        inner_vbox_layout = QVBoxLayout()
        video_widget = QWidget()
        inner_vbox_layout.addWidget(video_widget)

        brightness_bar = QProgressBar()
        brightness_bar.setRange(0, 256)
        brightness_bar.setValue(128)
        inner_vbox_layout.addWidget(brightness_bar)

        outer_hbox_layout.addLayout(inner_vbox_layout)
        video_widgets.append(video_widget)
        brightness_bars.append(brightness_bar)
    main_widget.setLayout(outer_hbox_layout)
    main_window.setCentralWidget(main_widget)

    main_window.show()

    app.exec()
