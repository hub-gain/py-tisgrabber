from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    print("IC_printItemandElementNames does not exist.")
else:
    print("No device opened")

ic.release_grabber(grabber)
