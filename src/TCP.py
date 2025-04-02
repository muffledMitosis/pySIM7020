from .Device import Device
from .Socket import *

class TCP:
  def __init__(self, device: Device):
    self.__device = device
    self.__socket = Socket(SockOps(
      SockDomain.AF_INET,
      SockType.SOCK_STREAM,
      SockProto.IPPROTO_TCP
    ))

    sockID = device.createTCPSocket(self.__socket)
    self.__socket.setID(sockID)
    print(sockID)
  
  def getDevice(self):
    return self.__device
