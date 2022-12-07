from tisgrabber.enums import CameraProperty
from tisgrabber.wrapper import ImageControl

ic = ImageControl()
grabber = ic.show_device_selection_dialog()

state = {True: "on", False: "off"}

if ic.is_dev_valid(grabber):
    # Turn auto exposure on
    if ic.is_camera_property_available(grabber, CameraProperty.EXPOSURE):
        print("Exposure is available.")

    if ic.is_camera_property_auto_available(grabber, CameraProperty.EXPOSURE):
        print("Automatic exposure is available.")

else:
    ic.msg_box("No device opened.", "Setting and getting properties")
ic.release_grabber(grabber)
