# NOTE: Not tested, since our camera does not support property "Partial scan"

from time import sleep

from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    try:
        # Set "big" video format
        ic.set_video_format(grabber, "Y800 (744x480)")
        ic.set_frame_rate(grabber, 30.0e-3)

        ic.start_live(grabber)
        ic.msg_box("Click OK to to use a smaller format", "ROI Demo")
        ic.stop_live(grabber)

        # Set a an ROI on the sensor. Make sure, the width and height are valid  for the
        # used camera!
        ic.set_video_format(grabber, "Y800 (320x240)")
        ic.set_frame_rate(grabber, 30.0e-3)

        # Moving the ROI on the sensor need to disable the Partial Scan Auto Center
        # property:
        ic.set_property_switch(grabber, "Partial scan", "Auto-center", False)
        ic.start_live(grabber)

        # Move the ROI on the sensor by x and y coordinates. This can be done,  while
        # the live video is running.
        x = 0
        for y in range(480 - 240):
            ic.set_property_value(grabber, "Partial scan", "X Offset", x)
            ic.set_property_value(grabber, "Partial scan", "Y Offset", y)
            x += 1
            sleep(0.05)

        ic.msg_box("Click to reset to bigger format again", "ROI Demo")
        ic.stop_live(grabber)
        ic.set_video_format(grabber, "Y800 (744x480)")
        ic.set_frame_rate(grabber, 30.0e-3)
        ic.set_property_switch(grabber, "Partial scan", "Auto-center", True)

        ic.start_live(grabber)
        ic.msg_box("Click OK to stop", "ROI Demo")
        ic.stop_live(grabber)

    finally:
        ic.release_grabber(grabber)
else:
    ic.msg_box("No device opened", "ROI Demo")
