from time import sleep

from tisgrabber.wrapper import ImageControl

ic = ImageControl()

filter_count = ic.get_available_frame_filter_count()
print(f"{filter_count} frame filters are available.")

filter_list = ic.get_available_frame_filters(filter_count)
print("Available frame filters:")
for filter in filter_list:
    print(f"{filter}")

filter = "Rotate Flip"
filter_handle = ic.create_frame_filter(filter)
print(f"Frame filter '{filter}' loaded. Available parameters are:")
for i in range(filter_handle.ParameterCount):
    print(
        (
            f"Name: {filter_handle.Parameters[i].Name.decode('UTF-8')}, "
            f"Type: {filter_handle.Parameters[i].Type}"
        )
    )

grabber = ic.show_device_selection_dialog()


if ic.is_dev_valid(grabber):
    ic.add_frame_filter_to_device(grabber, filter_handle)
    for angle in [90, 180, 270, 0]:
        ic.frame_filter_set_parameter_int(filter_handle, "Rotation Angle", angle)
        ic.start_live(grabber)
        sleep(2)
        ic.stop_live(grabber)

    ic.start_live(grabber)
    ic.frame_filter_set_parameter_boolean(filter_handle, "Flip H", True)
    sleep(2)

    ic.frame_filter_set_parameter_boolean(filter_handle, "Flip V", True)
    sleep(2)

    ic.frame_filter_set_parameter_boolean(filter_handle, "Flip H", False)
    sleep(2)

    ic.frame_filter_set_parameter_boolean(filter_handle, "Flip V", False)
    sleep(2)
    ic.stop_live(grabber)

else:
    ic.msg_box("No device opened", "Frame Filter")

ic.release_grabber(grabber)
