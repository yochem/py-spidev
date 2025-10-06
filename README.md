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

## SpiDev
Connect to a SPI device.

Examples:

```python
>>> SpiDev(0, 1) # connect to /dev/spidev0.1

>>> SpiDev(path='/dev/myspi') # connect to /dev/myspi
```

### Properties
#### `bits_per_word`: int
Bits per word used in the xfer methods.

#### `closed`: bool
Return True if the connection is not opened.

#### `cshigh`: bool

#### `loop`: bool
Sets the SPI_LOOP flag to enable loopback mode.

#### `lsbfirst`: bool

#### `max_speed_hz`: int
Max speed (in Hertz).

#### `mode`: int
SPI mode.

A two bit pattern of clock polarity and phase [CPOL|CPHA],
min: 0b00 = 0, max: 0b11 = 3

#### `no_cs`: bool
Sets the SPI_NO_CS flag to disable use of the chip select.

#### `read0`: bool
Read 0 bytes after transfer to lower CS if cshigh is set.

#### `threewire`: bool
SI/SO signals shared.


### Methods
#### `__init__(bus, device, path, mode, bits_per_word, max_speed_hz, read0)`
<details><summary>Signature</summary>

```python
def __init__(
    self,
    bus: int | None = None,
    device: int | None = None,
    *,
    path: StrPath | None = None,
    mode: int | None = None,
    bits_per_word: int | None = None,
    max_speed_hz: int | None = None,
    read0: bool | None = None
) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L40-L73)

</details>

Initialize self.  See help(type(self)) for accurate signature.

#### `close()`
<details><summary>Signature</summary>

```python
def close(self) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L195-L198)

</details>

Close the object from the interface.

#### `fileno()`
<details><summary>Signature</summary>

```python
def fileno(self) -> int
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L199-L213)

</details>

Return the file descriptor if it exists.

Returns:
    int: File descriptor number.

Raises:
    ValueError: if the connection is not open.

#### `open(bus, device)`
<details><summary>Signature</summary>

```python
def open(self, bus: int | None = None, device: int | None = None) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L221-L244)

</details>

Connect to the SPI device special file.

If bus and device are provided it opens "/dev/spidev<bus.<device>". If
path is provided it opens the SPI device at given path. Symbolic links
are followed.

Args:
    bus: Bus number.
    device: Device number.

Raises:
    ValueError: If bus/device or path is not provided.

#### `open_path(path)`
<details><summary>Signature</summary>

```python
def open_path(self, path: StrPath | None = None) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L245-L259)

</details>

Open SPI device at given path.

Args:
    path: Path to SPI device.

Raises:
    IOError

#### `read(size)`
<details><summary>Signature</summary>

```python
def read(self, size: int = -1, /) -> list[int]
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L260-L279)

</details>

Read and return up to _size_ bytes.

If size is omitted or negative, 1 byte is read.

Returns:
    list[int]: _size_ number of bytes.

Raises:
    OSError: If device is closed.

#### `readable()`
<details><summary>Signature</summary>

```python
def readable(self) -> bool
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L280-L283)

</details>

Return True if the SPI device is currently open.

#### `readbytes(length)`
<details><summary>Signature</summary>

```python
def readbytes(self, length: int) -> list[int]
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L284-L287)

</details>


#### `write(b)`
<details><summary>Signature</summary>

```python
def write(self, b: Sequence[int] | Buffer, /) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L292-L310)

</details>

Write bytes to SPI device.

Accepts arbitrary large lists. If list size exceeds buffer size (read
from /sys/module/spidev/parameters/bufsiz), data will be
split into smaller chunks and sent in multiple operations.

Args:
    b: Sequence of bytes or Buffer to write.

Raises:
    OSError: If device is closed.

#### `writeable()`
<details><summary>Signature</summary>

```python
def writeable(self) -> bool
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L288-L291)

</details>

Return True if the SPI connection is currently open.

#### `writebytes(values)`
<details><summary>Signature</summary>

```python
def writebytes(self, values: Sequence[int]) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L311-L314)

</details>


#### `writebytes2(values)`
<details><summary>Signature</summary>

```python
def writebytes2(self, values: Sequence[int] | Buffer) -> None
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L315-L318)

</details>


#### `xfer(values, speed_hz, delay_usecs, bits_per_word)`
<details><summary>Signature</summary>

```python
def xfer(
    self,
    values: Sequence[int],
    speed_hz: int | None = None,
    delay_usecs: int | None = None,
    bits_per_word: int | None = None
) -> list[int]
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L319-L341)

</details>

Performs an SPI transaction.

NOTE: Chip-select should be released and reactivated between blocks.

Args:
    values: Bytes to write.
    speed_hz: Speed to use.
    delay_usecs: Delay in microseconds between blocks.
    bits_per_word: Bits per word.

Returns:
    TODO

#### `xfer2(values, speed_hz, delay_usecs, bits_per_word)`
<details><summary>Signature</summary>

```python
def xfer2(
    self,
    values: Sequence[int],
    speed_hz: int | None = None,
    delay_usecs: int | None = None,
    bits_per_word: int | None = None
) -> list[int]
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L342-L364)

</details>

Performs an SPI transaction.

NOTE: Chip-select should be held active between blocks.

Args:
    values: Bytes to write.
    speed_hz: Speed to use.
    delay_usecs: Delay in microseconds between blocks.
    bits_per_word: Bits per word.

Returns:
    TODO

#### `xfer3(values, speed_hz, delay_usecs, bits_per_word)`
<details><summary>Signature</summary>

```python
def xfer3(
    self,
    values: Sequence[int],
    speed_hz: int | None = None,
    delay_usecs: int | None = None,
    bits_per_word: int | None = None
) -> tuple[int, ...]
```
[Full source](https://github.com/yochem/py-spidev/blob/5d02d3acddb5fea513415f593c972dca7418e806/spidev/_spi.py#L365-L389)

</details>

Performs an SPI transaction.

Accepts arbitrary large lists. If list size exceeds buffer size (read
from /sys/module/spidev/parameters/bufsiz), data will be split
into smaller chunks and sent in multiple operations.

Args:
    values: Bytes to write.
    speed_hz: Speed to use.
    delay_usecs: Delay in microseconds between blocks.
    bits_per_word: Bits per word.

Returns:
    TODO

## The Linux kernel and SPI bus numbering and the role of udev

### Summary

If your code may interact with an SPI controller which is attached to the
system via the USB or PCI buses, **or** if you are maintaining a product which
is likely to change SoCs **or upgrade kernels** during its lifetime, then you
should consider using one or more udev rules to create symlinks to the SPI
controller spidev, and then use `open_path`, to open the device file via the
symlink in your code.

Consider allowing the end-user to configure their choice of full spidev path -
for example with the use of a command line argument to your Python script, or
an entry in a configuration file which your code reads and parses.

Additional udev actions can also set the ownership and file access permissions
on the spidev device node file (to increase the security of the system).  In
some instances, udev rules may also be needed to ensure that spidev device
nodes are created in the first place (by triggering the Linux `spidev` driver
to "bind" to an underlying SPI controller).

### Detailed Information

This section provides an overview of the Linux APIs which this extension uses.

**If your software might be used on systems with non-deterministic SPI bus
numbering**, then using the `open_path` method can allow those maintaining the
system to use mechanisms such as `udev` to create stable symbolic links to the
SPI device for the correct physical SPI bus.

See the example udev rule file `99-local-spi-example-udev.rules`.

This Python extension communicates with SPI devices by using the 'spidev'
[Linux kernel SPI userspace
API](https://www.kernel.org/doc/html/next/spi/spidev.html).

'spidev' in turn communicates with SPI bus controller hardware using the
kernel's internal SPI APIs and hardware device drivers.

If the system is configured to expose a particular SPI device to user space
(i.e. when an SPI device is "bound" to the spidev driver), then the spidev
driver registers this device with the kernel, and exposes its Linux kernel SPI
bus number and SPI chip select number to user space in the form of a POSIX
"character device" special file.

A user space program (usually 'udev') listens for kernel device creation
events, and creates a file system "device node" for user space software to
interact with.  By convention, for spidev, the device nodes are named
`/dev/spidev<bus>.<device>` is (where the *bus* is the Linux kernel's internal
SPI bus number (see below) and the *device* number corresponds to the SPI
controller "chip select" output pin that is connected to the SPI *device* 'chip
select' input pin.

The Linux kernel **may assign SPI bus numbers to a system's SPI controllers in
a non-deterministic way.** In some hardware configurations, the SPI bus number
of a particular hardware peripheral is:

- Not guaranteed to remain constant between different Linux kernel versions.
- Not guaranteed to remain constant between successive boots of the same kernel
  (due to race conditions during boot-time hardware enumeration, or dynamic
  kernel module loading).
- Not guaranteed to match the hardware manufacturer's SPI bus numbering scheme.

In the case of SPI controllers which are themselves connected to the system via
buses that are subject to hot-plug (such as USB, Thunderbolt, or PCI), the SPI
bus number should usually be expected to be non-deterministic.

The supported Linux mechanism which allows user space software to identify the
correct hardware, it to compose "udev rules" which create stable symbolic links
to device files. For example, most Linux distributions automatically create
symbolic links to allow identification of block storage devices e.g. see the
output of `ls -alR /dev/disk`.

`99-local-spi-example-udev.rules` included with py-spidev includes example udev
rules for creating stable symlink device paths (for use with SpiDev's `path`
argument).

E.g. the following Python code could be used to communicate with an SPI device
attached to chip-select line 0 of an individual FTDI FT232H USB to SPI adapter
which has the USB serial number "1A8FG636":


```python
import spidev

spi = spidev.SpiDev(path="/dev/spi/by-path/usb-sernum-1A8FG636-cs-0")

with spi:
    # TODO: Useful stuff here
    ...
```

In the more general case, the example udev file should be modified as
appropriate to your needs, renamed to something descriptive of the purpose
and/or project, and placed in `/etc/udev/rules.d/` (or `/lib/udev/rules.d/` in
the case of rules files included with operating system packages).

