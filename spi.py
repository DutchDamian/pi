from time import sleep
import spidev

# Pi heeft 1 SPI bus met 2 devices (dus bus heeft 1 mogelijkheid, device 2)
bus = 0
device = 0

# Enable
spi = spidev.SpiDev()

# Open device
spi.open(bus, device)


try:
    while True:
#        to_send = [0x01, 0x02, 0x03]
#        resp = spi.xfer2(to_send)
        resp = spi.readbytes(4)
        if (resp == ""):
          print("nothing")

        print(resp)
        #print(resp)
#        print(int.from_bytes(color[0], "big"))
        sleep(1)
finally:
    spi.close()

