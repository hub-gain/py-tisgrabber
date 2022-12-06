from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.create_grabber()
ic.load_device_state_from_file(grabber, "./device.xml")

if ic.is_dev_valid(grabber):

    ic.start_live(grabber)
    ic.msg_box("Click OK to stop", "Simple Live Video")
    ic.stop_live(grabber)
else:
    ic.msg_box("No device opened", "Simple Live Video")
ic.release_grabber(grabber)
