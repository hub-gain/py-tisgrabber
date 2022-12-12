from tisgrabber.enums import CameraProperty
from tisgrabber.wrapper import ImageControl

ic = ImageControl()
grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    print(ic.camera_property_get_range(grabber, CameraProperty.EXPOSURE))

    ic.set_camera_property(grabber, CameraProperty.EXPOSURE, -6)

else:
    ic.msg_box("No device opened.", "Setting and getting properties")
ic.release_grabber(grabber)
