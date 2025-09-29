from . import _cspi

from types import TracebackType
from typing import Self


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

    def __enter__(self) -> Self:
        """
        Warning: The `bus` and `device` attributes have to be set to open the
        connection:

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
