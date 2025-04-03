from .Device import Device
from .Socket import *

class TCP:
  def __init__(self, device: Device):
    self.__device = device
    self.__sock = Socket(SockOps(
      SockDomain.AF_INET,
      SockType.SOCK_STREAM,
      SockProto.IPPROTO_TCP
    ))

    self.__sock = device.createTCPSock(self.__sock)

  def getDevice(self):
    return self.__device

  def getSocketID(self):
    return self.__sock.getID()

  def listen(self, port: str):
    resp = self.__device.sockListen(self.__sock.getID(), port)
    return resp.success

# TODO: Implement
  def connect(self, ip: str, port: str):
    resp = self.__device.sockConnect(self.__sock.getID(), ip, port)
    return resp.success

  def awaitConnection(self)
    pass

  def send(data: bytes):
    resp = self.__device.sockSend(
        self.__sock.getID(),
        str(len(data)),
        data.decode()
      )
    return resp.success
