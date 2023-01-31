from tisgrabber.enums import CameraProperty, VideoProperty
from tisgrabber.wrapper import ImageControl

ic = ImageControl()
grabber = ic.show_device_selection_dialog()

state = {True: "on", False: "off"}

if ic.is_dev_valid(grabber):
    print(ic.is_camera_property_auto_available(grabber, CameraProperty.EXPOSURE))
    print(ic.is_camera_property_auto_available(grabber, CameraProperty.PAN))

    print(ic.is_video_property_auto_available(grabber, VideoProperty.GAMMA))
    print(ic.is_video_property_auto_available(grabber, VideoProperty.GAIN))

else:
    ic.msg_box("No device opened.", "Setting and getting properties")
ic.release_grabber(grabber)
