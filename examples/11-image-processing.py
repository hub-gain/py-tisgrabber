import matplotlib.pyplot as plt

from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()
try:

    if ic.is_dev_valid(grabber):
        ic.start_live(grabber)
        key = ""
        while key != "q":
            print("p: Process an image")
            print("q: End program")
            key = input("Enter your choice: ")
            if key == "p":
                ic.snap_image(grabber, 2000)
                print("Image snapped.")
                image = ic.get_image_data(grabber)
                print("Image data retrieved.")

                plt.imshow(image)
                plt.show()

        ic.stop_live(grabber)
    else:
        ic.msg_box("No device opened", "Simple Live Video")
finally:
    ic.release_grabber(grabber)
