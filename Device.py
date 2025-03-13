import serial

import logging
import sys
from dataclasses import dataclass
from typing import Optional
from typing import List

@dataclass
class UART_OPS:
  port: str
  baud: int

@dataclass
class ATResponse:
  echo: str
  response: List[str]
  success: bool

class Device:
  def __init__(self, uartOps: Optional[UART_OPS] = None):
    if uartOps is None:
      self.__uartOps = UART_OPS("/dev/serial0", 115200)
    else:
      self.__uartOps = UART_OPS(uartOps.port, uartOps.baud)

    try:
      self.__serial = serial.Serial(self.__uartOps.port, self.__uartOps.baud, timeout=2)
    except serial.SerialException as e:
      logging.error(f"Could not establish serial connection: {e}\n\nExiting...")
      sys.exit()

  def __sendAT(self, command: str):
    self.__serial.write(f"{command}\r\n".encode())
    self.__serial.flush()

    response_lines = [line.decode().strip() for line in self.__serial.readlines()]

    echo = response_lines[0] if response_lines else ""
    success = response_lines[-1] == "OK" if response_lines else False
    response = response_lines[1:-1] if success else response_lines[1:]

    return ATResponse(echo=echo, response=response, success=success)


  def getSignalQuality(self) -> ATResponse:
    return self.__sendAT("AT+CSQ")

  def getFirmwareVersion(self) -> ATResponse:
    return self.__sendAT("AT+CGMR")

  def getInternetRegisterStatus(self) -> ATResponse:
    return self.__sendAT("AT+CGREG?")

  def getPDPStatus(self) -> ATResponse:
    return self.__sendAT("AT+CGACT?")

  def getInternetInfo(self) -> ATResponse:
    return self.__sendAT("AT+COPS?")

  def getInternetStatus(self) -> ATResponse:
    return self.__sendAT("AT+CGCONTRDP")
