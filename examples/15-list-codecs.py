from tisgrabber.wrapper import ImageControl

ic = ImageControl()

for codec in ic.get_available_codecs():
    print(codec)
