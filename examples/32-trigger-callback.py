# FIXME: Fails with
# tisgrabber.exceptions.PropertyElementNotAvailableError: Requested element is not
# available.

from ctypes import Structure, pointer

from tisgrabber.wrapper import HGRABBER, ImageControl


class CallbackUserData(Structure):
    """Example for user data passed to the callback function."""

    def __init__(self):
        self.unused = ""


def trigger_callback(grabber: HGRABBER, ptr: pointer, n_frame: int, data: Structure):
    """Example for a callback function."""
    image_description = ic.get_image_description(grabber)
    print("Trigger callback called")
    print(f"width: {image_description[0]}")
    print(f"height: {image_description[1]}")
    print(f"bits per pixel: {image_description[2]}")
    print(f"color format: {image_description[3]}")

    _ = ic.get_image_data(grabber)
    print("Image data received.")


ic = ImageControl()
user_data = CallbackUserData()
grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    ic.set_frame_ready_callback(grabber, trigger_callback, user_data)
    ic.set_continious_mode(grabber, False)
    ic.set_property_switch(grabber, "Trigger", "Enable", True)
    ic.start_live(grabber)

    ic.msg_box("Click OK to trigger", "Trigger Callback")
    ic.property_one_push(grabber, "Software Trigger")

    ic.msg_box("Click OK to stop", "Trigger Callback")
    ic.stop_live(grabber)
else:
    ic.msg_box("No device opened", "Simple Live Video")
ic.release_grabber(grabber)
