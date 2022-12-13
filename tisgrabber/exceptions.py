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


class ICError(Exception):
    """Base class for all IC exceptions."""

    pass


class NotAvailableError(ICError):
    """Exception raised when a property is not supported by the current device."""

    pass


class NoHandleError(ICError):
    """Exception raised when a handle is invalid."""

    pass


class NoDeviceError(ICError):
    """Exception raised when no video capture device is opened."""

    pass


class NotInLivemodeError(ICError):
    """Exception raised when setting a property  in live mode is not possible."""

    pass


class PropertyItemNotAvailableError(ICError):
    """Exception raised when a requested property item is not available."""

    pass


class PropertyElementNotAvailableError(ICError):
    """Exception raised when a requested property element is not available."""

    pass


class PropertyElementWrongInterfaceError(ICError):
    """
    Exception raised when a requested element hast not the interface which is needed.
    """

    pass


class NoPropertySetError(ICError):
    """Exception raised when a property set is not available."""

    pass


def check_device_handle_error_code(err: int) -> None:
    if err == IC_SUCCESS:
        return
    if err == IC_NO_HANDLE:
        raise NoHandleError("Invalid grabber handle")
    if err == IC_NO_DEVICE:
        raise NoDeviceError("No video capture device is opened")


def check_property_error_code(err: int) -> None:
    if err == IC_SUCCESS:
        return
    check_device_handle_error_code(err)
    if err == IC_PROPERTY_ITEM_NOT_AVAILABLE:
        raise PropertyItemNotAvailableError("Requested property is not available.")
    if err == IC_PROPERTY_ELEMENT_NOT_AVAILABLE:
        raise PropertyElementNotAvailableError("Requested element is not available.")
    if err == IC_PROPERTY_ELEMENT_WRONG_INTERFACE:
        raise PropertyElementWrongInterfaceError(
            "Requested element does not have the needed interface."
        )
