from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    ic.print_item_and_element_names(grabber)
else:
    print("No device opened")

ic.release_grabber(grabber)
