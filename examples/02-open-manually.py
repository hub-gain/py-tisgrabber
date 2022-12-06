from tisgrabber.wrapper import ImageControl

ic = ImageControl()

grabber = ic.create_grabber()
ic.open_video_capture_device(grabber, "DMM 22BUC03-ML")

if ic.is_dev_valid(grabber):
    ic.set_video_format(grabber, "Y800 (744x480)")
    ic.set_frame_rate(grabber, 30.0)
    ic.start_live(grabber)
    ic.msg_box("Click OK to stop", "Simple Live Video")
    ic.stop_live(grabber)
else:
    ic.msg_box("No device opened", "Simple Live Video")
ic.release_grabber(grabber)
