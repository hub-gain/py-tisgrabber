from ctypes import POINTER, Structure, c_char, c_int, c_void_p


class HGRABBER(Structure):
    """
    This class is used to handle the pointer to the internal Grabber class, which
    contains the camera. A pointer to this class is used by tisgrabber DLL.
    """

    _fields_ = [("unused", c_int)]


class HCODEC(Structure):
    """
    This class is used to handle the pointer to the internal codec class for AVI capture
    A pointer to this class is used by tisgrabber DLL.
    """

    _fields_ = [("unused", c_int)]


class FILTERPARAMETER(Structure):
    """
    This class implements the structure of a frame filter parameter used by the
    HFRAMEFILTER class
    """

    _fields_ = [("Name", c_char * 30), ("Type", c_int)]


class HFRAMEFILTER(Structure):
    """
    This class implements the structure of a frame filter used by the tisgrabber.dll.
    """

    _fields_ = [
        ("pFilter", c_void_p),
        ("bHasDialog", c_int),
        ("ParameterCount", c_int),
        ("Parameters", POINTER(FILTERPARAMETER)),
    ]
