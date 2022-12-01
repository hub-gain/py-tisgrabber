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


def declare_functions(ic):
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

    ic.IC_OpenVideoCaptureDevice.restype = c_int
    ic.IC_OpenVideoCaptureDevice.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_CloseVideoCaptureDevice.restype = None
    ic.IC_CloseVideoCaptureDevice.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetDeviceName.restype = c_char_p
    ic.IC_GetDeviceName.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetVideoFormatWidth.restype = c_int
    ic.IC_GetVideoFormatWidth.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetVideoFormatHeight.restype = c_int
    ic.IC_GetVideoFormatHeight.argtypes = (POINTER(HGRABBER),)

    ic.IC_SetFormat.restype = c_int
    ic.IC_SetFormat.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetFormat.restype = c_int
    ic.IC_GetFormat.argtypes = (POINTER(HGRABBER),)

    ic.IC_SetVideoFormat.restype = c_int
    ic.IC_SetVideoFormat.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_SetVideoNorm.restype = c_int
    ic.IC_SetVideoNorm.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_SetInputChannel.restype = c_int
    ic.IC_SetInputChannel.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_StartLive.restype = c_int
    ic.IC_StartLive.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_PrepareLive.restype = c_int
    ic.IC_PrepareLive.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SuspendLive.restype = c_int
    ic.IC_SuspendLive.argtypes = (POINTER(HGRABBER),)

    ic.IC_StopLive.restype = None
    ic.IC_StopLive.argtypes = (POINTER(HGRABBER),)

    ic.IC_IsCameraPropertyAvailable.restype = c_int
    ic.IC_IsCameraPropertyAvailable.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SetCameraProperty.restype = c_int
    ic.IC_SetCameraProperty.argtypes = (POINTER(HGRABBER), c_int, POINTER(c_long))

    ic.IC_CameraPropertyGetRange.restype = c_int
    ic.IC_CameraPropertyGetRange.argtypes = (
        POINTER(HGRABBER),
        c_int,
        POINTER(c_long),
        POINTER(c_long),
    )

    ic.IC_GetCameraProperty.restype = c_int
    ic.IC_GetCameraProperty.argtypes = (POINTER(HGRABBER), c_int, c_int)

    ic.IC_EnableAutoCameraProperty.restype = c_int
    ic.IC_EnableAutoCameraProperty.argtypes = (POINTER(HGRABBER), c_int, c_int)

    ic.IC_IsCameraPropertyAutoAvailable.restype = c_int
    ic.IC_IsCameraPropertyAutoAvailable.argtypes = (POINTER(HGRABBER), c_int, c_int)

    ic.IC_GetAutoCameraProperty.restype = c_int
    ic.IC_GetAutoCameraProperty.argtypes = (POINTER(HGRABBER), c_int, POINTER(c_int))

    ic.IC_IsVideoPropertyAvailable.restype = c_int
    ic.IC_IsVideoPropertyAvailable.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_VideoPropertyGetRange.restype = c_int
    ic.IC_VideoPropertyGetRange.argtypes = (
        POINTER(HGRABBER),
        c_int,
        POINTER(c_long),
        POINTER(c_long),
    )

    ic.IC_IsVideoPropertyAutoAvailable.restype = c_int
    ic.IC_IsVideoPropertyAutoAvailable.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetAutoVideoProperty.restype = c_int
    ic.IC_GetAutoVideoProperty.argtypes = (POINTER(HGRABBER), c_int, POINTER(c_int))

    ic.IC_SetVideoProperty.restype = c_int
    ic.IC_SetVideoProperty.argtypes = (POINTER(HGRABBER), c_int, c_long)

    ic.IC_EnableAutoVideoProperty.restype = c_int
    ic.IC_EnableAutoVideoProperty.argtypes = (POINTER(HGRABBER), c_int, c_int)

    ic.IC_GetImageDescription.restype = c_int
    ic.IC_GetImageDescription.argtypes = (
        POINTER(HGRABBER),
        POINTER(c_long),
        POINTER(c_long),
        POINTER(c_int),
        POINTER(c_int),
    )

    ic.IC_SnapImage.restype = c_int
    ic.IC_SnapImage.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SaveImage.restype = c_int
    ic.IC_SaveImage.argtypes = (POINTER(HGRABBER), c_char_p, c_int, c_long)

    ic.IC_GetImagePtr.restype = POINTER(c_void_p)
    ic.argtypes = (POINTER(HGRABBER),)

    ic.IC_SetHWnd.restype = c_int
    ic.IC_SetHWnd.argtypes = (POINTER(HGRABBER), c_int)

    # NOTE: returns wrong number according to py-ic-imaging-control
    ic.IC_GetSerialNumber.restype = None
    ic.IC_GetSerialNumber.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_ListDevices.restype = c_int
    ic.IC_ListDevices.argtypes = (POINTER(HGRABBER), POINTER((c_char * 20) * 40), c_int)

    ic.IC_ListVideoFormats.restype = c_int
    ic.IC_ListVideoFormats.argtypes = (
        POINTER(HGRABBER),
        POINTER((c_char * 40) * 80),
        c_int,
    )

    ic.IC_GetDeviceCount.restype = c_int
    ic.IC_GetDeviceCount.argtypes = None

    ic.IC_GetDevice.restype = c_char_p
    ic.IC_GetDevice.argtypes = (c_int,)

    ic.IC_GetUniqueNamefromList.restype = c_char_p
    ic.IC_GetUniqueNamefromList.argtypes = (c_int,)

    ic.IC_GetInputChannelCount.restype = c_int
    ic.IC_GetInputChannelCount.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetInputChannel.restype = c_char_p
    ic.IC_GetInputChannel.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetVideoNormCount.restype = c_int
    ic.IC_GetVideoNormCount.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetVideoNorm.restype = c_char_p
    ic.IC_GetVideoNorm.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetVideoFormatCount.restype = c_int
    ic.IC_GetVideoFormatCount.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetVideoFormat.restype = c_char_p
    ic.IC_GetVideoFormat.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SaveDeviceStateToFile.restype = c_int
    ic.IC_SaveDeviceStateToFile.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_LoadDeviceStateFromFile.restype = POINTER(HGRABBER)
    ic.IC_LoadDeviceStateFromFile.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_OpenDevByDisplayName.restype = c_int
    ic.IC_OpenDevByDisplayName.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_GetDisplayName.restype = c_int
    ic.IC_GetDisplayName.argtypes = (POINTER(HGRABBER), c_char_p, c_int)

    ic.IC_OpenDevByUniqueName.restype = c_int
    ic.IC_OpenDevByUniqueName.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_GetUniqueName = c_int
    ic.IC_GetUniqueName.argtypes = (POINTER(HGRABBER), c_char_p, c_int)

    ic.IC_IsDevValid.restype = c_int
    ic.IC_IsDevValid.argtypes = (POINTER(HGRABBER),)

    ic.IC_ShowPropertyDialog.restype = c_int
    ic.IC_ShowPropertyDialog.argtypes = (POINTER(HGRABBER),)

    ic.IC_ShowDeviceSelectionDialog.restype = POINTER(HGRABBER)
    ic.IC_ShowDeviceSelectionDialog.argtypes = (POINTER(HGRABBER),)

    ic.IC_IsTriggerAvailable.restype = c_int
    ic.IC_IsTriggerAvailable.argtypes = (POINTER(HGRABBER),)

    ic.IC_EnableTrigger.restype = c_int
    ic.IC_EnableTrigger.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_RemoveOverlay.restype = None
    ic.IC_RemoveOverlay.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_MsgBox.restype = None
    ic.IC_MsgBox.argtypes = (c_char_p, c_char_p)

    ic.FRAMEREADYCALLBACK = CFUNCTYPE(
        c_void_p,
        POINTER(HGRABBER),
        POINTER(c_ubyte),
        c_ulong,
        py_object,
    )

    ic.DEVICELOSTCALLBACK = CFUNCTYPE(c_void_p, POINTER(HGRABBER), py_object)

    ic.IC_SetFrameReadyCallback.argtypes = (
        POINTER(HGRABBER),
        ic.FRAMEREADYCALLBACK,
        py_object,
    )
    ic.IC_SetCallbacks.argtypes = (
        POINTER(HGRABBER),
        ic.FRAMEREADYCALLBACK,
        py_object,
        ic.DEVICELOSTCALLBACK,
        py_object,
    )

    ic.IC_SetContinuousMode.restype = c_int
    ic.IC_SetContinuousMode.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SignalDetected.restype = c_int
    ic.IC_SignalDetected.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetTriggerModes.restype = c_int
    ic.IC_GetTriggerModes.argtypes = (
        POINTER(HGRABBER),
        POINTER((c_char * 20) * 10),
        c_int,
    )

    ic.IC_SetTriggerMode.restype = c_int
    ic.IC_SetTriggerMode.argtypes = (POINTER(HGRABBER), c_char_p)

    ic.IC_SetTriggerPolarity.restype = c_int
    ic.IC_SetTriggerPolarity.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetExpRegValRange.restype = c_int
    ic.IC_GetExpRegValRange.argtypes = (
        POINTER(HGRABBER),
        POINTER(c_long),
        POINTER(c_long),
    )

    ic.IC_GetExpRegVal.restype = c_int
    ic.IC_GetExpRegVal.argtypes = (POINTER(HGRABBER), POINTER(c_long))

    ic.IC_SetExpRegVal.restype = c_int
    ic.IC_SetExpRegVal.argtypes = (POINTER(HGRABBER), c_long)

    ic.IC_EnableExpRegValAuto.restype = c_int
    ic.IC_EnableExpRegValAuto.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_GetExpRegValAuto.restype = c_int
    ic.IC_GetExpRegValAuto.argtypes = (POINTER(HGRABBER), POINTER(c_int))

    ic.IC_IsExpAbsValAvailable.restype = c_int
    ic.IC_IsExpAbsValAvailable.argtypes = (POINTER(HGRABBER),)

    ic.IC_GetExpAbsValRange.restype = c_int
    ic.IC_GetExpAbsValRange.argtypes = (
        POINTER(HGRABBER),
        POINTER(c_float),
        POINTER(c_float),
    )

    ic.IC_GetExpAbsVal.restype = c_int
    ic.IC_GetExpAbsVal.argtypes = (POINTER(HGRABBER), c_float)

    ic.IC_GetColorEnhancement.restype = c_int
    ic.IC_GetColorEnhancement.argtypes = (POINTER(HGRABBER), POINTER(c_int))

    ic.IC_SetColorEnhancement.restype = c_int
    ic.IC_SetColorEnhancement.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SoftwareTrigger.restype = c_int
    ic.IC_SoftwareTrigger.argtypes = (POINTER(HGRABBER),)

    ic.IC_SetFrameRate.restype = c_int
    ic.IC_SetFrameRate.argtypes = (POINTER(HGRABBER), c_float)

    ic.IC_GetFrameRate.restype = c_float
    ic.IC_GetFrameRate.argtypes = (POINTER(HGRABBER),)

    ic.IC_FocusOnePush.restype = c_int
    ic.IC_FocusOnePush.argtypes = (POINTER(HGRABBER),)

    ic.IC_ResetProperties.restype = c_int
    ic.IC_ResetProperties.argtypes = (POINTER(HGRABBER),)

    # NOTE: Do not use. For internal purposes only.
    ic.IC_ResetUSBCam.restype = c_int
    ic.IC_ResetUSBCam.argtypes = (POINTER(HGRABBER),)

    ic.IC_QueryPropertySet.restype = c_int
    ic.IC_QueryPropertySet.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_QueryPropertySet.restype = c_int
    ic.IC_QueryPropertySet.argtypes = POINTER(HGRABBER)

    # TODO
    # ic.IC_PropertySet_Set.restype = c_int
    # ic.IC_PropertySet_Set.argtypes = (POINTER(HGRABBER),  ?, ?)

    ic.IC_SetDefaultWindowPosition.restype = c_int
    ic.IC_SetDefaultWindowPosition.argtypes = (POINTER(HGRABBER), c_int)

    ic.IC_SetWindowPosition.restype = c_int
    ic.IC_SetWindowPosition.argtypes = (POINTER(HGRABBER), c_int, c_int, c_int, c_int)

    ic.IC_IsPropertyAvailable.restype = c_int
    ic.IC_IsPropertyAvailable.argtypes = (POINTER(HGRABBER), c_char_p, c_char_p)

    ic.IC_GetPropertyValueRange.restype = c_int
    ic.IC_GetPropertyValueRange.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
        POINTER(c_long),
    )

    ic.IC_GetPropertyValue.restype = c_int
    ic.IC_GetPropertyValue.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
    )

    ic.IC_SetPropertyValue.restype = c_int
    ic.IC_SetPropertyValue.argtypes = (POINTER(HGRABBER), c_char_p, c_int)

    ic.IC_GetPropertyAbsoluteValueRang = c_int
    ic.IC_GetPropertyAbsoluteValueRange.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_float),
        POINTER(c_float),
    )

    ic.IC_GetPropertyAbsoluteValue.restype = c_int
    ic.IC_GetPropertyAbsoluteValue.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_float),
    )

    ic.IC_SetPropertyAbsoluteValue.restype = c_int
    ic.IC_SetPropertyAbsoluteValue.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        c_float,
    )

    ic.IC_IsPropertyAutoAvailable.restype = c_int
    ic.IC_GetPropertySwitch.argtypes = (
        POINTER(HGRABBER),
        c_char_p,
        c_char_p,
        POINTER(c_long),
    )

    ic.IC_SetPropertySwitch.restype = c_int
    ic.IC_SetPropertySwitch.argtypes = (POINTER(HGRABBER), c_char_p, c_char_p, c_int)

    ic.IC_PropertyOnePush.restype = c_int
    ic.IC_PropertyOnePush.argtypes = (POINTER(HGRABBER), c_char_p, c_char_p)

    # TODO
    # ic.IC_GetPropertyMapStrings.restype = c_int
    # ic.IC_GetPropertyMapStrings.argtypes = (
    #   POINTER(HGRABBER),
    #   c_char_p,
    #   c_char_p,
    #   c_int,
    #   ?
    # )
    #
    # ic.IC_SetPropertyMapString.restype = c_int
    # ic.IC_SetPropertyMapString.argtypes = (
    #   POINTER(HGRABBER),
    #   c_char_p,
    #   c_char_p,
    #   c_char_p
    # )

    ic.IC_GetAvailableFrameFilters.restype = c_int
    ic.IC_GetAvailableFrameFilters.argtypes = (
        POINTER(POINTER((c_char * 80) * 40)),
        c_int,
    )

    ic.IC_SetFrameFilter.restype = c_int
    ic.IC_CreateFrameFilter.argtypes = (c_char_p, POINTER(HFRAMEFILTER))

    ic.IC_DeleteFrameFilter.restype = None
    ic.IC_DeleteFrameFilter.argtypes = (POINTER(HFRAMEFILTER),)

    ic.IC_FrameFilterShowDialog.restype = c_int
    ic.IC_FrameFilterShowDialog.argtypes = (POINTER(HFRAMEFILTER),)

    ic.IC_FrameFilterGetParameter.restype = c_int
    ic.IC_FrameFilterGetParameter.argtypes = (POINTER(HFRAMEFILTER), c_char_p, c_void_p)

    ic.IC_FrameFilterSetParameterInt.restype = c_int
    ic.IC_FrameFilterSetParameterInt.argtypes = (POINTER(HFRAMEFILTER), c_char_p, c_int)

    ic.IC_FrameFilterSetParameterFloat.restype = c_int
    ic.IC_FrameFilterSetParameterFloat.argtypes = (
        POINTER(HFRAMEFILTER),
        c_char_p,
        c_float,
    )

    ic.IC_FrameFilterSetParameterBoolean.restype = c_int
    ic.IC_FrameFilterSetParameterBoolean.argtypes = (
        POINTER(HFRAMEFILTER),
        c_char_p,
        c_int,
    )

    ic.IC_FrameFilterSetParameterString.restype = c_int
    ic.IC_FrameFilterSetParameterString.argtypes = (
        POINTER(HFRAMEFILTER),
        c_char_p,
        c_char_p,
    )

    ic.IC_FrameFilterDeviceClear.restype = c_int
    ic.IC_FrameFilterDeviceClear.argtypes = (POINTER(HGRABBER),)

    ic.ENUMCODECCB = CFUNCTYPE(c_void_p, c_char_p, py_object)
    ic.IC_enumCodecs.argtypes = (ic.ENUMCODECCB, py_object)

    ic.IC_Codec_Create.restype = POINTER(HCODEC)
    ic.IC_Codec_Create.argtypes = c_char_p

    ic.IC_Codec_Release.restype = None
    ic.IC_Codec_Release.argtypes = (POINTER(HCODEC),)

    ic.IC_Codec_getName.restype = c_int
    ic.IC_Codec_getName.argtypes = (POINTER(HCODEC), c_int, c_char_p)

    ic.IC_Codec_hasDialog.restype = c_int
    ic.IC_Codec_hasDialog.argtypes = (POINTER(HCODEC),)

    ic.IC_Codec_showDialog.restype = c_int
    ic.IC_Codec_showDialog.argtypes = (POINTER(HCODEC),)

    ic.IC_SetCodec.restype = c_int
    ic.IC_SetCodec.argtypes = (POINTER(HGRABBER), POINTER(HCODEC))

    ic.IC_SetAVIFileName.restype = c_int
    ic.IC_SetAVIFileName.argtypes = (POINTER(HGRABBER), c_char_p)
    ic.IC_enableAVICapturePause.restype = c_int
    ic.IC_enableAVICapturePause.argtypes = (POINTER(HGRABBER), c_int)
