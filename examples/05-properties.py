from tisgrabber.wrapper import ImageControl

ic = ImageControl()
grabber = ic.show_device_selection_dialog()

state = {True: "on", False: "off"}

if ic.is_device_valid(grabber):
    # Turn auto exposure on
    ic.set_property_switch(grabber, "Exposure", "Auto", True)
    on = ic.get_property_switch(grabber, "Exposure", "Auto")
    print(f"Automatic exposure is {state[on]}.")

    # Turn auto exposure off
    ic.set_property_switch(grabber, "Exposure", "Auto", False)
    on = ic.get_property_switch(grabber, "Exposure", "Auto")
    print(f"Automatic exposure is {state[on]}.")

    # Set exposure to 30 ms or its closest possible value
    ic.set_property_absolute_value(grabber, "Exposure", "Value", 0.03)
    value = ic.get_property_absolute_value(grabber, "Exposure", "Value")
    print(f"Exposure is {1e3 * value} ms.")

    # Query possible exposure values
    min_, max_ = ic.get_property_absolute_value_range(grabber, "Exposure", "Value")
    print(f"Exposure can be set between {1e3 * min_} and {1e3 * max_} ms.")

else:
    ic.msg_box("No device opened", "Setting and getting properties")
ic.release_grabber(grabber)
