from tisgrabber.wrapper import ImageControl

ic = ImageControl()

n_devices = ic.get_device_count()

for i in range(n_devices):
    print(f"Device {i}: {ic.get_device(i)}")
    print("Unique name:", ic.get_unique_name_from_list(i))

if input("Type y if you want to open live videos for all devices: ").lower() == "y":
    try:
        grabbers = []
        for i in range(n_devices):
            grabber = ic.create_grabber()
            unique_name = ic.get_unique_name_from_list(i)
            ic.open_device_by_unique_name(grabber, unique_name)
            grabbers.append(grabber)
            print(f"Opened device {i}: {unique_name}")

        for grabber in grabbers:
            if ic.is_device_valid(grabber):
                ic.start_live(grabber)

        ic.msg_box("Stop'em all!", "Simple Live Video")

        for grabber in grabbers:
            if ic.is_device_valid(grabber):
                ic.stop_live(grabber)

    finally:
        for grabber in grabbers:
            if ic.is_device_valid(grabber):
                ic.release_grabber(grabber)
