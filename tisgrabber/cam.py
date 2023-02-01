from ctypes import Structure
from typing import Any, Callable, Self

import numpy as np

from .enums import CameraProperty, VideoProperty
from .structs import HGRABBER
from .wrapper import FilePath, ImageControl

ic = ImageControl()


class CameraSetting:
    def __init__(self, grabber, property: CameraProperty):
        self._grabber = grabber
        self._property = property
        self.is_available = ic.is_camera_property_available(grabber, property)
        self.auto_available = ic.is_camera_property_auto_available(grabber, property)

    @property
    def value(self) -> int:
        if self.is_available:
            return ic.get_camera_property(self._grabber, self._property)
        else:
            raise RuntimeError("Camera property not available.")

    @value.setter
    def value(self, value: int) -> None:
        if self.is_available:
            self.auto = False
            ic.set_camera_property(self._grabber, self._property, value)
        else:
            raise RuntimeError("Camera property not available.")

    @property
    def setting_range(self) -> tuple[int, int]:
        if self.is_available:
            return ic.camera_property_get_range(self._grabber, self._property)
        else:
            raise RuntimeError("Camera property not available.")

    @property
    def auto(self) -> bool:
        if self.auto_available:
            return ic.get_auto_camera_property(self._grabber, self._property)
        else:
            raise RuntimeError("Auto setting for property is not available.")

    @auto.setter
    def auto(self, enable: bool) -> None:
        if self.auto_available:
            ic.enable_auto_camera_property(self._grabber, self._property, enable)
        else:
            raise RuntimeError("Auto setting for property is not available.")


class Exposure(CameraSetting):
    @property
    def setting(self) -> int:
        if self.is_available:
            return ic.get_exp_reg_val(self._grabber)
        else:
            raise RuntimeError("Camera property not available.")

    @setting.setter
    def setting(self, value: int) -> None:
        if self.is_available:
            self.auto = False
            ic.set_exp_reg_val(self._grabber, value)
        else:
            raise RuntimeError("Camera property not available.")

    @property
    def value(self) -> float:
        return ic.get_property_absolute_value(self._grabber, "Exposure", "Value")

    @value.setter
    def value(self, value: float) -> None:
        ic.set_property_absolute_value(self._grabber, "Exposure", "Value", value)


class VideoSetting:
    def __init__(self, grabber, property: VideoProperty):
        self._grabber = grabber
        self._property = property
        self.is_available = ic.is_video_property_available(grabber, property)
        self.auto_available = ic.is_video_property_auto_available(grabber, property)

    @property
    def setting(self) -> int:
        if self.is_available:
            return ic.get_video_property(self._grabber, self._property)
        else:
            raise RuntimeError("Video property not available.")

    @setting.setter
    def setting(self, value: int) -> None:
        if self.is_available:
            self.auto = False
            ic.set_video_property(self._grabber, self._property, value)
        else:
            raise RuntimeError("Video property not available.")

    @property
    def auto(self) -> bool:
        if self.auto_available:
            return ic.get_auto_video_property(self._grabber, self._property)
        else:
            raise RuntimeError("Auto setting for property is not available.")

    @auto.setter
    def auto(self, enable: bool) -> None:
        if self.auto_available:
            ic.enable_auto_video_property(self._grabber, self._property, enable)
        else:
            raise RuntimeError("Auto setting for property is not available.")

    @property
    def setting_range(self) -> tuple[int, int]:
        if self.is_available:
            return ic.video_property_get_range(self._grabber, self._property)
        else:
            raise RuntimeError("Video property not available.")


class Camera:
    def __init__(self, grabber: HGRABBER) -> None:
        self._grabber = grabber

        self.pan = CameraSetting(self._grabber, CameraProperty.PAN)
        self.tilt = CameraSetting(self._grabber, CameraProperty.TILT)
        self.roll = CameraSetting(self._grabber, CameraProperty.ROLL)
        self.zoom = CameraSetting(self._grabber, CameraProperty.ZOOM)
        # NOTE: Exposure is a special case with different commands
        self.exposure = Exposure(self._grabber, CameraProperty.EXPOSURE)
        self.iris = CameraSetting(self._grabber, CameraProperty.IRIS)
        self.focus = CameraSetting(self._grabber, CameraProperty.FOCUS)
        self.brightness = VideoSetting(self._grabber, VideoProperty.BRIGHTNESS)
        self.contrast = VideoSetting(self._grabber, VideoProperty.CONTRAST)
        self.hue = VideoSetting(self._grabber, VideoProperty.HUE)
        self.saturation = VideoSetting(self._grabber, VideoProperty.SATURATION)
        self.sharpness = VideoSetting(self._grabber, VideoProperty.SHARPNESS)
        self.gamma = VideoSetting(self._grabber, VideoProperty.GAMMA)
        self.color_enable = VideoSetting(self._grabber, VideoProperty.COLORENABLE)
        self.white_balance = VideoSetting(self._grabber, VideoProperty.WHITEBALANCE)
        self.black_light_compensation = VideoSetting(
            self._grabber, VideoProperty.BLACKLIGHTCOMPENSATION
        )
        self.gain = VideoSetting(self._grabber, VideoProperty.GAIN)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ic.release_grabber(self._grabber)

    def release_grabber(self):
        ic.release_grabber(self._grabber)

    @property
    def frame_rate(self) -> float:
        return ic.get_frame_rate(self._grabber)

    @frame_rate.setter
    def frame_rate(self, value: float) -> None:
        ic.set_frame_rate(self._grabber, value)

    def start_live(self) -> None:
        ic.start_live(self._grabber)

    def stop_live(self) -> None:
        ic.stop_live(self._grabber)

    def snap_image(self, timeout=1000) -> None:
        ic.snap_image(self._grabber, timeout=timeout)

    def get_image_data(self) -> np.ndarray:
        return ic.get_image_data(self._grabber)

    def save_device_state_to_file(self, filename: FilePath) -> None:
        ic.save_device_state_to_file(self._grabber, filename)

    def get_image_description(self) -> tuple[int, int, int, int]:
        return ic.get_image_description(self._grabber)

    def show_property_dialog(self) -> None:
        ic.show_property_dialog(self._grabber)

    def set_window_handle(self, handle: Any) -> None:
        ic.set_hwnd(self._grabber, handle)

    def set_continuous_mode(self, enable: bool) -> None:
        ic.set_continuous_mode(self._grabber, enable)

    def set_frame_ready_callback(
        self, callback: Callable[[Structure], None], data: Structure
    ):
        """
        Set a callback function that is called when a new frame is ready.

        Uses a simplified version of the callback signature as compared to the one
        required by the IC Imaging Control library.

        :param callback:
            Function to call when a new frame is ready. Takes `data` as its only
            argument.
        :param data:
            Payload of the callback function. Is passed as the only argument to
            the `callback` function.
        """

        def modified_callback(grabber, ptr, n_frame, data: Structure):
            # `grabber`, `ptr` and `n_frame` are not needed by the user but are required
            # by the IC Imaging Control library.
            callback(data)

        ic.set_frame_ready_callback(self._grabber, modified_callback, data)


if __name__ == "__main__":
    grabber = ic.show_device_selection_dialog()
    with Camera(grabber) as cam:
        cam.start_live()
        ic.msg_box("Press OK to stop.", "Live image")
        cam.stop_live()
