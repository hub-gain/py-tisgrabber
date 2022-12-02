from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_device_valid(grabber):
    ic.start_live(grabber)
    ic.msg_box("Click OK to stop", "Simple Live Video")
    ic.stop_live(grabber)
else:
    ic.msg_box("No device opened", "Simple Live Video")
ic.release_grabber(grabber)
