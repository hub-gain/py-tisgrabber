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
