from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_device_valid(grabber):
    ic.set_property_switch(grabber, "Exposure", "Auto", True)
    on = ic.get_property_switch(grabber, "Exposure", "Auto")
    state = "on" if on else "off"
    print(f"Automatic exposure is {state}.")
else:
    ic.msg_box("No device opened", "Setting and getting properties")
ic.release_grabber(grabber)
