"""
# Python Spidev

Python interface for the spidev Linux kernel driver for connecting to SPI
devices.

All code is MIT licensed unless explicitly stated otherwise.

## Usage

```python
from spidev import SpiDev

# bus=0, device=1. Same as path="/dev/spidev0.1"
with SpiDev(0, 1) as spi:
    spi.write([0x01, 0x02, 0x03])

# or directly from a path and manually opening/closing the file:

spi = SpiDev(path="/dev/myspidev")
spi.open()

print(spi.read(64))

spi.close()
```
"""

from ._spi import SpiDev

__version__ = "4.0.0"

__all__ = ("SpiDev",)
