from . import _cspi

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType
    from typing import Self, Union, Sequence
    from collections.abc import Buffer


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
        if self.bus and self.device:
            super().open(self.bus, self.device)

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        super().close()
