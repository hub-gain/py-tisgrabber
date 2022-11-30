from ctypes import (
    CFUNCTYPE,
    POINTER,
    Structure,
    c_char,
    c_char_p,
    c_float,
    c_int,
    c_long,
    c_ubyte,
    c_ulong,
    c_void_p,
    py_object,
)
from enum import Enum


class SinkFormats(Enum):
    Y800 = 0
    RGB24 = 1
    RGB32 = 2
    UYVY = 3
    Y16 = 4


class FRAMEFILTER_PARAM_TYPE(Enum):
    eParamLong = 0
    eParamBoolean = 1
    eParamFloat = 2
    eParamString = 3
    eParamData = 4


ImageFileTypes = {"BMP": 0, "JPEG": 1}

IC_SUCCESS = 1
IC_ERROR = 0
IC_NO_HANDLE = -1
IC_NO_DEVICE = -2
IC_NOT_AVAILABLE = -3
IC_NO_PROPERTYSET = -3
IC_DEFAULT_WINDOW_SIZE_SET = -3
IC_NOT_IN_LIVEMODE = -3
IC_PROPERTY_ITEM_NOT_AVAILABLE = -4
IC_PROPERTY_ELEMENT_NOT_AVAILABLE = -5
IC_PROPERTY_ELEMENT_WRONG_INTERFACE = -6
IC_INDEX_OUT_OF_RANGE = -7
IC_WRONG_XML_FORMAT = -1
IC_WRONG_INCOMPATIBLE_XML = -3
IC_NOT_ALL_PROPERTIES_RESTORED = -4
IC_DEVICE_NOT_FOUND = -5
IC_FILE_NOT_FOUND = 35


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


def declareFunctions(ic):
    """
    Functions returning a HGRABBER Handle must set their restype to POINTER(HGRABBER)

    :param ic: The loaded tisgrabber*.dll
    """
    ic.IC_InitLibrary.restype = c_int
    ic.IC_InitLibrary.argtypes = (c_char_p,)

    ic.IC_CreateGrabber.restype = POINTER(HGRABBER)
    ic.IC_CreateGrabber.argtypes = None

    ic.IC_ReleaseGrabber.restype = None
    ic.IC_ReleaseGrabber.argtypes = (POINTER(HGRABBER),)

    ic.IC_CloseLibrary.restype = None
    ic.IC_CloseLibrary.argtypes = None

    ic.IC_ShowDeviceSelectionDialog.restype = POINTER(HGRABBER)

    ic.IC_LoadDeviceStateFromFile.restype = POINTER(HGRABBER)

    ic.IC_GetPropertyValueRange.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
        POINTER(c_long),
    )

    ic.IC_GetPropertyValue.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
    )

    ic.IC_GetPropertyAbsoluteValue.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_float),
    )

    ic.IC_GetPropertyAbsoluteValueRange.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_float),
        POINTER(c_float),
    )

    ic.IC_GetPropertySwitch.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
    )

    ic.IC_GetImageDescription.argtypes = (
        POINTER(HGRABBER),
        POINTER(c_long),
        POINTER(c_long),
        POINTER(c_int),
        POINTER(c_int),
    )

    ic.IC_GetImagePtr.restype = c_void_p

    ic.IC_SetHWnd.argtypes = (POINTER(HGRABBER), c_int)
    # definition of the frameready callback
    ic.FRAMEREADYCALLBACK = CFUNCTYPE(
        c_void_p,
        POINTER(HGRABBER),
        POINTER(c_ubyte),
        c_ulong,
        py_object,
    )
    ic.DEVICELOSTCALLBACK = CFUNCTYPE(c_void_p, POINTER(HGRABBER), py_object)

    ic.IC_SetFrameReadyCallback.argtypes = [
        POINTER(HGRABBER),
        ic.FRAMEREADYCALLBACK,
        py_object,
    ]
    ic.IC_SetCallbacks.argtypes = [
        POINTER(HGRABBER),
        ic.FRAMEREADYCALLBACK,
        py_object,
        ic.DEVICELOSTCALLBACK,
        py_object,
    ]

    ic.IC_Codec_Create.restype = POINTER(HCODEC)

    ic.ENUMCODECCB = CFUNCTYPE(c_void_p, c_char_p, py_object)
    ic.IC_enumCodecs.argtypes = (ic.ENUMCODECCB, py_object)

    ic.IC_GetDeviceName.restype = c_char_p
    ic.IC_GetDevice.restype = c_char_p
    ic.IC_GetUniqueNamefromList.restype = c_char_p

    ic.IC_CreateFrameFilter.argtypes = (c_char_p, POINTER(HFRAMEFILTER))


def T(instr):
    """
    Helper function
    Encodes the input string to utf-8

    :param instr: Python string to be converted
    :return: converted string
    """
    return instr.encode("utf-8")


def D(instr):
    """
    Helper function
    Decodes instr utf-8

    :param instr: Python string to be converted
    :return: converted string
    """
    return instr.decode("utf-8", "ignore")


def openDevice(ic):
    """
    Helper functions
    Open a camera. If a file with a device state exists, it will be used. If not, the
    device selection dialog is shown and if a valid devices was selected, the device
    state file is created.

    :return: a HGRABBER
    """
    try:
        hGrabber = ic.IC_LoadDeviceStateFromFile(None, T("device.xml"))
        if not ic.IC_IsDevValid(hGrabber):
            hGrabber = ic.IC_ShowDeviceSelectionDialog(None)
    except Exception:
        hGrabber = ic.IC_ShowDeviceSelectionDialog(None)

    if ic.IC_IsDevValid(hGrabber):
        ic.IC_SaveDeviceStateToFile(hGrabber, T("device.xml"))
    return hGrabber
