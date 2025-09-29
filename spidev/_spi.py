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
        super().__init__(bus, client)

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
