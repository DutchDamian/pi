from ctypes import *
schuifmaat = CDLL("./schuifmaat.so")
schuifmaat.meassureDistance.restype = c_float
test = round(schuifmaat.meassureDistance(), 2)
print(str(test))
