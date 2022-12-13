import ctypes
from pathlib import Path
from typing import Any, Callable, Optional, Union

import numpy as np

from .enums import CameraProperty, ImageFileType, VideoProperty
from .exceptions import (
    IC_ERROR,
    IC_NO_HANDLE,
    IC_NO_PROPERTYSET,
    IC_NOT_AVAILABLE,
    IC_NOT_IN_LIVEMODE,
    IC_SUCCESS,
    ICError,
    NoHandleError,
    NoPropertySetError,
    NotAvailableError,
    NotInLivemodeError,
    check_device_handle_error_code,
    check_property_error_code,
)
from .tisgrabber import HCODEC, HFRAMEFILTER, HGRABBER, load_library

FilePath = Union[str, Path]
FrameReadyCallbackFunction = Callable[
    [HGRABBER, ctypes.pointer, int, ctypes.Structure], None
]
DeviceLostCallbackFunction = Callable[[HGRABBER, ctypes.Structure], None]


class ImageControl:
    def __init__(self, lib_path=None):
        self._ic = load_library(lib_path)
        err = self._ic.IC_InitLibrary()
        if err == IC_ERROR:
            raise ICError("Failed to initialize ImageControl library")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_library()

    def create_grabber(self) -> HGRABBER:
        return self._ic.IC_CreateGrabber()

    def release_grabber(self, grabber: HGRABBER) -> None:
        self._ic.IC_ReleaseGrabber(grabber)

    def close_library(self) -> None:
        self._ic.IC_CloseLibrary()

    def open_video_capture_device(self, grabber: HGRABBER, device_name: str) -> None:
        err = self._ic.IC_OpenVideoCaptureDevice(grabber, device_name.encode("utf-8"))
        if err == IC_ERROR:
            raise ICError("Failed to open video capture device")

    def close_video_capture_device(self, grabber: HGRABBER) -> None:
        self._ic.IC_CloseVideoCaptureDevice(grabber)

    def get_device_name(self, grabber: HGRABBER) -> str:
        return self._ic.IC_GetDeviceName(grabber).decode("utf-8")

    # def get_video_format_width()

    # def get_video_format_height()

    # def set_format()

    # def get_format()

    def set_video_format(self, grabber: HGRABBER, format: str) -> None:
        err = self._ic.IC_SetVideoFormat(grabber, format.encode("utf-8"))
        if err == IC_ERROR:
            raise ICError(f"Failed to set video format to '{format}'")

    # def set_video_norm()

    # def set_input_channel()

    def start_live(self, grabber: HGRABBER) -> None:
        return self._ic.IC_StartLive(grabber, 1)

    # def prepare_live()

    # def suspend_live()

    def stop_live(self, grabber: HGRABBER) -> None:
        return self._ic.IC_StopLive(grabber)

    def is_camera_property_available(self, grabber, prop: CameraProperty) -> bool:
        return bool(self._ic.IC_IsCameraPropertyAvailable(grabber, prop.value))

    def set_camera_property(
        self, grabber: HGRABBER, prop: CameraProperty, value: int
    ) -> None:
        err = self._ic.IC_SetCameraProperty(
            grabber, ctypes.c_int(prop.value), ctypes.c_int(value)
        )
        if err == IC_ERROR:
            raise ICError("An error occurred while setting camera property.")

    def camera_property_get_range(
        self, grabber: HGRABBER, prop: CameraProperty
    ) -> tuple[int, int]:
        min_ = ctypes.c_long()
        max_ = ctypes.c_long()
        err = self._ic.IC_CameraPropertyGetRange(
            grabber,
            ctypes.c_int(prop.value),
            ctypes.byref(min_),
            ctypes.byref(max_),
        )
        if err == IC_SUCCESS:
            raise ICError("An error occurred while getting camera property range.")
        return min_.value, max_.value

    def get_camera_property(self, grabber: HGRABBER, prop: CameraProperty) -> int:
        value = ctypes.c_long()
        err = self._ic.IC_GetCameraProperty(
            grabber, ctypes.c_int(prop.value), ctypes.byref(value)
        )
        if err == IC_ERROR:
            raise ICError("An error occurred while getting camera property.")
        return value.value

    def enable_auto_camera_property(
        self, grabber: HGRABBER, prop: CameraProperty, enable: bool
    ) -> None:
        err = self._ic.IC_EnableAutoCameraProperty(grabber, prop.value, int(enable))
        if err == IC_ERROR:
            raise ICError("An error occurred while enabling auto camera property.")

    def is_camera_property_auto_available(
        self, grabber: HGRABBER, prop: CameraProperty
    ) -> bool:
        # NOTE: explicit conversion to c_int is necessary here
        err = self._ic.IC_IsCameraPropertyAutoAvailable(
            grabber, ctypes.c_int(prop.value)
        )
        check_property_error_code(err)
        return bool(err)

    def get_auto_camera_property(self, grabber: HGRABBER, prop: CameraProperty) -> bool:
        value = ctypes.c_int()
        err = self._ic.IC_GetAutoCameraProperty(
            grabber, prop.value, ctypes.byref(value)
        )
        if err != IC_SUCCESS:
            raise ICError(f"Error {err} occurred while getting auto camera value.")
        return bool(value.value)

    def is_video_property_available(self, grabber, prop: VideoProperty) -> bool:
        return bool(self._ic.IC_IsVideoPropertyAvailable(grabber, prop.value))

    def video_property_get_range(
        self, grabber: HGRABBER, prop: VideoProperty
    ) -> tuple[int, int]:
        min_ = ctypes.c_long()
        max_ = ctypes.c_long()
        err = self._ic.IC_VideoPropertyGetRange(
            grabber,
            prop.value,
            ctypes.byref(min_),
            ctypes.byref(max_),
        )
        if err != IC_SUCCESS:
            raise ICError(f"Error {err} occurred while getting video property range.")
        return min_.value, max_.value

    def get_video_property(self, grabber: HGRABBER, prop: VideoProperty) -> int:
        value = ctypes.c_long()
        err = self._ic.IC_GetVideoProperty(grabber, prop.value, ctypes.byref(value))
        if err != IC_SUCCESS:
            raise ICError(f"Error {err} occurred while getting video property.")
        return value.value

    def is_video_property_auto_available(
        self, grabber: HGRABBER, prop: VideoProperty
    ) -> bool:
        return bool(
            self._ic.IC_IsVideoPropertyAutoAvailable(grabber, ctypes.c_int(prop.value))
        )

    def get_auto_video_property(self, grabber: HGRABBER, prop: VideoProperty) -> bool:
        value = ctypes.c_int()
        err = self._ic.IC_GetAutoVideoProperty(grabber, prop.value, ctypes.byref(value))
        if err == IC_ERROR:
            raise ICError("An error occurred while getting auto video value.")
        return bool(value.value)

    def set_video_property(
        self, grabber: HGRABBER, prop: VideoProperty, value: int
    ) -> None:
        err = self._ic.IC_SetVideoProperty(grabber, prop.value, value)
        if err == IC_ERROR:
            raise ICError("Error occurred while setting video property.")

    def enable_auto_video_property(
        self, grabber: HGRABBER, prop: VideoProperty, enable: bool
    ) -> None:
        err = self._ic.IC_EnableAutoVideoProperty(grabber, prop.value, int(enable))
        if err == IC_ERROR:
            raise ICError("An error occurred while enabling auto video property.")

    def get_image_description(self, grabber: HGRABBER) -> tuple[int, int, int, int]:
        width = ctypes.c_long()
        height = ctypes.c_long()
        bits_per_pixel = ctypes.c_int()
        color_format = ctypes.c_int()

        err = self._ic.IC_GetImageDescription(
            grabber, width, height, bits_per_pixel, color_format
        )
        if err == IC_ERROR:
            raise ICError("An error occurred while getting image description.")
        return (width.value, height.value, bits_per_pixel.value, color_format.value)

    def snap_image(self, grabber: HGRABBER, timeout: int = 1000) -> None:
        err = self._ic.IC_SnapImage(grabber, timeout)
        if err == IC_NOT_IN_LIVEMODE:
            raise NotInLivemodeError("The camera is not in live mode.")
        if err == IC_ERROR:
            raise ICError("An error occurred while snapping the image.")

    def save_image(
        self,
        grabber: HGRABBER,
        filename: FilePath,
        format: ImageFileType = ImageFileType.JPEG,
        quality: int = 100,
    ) -> None:
        err = self._ic.IC_SaveImage(
            grabber, str(filename).encode("utf-8"), format.value, quality
        )
        if err == IC_ERROR:
            raise ICError("An error occurred while saving the image.")

    def _get_image_ptr(self, grabber: HGRABBER):
        return self._ic.IC_GetImagePtr(grabber)

    def get_image_data(self, grabber: HGRABBER) -> np.ndarray:
        width, height, bits_per_pixel, _ = self.get_image_description(grabber)
        buffer_size = width * height * bits_per_pixel

        image_ptr = self._get_image_ptr(grabber)
        image_data = ctypes.cast(
            image_ptr, ctypes.POINTER(ctypes.c_ubyte * buffer_size)
        )

        image = np.ndarray(
            buffer=image_data.contents,
            dtype=np.uint8,
            shape=(height, width, bits_per_pixel // 8),
        )

        return image

    # def set_hwnd()

    # def get_serial_number()

    # def list_devices()

    # def list_video_formats()

    def get_device_count(self) -> int:
        return self._ic.IC_GetDeviceCount()

    def get_device(self, index: int) -> str:
        device = self._ic.IC_GetDevice(index)
        if device:
            device = device.decode("utf-8")
        return device

    def get_unique_name_from_list(self, index: int) -> str:
        unique_name = self._ic.IC_GetUniqueNamefromList(index)
        if unique_name:
            unique_name = unique_name.decode("utf-8")
        return unique_name

    # def get_input_channel_count()

    # def get_input_channel()

    # def get_video_norm_count()

    # def get_video_norm()

    # def get_video_format_count()

    def get_video_format(self, grabber: HGRABBER) -> str:
        return self._ic.IC_GetVideoFormat(grabber).decode("utf-8")

    def save_device_state_to_file(self, grabber: HGRABBER, file_path: FilePath) -> None:
        err = self._ic.IC_SaveDeviceStateToFile(grabber, str(file_path).encode("utf-8"))
        if err == IC_ERROR:
            raise ICError("Failed to save device state to file")

    def load_device_state_from_file(
        self, grabber: HGRABBER, file_path: FilePath
    ) -> HGRABBER:
        return self._ic.IC_LoadDeviceStateFromFile(
            grabber, str(file_path).encode("utf-8")
        )

    # def open_dev_by_display_name()

    # def get_display_name()

    def open_dev_by_unique_name(self, grabber: HGRABBER, unique_name: str) -> None:
        self._ic.IC_OpenDevByUniqueName(grabber, unique_name.encode("utf-8"))

    # def get_unique_name()

    def is_dev_valid(self, grabber: HGRABBER) -> bool:
        return bool(self._ic.IC_IsDevValid(grabber))

    def show_property_dialog(self, grabber: HGRABBER) -> None:
        _ = self._ic.IC_ShowPropertyDialog(grabber)

    def show_device_selection_dialog(
        self, grabber: Optional[HGRABBER] = None
    ) -> HGRABBER:
        return self._ic.IC_ShowDeviceSelectionDialog(grabber)

    def is_trigger_available(self, grabber: HGRABBER) -> bool:
        err = self._ic.IC_IsTriggerAvailable(grabber)
        check_device_handle_error_code(err)
        return bool(err)

    def enable_trigger(self, grabber: HGRABBER, enable: bool) -> None:
        err = self._ic.IC_EnableTrigger(grabber, int(enable))
        if err == IC_NOT_AVAILABLE:
            raise NotAvailableError("Device does not support triggering.")
        if err == IC_NO_PROPERTYSET:
            raise NoPropertySetError("Failed to query the property set of the device.")

    # def remove_overlay()

    def msg_box(self, msg: str, title: str) -> None:
        return self._ic.IC_MsgBox(msg.encode("utf-8"), title.encode("utf-8"))

    def set_frame_ready_callback(
        self,
        grabber: HGRABBER,
        callback: Callable[[HGRABBER, Any, int, ctypes.Structure], None],
        data: ctypes.Structure,
    ) -> None:
        self._ic.IC_SetFrameReadyCallback(
            grabber, self._ic.FRAMEREADYCALLBACK(callback), data
        )

    def set_callbacks(
        self,
        grabber: HGRABBER,
        frame_ready_callback: FrameReadyCallbackFunction,
        frame_ready_data: ctypes.Structure,
        device_lost_callback: DeviceLostCallbackFunction,
        device_lost_data: ctypes.Structure,
    ) -> None:
        self._ic.IC_SetCallbacks(
            grabber,
            self._ic.FRAMEREADYCALLBACK(frame_ready_callback),
            frame_ready_data,
            self._ic.DEVICELOSTCALLBACK(device_lost_callback),
            device_lost_data,
        )

    def set_continious_mode(self, grabber: HGRABBER, enable: bool) -> None:
        err = self._ic.IC_SetContinuousMode(grabber, int(enable))
        if err == IC_NOT_IN_LIVEMODE:
            raise NotInLivemodeError(
                "Device is currently streaming, so setting continious mode failed."
            )
        if err == IC_NO_HANDLE:
            raise NoHandleError("Device handle is invalid.")

    def signal_detected(self, grabber: HGRABBER) -> bool:
        err = bool(self._ic.IC_SignalDetected(grabber))
        check_device_handle_error_code(err)
        if err == IC_NOT_IN_LIVEMODE:
            raise NotInLivemodeError("Turn on live mode first.")
        if err == IC_NOT_AVAILABLE:
            raise NotAvailableError("Signal detection property is not available.")

    # def get_trigger_modes()

    # def set_trigger_mode()

    # def set_trigger_polarity()

    def get_exp_reg_val_range(self, grabber: HGRABBER) -> tuple[int, int]:
        min_ = ctypes.c_int()
        max_ = ctypes.c_int()
        self._ic.IC_GetExpRegValRange(grabber, ctypes.byref(min_), ctypes.byref(max_))
        return min_.value, max_.value

    def get_exp_reg_val(self, grabber: HGRABBER) -> int:
        value = ctypes.c_long()
        err = self._ic.IC_GetExpRegVal(grabber, value)
        if err != IC_SUCCESS:
            raise ICError("Failed to get exposure register value. Error code: {err}")
        return value.value

    def set_exp_reg_val(self, grabber: HGRABBER, value: int) -> None:
        err = self._ic.IC_SetExpRegVal(grabber, ctypes.c_long(value))
        if err != IC_SUCCESS:
            raise ICError(
                f"Failed to set exposure register value to {value}. Error code: {err}"
            )

    def enable_exp_reg_val_auto(self, grabber: HGRABBER, enable: bool) -> None:
        err = self._ic.IC_EnableExpRegValAuto(grabber, int(enable))
        if err != IC_SUCCESS:
            raise ICError(
                f"Failed to set exposure auto register value. Error code: {err}"
            )

    def get_exp_reg_val_auto(self, grabber: HGRABBER) -> bool:
        value = ctypes.c_int()
        err = self._ic.IC_GetExpRegValAuto(grabber, ctypes.byref(value))
        if err != IC_SUCCESS:
            raise ICError(
                f"Failed to get exposure register value auto. Error code: {err}"
            )
        return bool(value.value)

    def is_exp_abs_val_available(self, grabber: HGRABBER) -> bool:
        err = self._ic.IC_IsExpAbsValAvailable(grabber)
        if err < 0:
            raise ICError(f"Failed to check if property is available. Error {err}.")
        return bool()

    def get_exp_abs_val_range(self, grabber: HGRABBER) -> tuple[float, float]:
        min_ = ctypes.c_float()
        max_ = ctypes.c_float()
        err = self._ic.IC_GetExpAbsValRange(
            grabber, ctypes.byref(min_), ctypes.byref(max_)
        )
        if err != IC_SUCCESS:
            raise ICError(
                f"Failed to get exposure absolute value range. Error code: {err}"
            )
        return min_.value, max_.value

    def get_exp_abs_val(self, grabber: HGRABBER) -> float:
        value = ctypes.c_float()
        err = self._ic.IC_GetExpAbsVal(grabber, ctypes.byref(value))
        if err != IC_SUCCESS:
            raise ICError("Failed to get exposure absolute value. Error code: {err}")
        return value.value

    # def get_color_enhancement()

    # def set_color_enhancement()

    def software_trigger(self, grabber: HGRABBER) -> None:
        err = self._ic.IC_SoftwareTrigger(grabber)
        check_device_handle_error_code(err)
        if err == IC_NOT_AVAILABLE:
            raise NotAvailableError("Software trigger not available for this device.")

    def set_frame_rate(self, grabber: HGRABBER, frame_rate: float) -> None:
        err = self._ic.IC_SetFrameRate(grabber, frame_rate)
        check_device_handle_error_code(err)
        if err == IC_NOT_AVAILABLE:
            raise NotAvailableError(
                "Setting frame rate is not supported by the current device"
            )
        if err == IC_NOT_IN_LIVEMODE:
            raise NotInLivemodeError("Setting frame rate is not possible in live mode")

    def get_frame_rate(self, grabber: HGRABBER) -> float:
        return self._ic.IC_GetFrameRate(grabber)

    # def focus_one_push()

    def print_item_and_element_names(self, grabber: HGRABBER) -> None:
        self._ic.IC_PrintItemAndElementNames(grabber)

    def reset_properties(self, grabber: HGRABBER) -> None:
        err = self._ic.IC_ResetProperties(grabber)
        if err != IC_SUCCESS:
            raise ICError(f"Failed to reset properties. Error code: {err}")

    # def property_set_set()

    # def set_default_window_position()

    # def set_window_position()

    def is_property_available(self, grabber: HGRABBER, prop: str) -> bool:
        err = self._ic.IC_IsPropertyAvailable(grabber, prop.encode("utf-8"))
        check_property_error_code(err)
        return bool(err)

    def get_property_value_range(
        self, grabber: HGRABBER, prop: str, element: str
    ) -> tuple[int, int]:
        min_, max_ = ctypes.c_long(), ctypes.c_long()
        err = self._ic.IC_GetPropertyValueRange(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), min_, max_
        )
        check_property_error_code(err)
        return (min_.value, max_.value)

    def get_property_value(self, grabber: HGRABBER, prop: str, element: str) -> int:
        value = ctypes.c_long()
        err = self._ic.IC_GetPropertyValue(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), value
        )
        check_property_error_code(err)
        return value.value

    def set_property_value(
        self, grabber: HGRABBER, prop: str, element: str, value: int
    ) -> None:
        err = self._ic.IC_SetPropertyValue(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), value
        )
        check_property_error_code(err)

    def get_property_absolute_value_range(
        self, grabber: HGRABBER, prop: str, element: str
    ) -> tuple[float, float]:
        min_, max_ = ctypes.c_float(), ctypes.c_float()
        err = self._ic.IC_GetPropertyAbsoluteValueRange(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), min_, max_
        )
        check_property_error_code(err)
        return (min_.value, max_.value)

    def get_property_absolute_value(
        self, grabber: HGRABBER, prop: str, element: str
    ) -> float:
        value = ctypes.c_float()
        err = self._ic.IC_GetPropertyAbsoluteValue(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), value
        )
        check_property_error_code(err)
        return value.value

    def set_property_absolute_value(
        self, grabber: HGRABBER, prop: str, element: str, value: float
    ) -> None:
        err = self._ic.IC_SetPropertyAbsoluteValue(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), value
        )
        check_property_error_code(err)

    def get_property_switch(self, grabber: HGRABBER, prop: str, element: str) -> bool:
        on = ctypes.c_int()
        err = self._ic.IC_GetPropertySwitch(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), on
        )
        check_property_error_code(err)
        return bool(on.value)

    def set_property_switch(
        self, grabber: HGRABBER, prop: str, element: str, on: bool
    ) -> None:
        err = self._ic.IC_SetPropertySwitch(
            grabber, prop.encode("utf-8"), element.encode("utf-8"), int(on)
        )
        self.check_property_error_code(err)

    def property_one_push(self, grabber: HGRABBER, prop: str) -> None:
        err = self._ic.IC_PropertyOnePush(
            grabber, prop.encode("utf-8"), "One Push".encode("utf-8")
        )
        check_property_error_code(err)

    # def get_property_map_strings()

    # def set_property_map_strings()

    def get_available_frame_filter_count(self):
        return self._ic.IC_GetAvailableFrameFilterCount()

    def get_available_frame_filters(self, filter_count: int) -> list[str]:
        string_buffers = [ctypes.create_string_buffer(50) for _ in range(filter_count)]
        pointers = (ctypes.c_char_p * filter_count)(
            *map(ctypes.addressof, string_buffers)
        )
        self._ic.IC_GetAvailableFrameFilters(pointers, filter_count)
        frame_filters = [string_buffer.value for string_buffer in string_buffers]
        return frame_filters

    def create_frame_filter(self, name: str) -> HFRAMEFILTER:
        filter_handle = HFRAMEFILTER()
        err = self._ic.IC_CreateFrameFilter(name.encode("utf-8"), filter_handle)
        if err == IC_ERROR:
            raise ICError("Frame filter load failed. ")
        return filter_handle

    def add_frame_filter_to_device(
        self, grabber: HGRABBER, filter: HFRAMEFILTER
    ) -> None:
        err = self._ic.IC_AddFrameFilterToDevice(grabber, filter)
        if err == IC_ERROR:
            raise ICError("Adding frame filter failed.")

    # def delete_frame_filter()

    # def frame_filter_show_dialog()

    # def frame_filter_get_parameter()

    def frame_filter_set_parameter_int(
        self, filter: HFRAMEFILTER, param: str, value: int
    ) -> None:
        err = self._ic.IC_FrameFilterSetParameterInt(
            filter, param.encode("utf-8"), value
        )
        check_property_error_code(err)
        if err == IC_ERROR:
            raise ICError("Setting frame filter parameter failed.")

    def frame_filter_set_parameter_float(
        self, filter: HFRAMEFILTER, param: str, value: float
    ) -> None:
        err = self._ic.IC_FrameFilterSetParameterFloat(
            filter, param.encode("utf-8"), value
        )
        check_property_error_code(err)
        if err == IC_ERROR:
            raise ICError("Setting frame filter parameter failed.")

    def frame_filter_set_parameter_boolean(
        self, filter: HFRAMEFILTER, param: str, value: bool
    ) -> None:
        err = self._ic.IC_FrameFilterSetParameterBoolean(
            filter, param.encode("utf-8"), int(value)
        )
        check_property_error_code(err)
        if err == IC_ERROR:
            raise ICError("Setting frame filter parameter failed.")

    def frame_filter_set_parameter_string(
        self, filter: HFRAMEFILTER, param: str, value: str
    ) -> None:
        err = self._ic.IC_FrameFilterSetParameterString(
            filter, param.encode("utf-8"), value
        )
        check_property_error_code(err)
        if err == IC_ERROR:
            raise ICError("Setting frame filter parameter failed.")

    def frame_filter_device_clear(self, grabber: HGRABBER) -> None:
        self._ic.IC_FrameFilterDeviceClear(grabber)

    def get_available_codecs(self) -> list[str]:
        def enum_codec_callback(name, lst):
            lst.append(name.decode("utf-8"))
            return 0

        enum_codec_callback_func = self._ic.ENUMCODECCB(enum_codec_callback)
        codecs = []
        self._ic.IC_enumCodecs(enum_codec_callback_func, codecs)
        return codecs

    def codec_create(self, codec_name: str) -> HCODEC:
        return self._ic.IC_Codec_Create(codec_name.encode("utf-8"))

    # def codec_release()

    # def codec_get_name()

    def codec_has_dialog(self, codec: HCODEC) -> bool:
        return bool(self._ic.IC_Codec_hasDialog(codec))

    def codec_show_dialog(self, codec) -> None:
        self._ic.IC_Codec_showDialog(codec)

    def set_codec(self, grabber: HGRABBER, codec: HCODEC) -> None:
        self._ic.IC_SetCodec(grabber, codec)

    def set_avi_file_name(self, grabber: HGRABBER, filename: FilePath) -> None:
        self._ic.IC_SetAVIFileName(grabber, str(filename).encode("utf-8"))

    def enable_avi_capture_pause(self, grabber: HGRABBER, enable: bool) -> None:
        self._ic.IC_enableAVICapturePause(grabber, int(enable))
