import ctypes
from pathlib import Path
from typing import NewType, Optional, Union

from .exceptions import (
    ICError,
    NoDeviceError,
    NoHandleError,
    NotAvailableError,
    NotInLivemodeError,
    PropertyElementNotAvailableError,
    PropertyElementWrongInterfaceError,
    PropertyItemNotAvailableError,
)
from .tisgrabber import (
    IC_ERROR,
    IC_NO_DEVICE,
    IC_NO_HANDLE,
    IC_NOT_AVAILABLE,
    IC_NOT_IN_LIVEMODE,
    IC_PROPERTY_ELEMENT_NOT_AVAILABLE,
    IC_PROPERTY_ELEMENT_WRONG_INTERFACE,
    IC_PROPERTY_ITEM_NOT_AVAILABLE,
    IC_SUCCESS,
    load_library,
)

hGrabber = NewType("hGrabber", int)
FilePath = Union[str, Path]


class ImageControl:
    def __init__(self, lib_path=None):
        self._ic = load_library(lib_path)
        err = self._ic.IC_InitLibrary()
        if err == IC_ERROR:
            raise ICError("Failed to initialize ImageControl library")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ic.IC_CloseLibrary()

    def create_grabber(self) -> hGrabber:
        return self._ic.IC_CreateGrabber()

    def release_grabber(self, grabber: hGrabber) -> None:
        self._ic.IC_ReleaseGrabber(grabber)

    def show_device_selection_dialog(
        self, grabber: Optional[hGrabber] = None
    ) -> hGrabber:
        return self._ic.IC_ShowDeviceSelectionDialog(grabber)

    def is_device_valid(self, grabber: hGrabber) -> bool:
        return bool(self._ic.IC_IsDevValid(grabber))

    def start_live(self, grabber: hGrabber) -> None:
        return self._ic.IC_StartLive(grabber, 1)

    def stop_live(self, grabber: hGrabber) -> None:
        return self._ic.IC_StopLive(grabber)

    def msg_box(self, msg: str, title: str) -> None:
        return self._ic.IC_MsgBox(msg.encode("utf-8"), title.encode("utf-8"))

    def open_video_capture_device(self, grabber: hGrabber, device_name: str) -> None:
        err = self._ic.IC_OpenVideoCaptureDevice(grabber, device_name.encode("utf-8"))
        if err == IC_ERROR:
            raise ICError("Failed to open video capture device")

    def close_video_capture_device(self, grabber: hGrabber) -> None:
        self._ic.IC_CloseVideoCaptureDevice(grabber)

    def set_video_format(self, grabber: hGrabber, format: str) -> None:
        err = self._ic.IC_SetVideoFormat(grabber, format.encode("utf-8"))
        if err == IC_ERROR:
            raise ICError("Failed to set video format {format}")

    def set_frame_rate(self, grabber: hGrabber, frame_rate: float) -> None:
        err = self._ic.IC_SetFrameRate(grabber, frame_rate)
        if err == IC_NOT_AVAILABLE:
            raise NotAvailableError(
                "Setting frame rate is not supported by the current device"
            )
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_NOT_IN_LIVEMODE:
            raise NotInLivemodeError("Setting frame rate is not possible in live mode")

    def save_device_state_to_file(self, grabber: hGrabber, file_path: FilePath) -> None:
        err = self._ic.IC_SaveDeviceStateToFile(grabber, str(file_path).encode("utf-8"))
        if err == IC_ERROR:
            raise ICError("Failed to save device state to file")

    def load_device_state_from_file(
        self, grabber: hGrabber, file_path: FilePath
    ) -> hGrabber:
        return self._ic.IC_LoadDeviceStateFromFile(
            grabber, str(file_path).encode("utf-8")
        )

    def set_property_switch(
        self, grabber: hGrabber, property: str, element: str, on: bool
    ) -> None:
        err = self._ic.IC_SetPropertySwitch(
            grabber, property.encode("utf-8"), element.encode("utf-8"), int(on)
        )
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError(
                f"Requested item {property} is not available."
            )
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                f"Requested element {element} is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def get_property_switch(
        self, grabber: hGrabber, property: str, element: str
    ) -> bool:
        on = ctypes.c_int()
        err = self._ic.IC_GetPropertySwitch(
            grabber, property.encode("utf-8"), element.encode("utf-8"), on
        )
        if err == IC_SUCCESS:
            return bool(on.value)
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def set_property_absolute_value(
        self, grabber: hGrabber, property: str, element: str, value: float
    ) -> None:
        err = self._ic.IC_SetPropertyAbsoluteValue(
            grabber, property.encode("utf-8"), element.encode("utf-8"), value
        )
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def get_property_absolute_value(
        self, grabber: hGrabber, property: str, element: str
    ) -> float:
        value = ctypes.c_float()
        err = self._ic.IC_GetPropertyAbsoluteValue(
            grabber, property.encode("utf-8"), element.encode("utf-8"), value
        )
        if err == IC_SUCCESS:
            return value.value
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def get_property_absolute_value_range(
        self, grabber: hGrabber, property: str, element: str
    ) -> tuple[float, float]:
        min_, max_ = ctypes.c_float(), ctypes.c_float()
        err = self._ic.IC_GetPropertyAbsoluteValueRange(
            grabber, property.encode("utf-8"), element.encode("utf-8"), min_, max_
        )
        if err == IC_SUCCESS:
            return (min_.value, max_.value)
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def get_property_value_range(
        self, grabber: hGrabber, property: str, element: str
    ) -> tuple[int, int]:
        min_, max_ = ctypes.c_long(), ctypes.c_long()
        err = self._ic.IC_GetPropertyValueRange(
            grabber, property.encode("utf-8"), element.encode("utf-8"), min_, max_
        )
        if err == IC_SUCCESS:
            return (min_.value, max_.value)
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )
        if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
            raise PropertyElementWrongInterfaceError(
                "Requested element does not have the interface that is needed."
            )

    def property_one_push(self, grabber: hGrabber, property: str) -> None:
        err = self._ic.IC_PropertyOnePush(
            grabber, property.encode("utf-8"), "One Push".encode("utf-8")
        )
        if err == IC_NO_HANDLE:
            raise NoHandleError("Invalid grabber handle")
        if err == IC_NO_DEVICE:
            raise NoDeviceError("No video capture device is opened")
        if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
            raise PropertyItemNotAvailableError("Requested item is not available.")
        if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
            raise PropertyElementNotAvailableError(
                "Requested element is not available."
            )

    def get_device_count(self) -> int:
        return self._ic.IC_GetDeviceCount()

    def get_device(self, index: int) -> str:
        device = self._ic.IC_GetDevice(index)
        if device:
            device = device.decode("utf-8")
        return device

    def get_unique_name_from_list(self, index: int) -> str:
        unique_name = self._ic.IC_GetUniqueNameFromList(index)
        if unique_name:
            unique_name = unique_name.decode("utf-8")
        return unique_name

    def open_device_by_unique_name(self, grabber: hGrabber, unique_name: str) -> None:
        self._ic.IC_OpenDeviceByUniqueName(grabber, unique_name.encode("utf-8"))
