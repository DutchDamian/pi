import time
import spidev

# Pi heeft 1 SPI bus met 2 devices (dus bus heeft 1 mogelijkheid, device 2)
bus = 0
device = 1

# Enable
spi = spidev.SpiDev()

# Open device
spi.open(bus, device)

# Set SPI speed and mode
spi.max_speed_hz = 500000
spi.mode = 0

