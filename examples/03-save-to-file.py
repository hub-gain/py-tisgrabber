from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_device_valid(grabber):
    ic.save_device_state_to_file(grabber, "device.xml")
else:
    ic.msg_box("No device opened", "Failed to save device state.")
ic.release_grabber(grabber)
