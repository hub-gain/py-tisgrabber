from ctypes import Structure
from time import sleep

from tisgrabber.wrapper import HGRABBER, ImageControl


class DeviceLostCallbackData(Structure):
    """Example for user data passed to the callback function."""

    def __init__(self):
        self.device_name = ""
        self.connected = False


def device_lost_callback(grabber: HGRABBER, data: Structure):
    """Example for a device lost callback function."""
    data.connected = False
    print(f"Connection to {data.device_name} lost.")


def frame_ready_callback(grabber: HGRABBER, n_frame: int, data: Structure):
    """This example function does nothing."""
    pass


ic = ImageControl()

device_lost_data = DeviceLostCallbackData()
grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    device_lost_data.device_name = ic.get_device_name(grabber)
    device_lost_data.connected = True

    ic.set_callbacks(
        grabber, frame_ready_callback, None, device_lost_callback, device_lost_data
    )
    ic.start_live()
    while device_lost_data.connected:
        print("Disconnect the camera now.")
        sleep(1)
    ic.IC_StopLive(grabber)

else:
    ic.msg_box("No device opened", "Device Lost Callback")
ic.release_grabber(grabber)
