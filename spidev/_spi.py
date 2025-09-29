from . import _cspi

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from types import TracebackType
    from typing import Self, Union, Sequence, overload
    from collections.abc import Buffer

    StrPath = Union[str, PathLike[str]]


class SpiDev(_cspi.SpiDev):
    def __init__(
        self,
        bus: int | None = None,
        device: int | None = None,
        *,
        path: StrPath | None = None,
        mode: int | None = None,
        bits_per_word: int | None = None,
        max_speed_hz: int | None = None,
    ):
        super().__init__(bus, device)

        self.bus = bus
        self.device = device
        if mode is not None:
            self.mode = mode

        if path and (bus or device):
            raise ValueError(
                "both path and bus/device number of SPI device are provided"
            )
        self.path = path

        if mode is not None:
            self.mode = mode
        if bits_per_word is not None:
            self.bits_per_word = bits_per_word
        if max_speed_hz is not None:
            self.max_speed_hz = max_speed_hz
        if read0 is not None:
            super().__setattr__("read0", read0)

        # TODO: open() here? It's what the original implementation did
        self.open()

    def _resolve_path(self) -> str:
        if self.bus is not None and self.device is not None:
            return "/dev/spidev{:d}.{:d}".format(self.bus, self.device)
        elif self.path is not None:
            return str(self.path)
        raise ValueError("bus/device or path not set")

    @property
    def mode(self) -> int:
        """SPI mode.

        A two bit pattern of clock polarity and phase [CPOL|CPHA],
        min: 0b00 = 0, max: 0b11 = 3
        """
        return super().mode

    @mode.setter
    def mode(self, value: int) -> None:
        try:
            v = int(value)
        except (TypeError, ValueError):
            raise TypeError(f"mode must be an integer, but is {value}")

        if not 0 <= v <= 3:
            raise ValueError(f"mode must be between 0 and 3, but is {v}")

        super().__setattr__("mode", v)

    def closed(self) -> bool:
        """True if the connection is closed."""
        try:
            self.fileno()
            return True
        except ValueError:
            return False

    def fileno(self) -> int:
        """Return the file descriptor if it exists.

        Returns:
            int: File descriptor number.

        Raises:
            ValueError: if the connection is not open.
        """
        fd = super().fileno()
        if fd < 0:
            raise ValueError("I/O operation on closed file")
        return fd

    @overload
    def open(self) -> None: ...
    @overload
    def open(self, bus: int, device: int) -> None: ...
    def open(self, bus: int | None = None, device: int | None = None) -> None:
        """Connect to the SPI device special file.

        If bus and device are provided it opens "/dev/spidev<bus.<device>". If
        path is provided it opens the SPI device at given path. Symbolic links
        are followed.

        Raises:
            ValueError: If bus/device or path is not provided.
        """
        if bus:
            self.bus = bus
        if device:
            self.device = device

        path = self._resolve_path()
        super().open_path(path)
        # TODO: return and set fd

    def read(self, size: int | None = None, /) -> list[int]:
        """Read and return up to _size_ bytes.

        If size is omitted or negative, 1 byte is read.

        Returns:
            list[int]: _size_ number of bytes.
        """
        if not self.readable():
            raise OSError("SPI device not readable")
        # TODO: negative size generally means "read as much as possible". How
        # can we mimic this behavior?
        if size is None or size < 1:
            size = 1
        return super().readbytes(size)

    def readable(self) -> bool:
        """True if the SPI connection is currently open."""
        return not self.closed()

    def writeable(self) -> bool:
        """True if the SPI connection is currently open."""
        return not self.closed()

    def write(self, b: Sequence[int] | Buffer, /) -> None:
        if not self.writeable():
            raise OSError("SPI device not writeable")
        # TODO: return number of bytes written
        super().writebytes2(b)

    def __enter__(self) -> Self:
        """
        Warning: The `bus` and `device` attributes must be set to open the
        connection automatically:

        ```
        spi = SpiDev(bus=0, device=1)
        # or
        spi = SpiDev()
        spi.bus = 0
        spi.device = 1
        # or
        with spi:
            spi.open(0, 1)
            ...
        ```
        """
        try:
            self.open()
        except ValueError:
            pass

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        super().close()
