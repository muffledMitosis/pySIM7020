from .Device import Device

class TCP:
  def __init__(self, device: Device):
    self.__device = device
  
  def getDevice(self):
    return self.__device
