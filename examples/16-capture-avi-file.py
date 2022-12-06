from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.show_device_selection_dialog()

try:
    if ic.is_dev_valid(grabber):
        codec = ic.codec_create("MJPEG Compressor")
        if ic.codec_has_dialog(codec):
            ic.codec_show_dialog(codec)

        ic.set_codec(grabber, codec)
        ic.set_avi_file_name(grabber, "capture.avi")
        ic.enable_avi_capture_pause(grabber, True)

        ic.start_live(grabber)
        ic.msg_box("Click OK to start capture", "AVI Capture")
        ic.enable_avi_capture_pause(grabber, False)
        ic.msg_box("Click OK to stop capture", "AVI Capture")
        ic.enable_avi_capture_pause(grabber, True)

    else:
        ic.msg_box("No device opened", "Simple Live Video")
finally:
    ic.release_grabber(grabber)
