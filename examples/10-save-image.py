from tisgrabber.enums import ImageFileType
from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

if ic.is_dev_valid(grabber):
    try:
        ic.start_live(grabber)
        key = ""
        while key != "q":
            print("s: Save an image")
            print("q: End program")
            key = input("Enter your choice: ")
            if key == "s":
                ic.snap_image(grabber, 2000)
                print("Image snapped.")
                ic.save_image(grabber, "image.png", ImageFileType.JPEG, 90)
                print("Image saved.")
        ic.stop_live(grabber)
    finally:
        ic.release_grabber(grabber)
else:
    ic.msg_box("No device opened.", "Snapping images")
