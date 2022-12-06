from ctypes import Structure, pointer

from tisgrabber.wrapper import HGRABBER, ImageControl


class CallbackData(Structure):
    """Example for user data passed to the callback function."""

    def __init__(self):
        self.value_1 = 42
        self.value_2 = 0
        self.camera = None


def frame_callback(grabber: HGRABBER, ptr: pointer, n_frame: int, data: Structure):
    """Example for a callback function."""
    print(f"Callback called, {data.value_1=}")
    data.value_1 += 1


ic = ImageControl()

grabber = ic.show_device_selection_dialog()
data = CallbackData()

if ic.is_dev_valid(grabber):
    ic.set_frame_ready_callback(grabber, frame_callback, data)
    ic.set_continious_mode(grabber, False)
    ic.start_live(grabber)
    ic.msg_box("Click OK to stop", "Callback")
    ic.stop_live(grabber)
else:
    ic.msg_box("No device opened", "Callback")
ic.release_grabber(grabber)
