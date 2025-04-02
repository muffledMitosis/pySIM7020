import enum
from typing import Optional
from dataclasses import dataclass

class SockDomain(enum.IntEnum):
  AF_INET = 1
  AF_INET6 = 2

class SockType(enum.IntEnum):
  SOCK_STREAM = 1
  SOCK_DGRAM = 2

class SockProto(enum.IntEnum):
  IPPROTO_TCP = 1
  IPPROTO_UDP = 2

@dataclass
class SockOps:
  sDomain: SockDomain
  sType: SockType
  sProto: SockProto

class Socket:
  def __init__(
      self,
      sockOps: Optional[SockOps] = SockOps(1, 1, 1)
    ):
    self.sockOps = sockOps

  def getConnCommand(self):
    ops = self.sockOps
    return f"AT+CSOC={ops.sDomain},{ops.sType},{ops.sProto}"
