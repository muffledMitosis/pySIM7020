import serial
import logging
import sys
from dataclasses import dataclass
from typing import Optional
from typing import List

from .Socket import *


@dataclass
class UART_OPS:
  """Represents the UART communication parameters.

  Attributes:
      port (str): The serial port to use for communication.
      baud (int): The baud rate for the serial communication.
  """
  port: str
  baud: int


@dataclass
class ATResponse:
  """Represents the response from an AT command sent to a device.

  Attributes:
      echo (str): The echo response returned from the device.
      response (List[str]): The lines of response from the device.
      success (bool): Whether the command was successful (ends with "OK").
  """
  echo: str
  response: List[str]
  success: bool


class Device:
  """Represents a sim7020 device that communicates over a UART serial
  connection.

  Attributes:
      __uartOps (UART_OPS): The UART configuration for communication.
      __serial (serial.Serial): The serial connection to the device.
  """

  def __init__(self, 
    uartOps: Optional[UART_OPS] = None,
    name: Optional[str] = "sim7020"):
    """Initializes the Device object and establishes the UART serial
    connection.

    Args:
        uartOps (Optional[UART_OPS]): UART configuration, if not provided,
        defaults to "/dev/serial0" and baud rate 115200.
        name (Optional[str]): Device name. Only used for printing information,
        if not provided defaults to "sim7020".

    Raises:
        SystemExit: If the serial connection cannot be established, the program
        exits.
    """
    self.__deviceName = name
    if uartOps is None:
      self.__uartOps = UART_OPS("/dev/serial0", 115200)
    else:
      self.__uartOps = UART_OPS(uartOps.port, uartOps.baud)

    try:
      self.__serial = serial.Serial(
          self.__uartOps.port, self.__uartOps.baud, timeout=2)
    except serial.SerialException as e:
      logging.error(
          f"Could not establish serial connection: {e}\n\nExiting...")
      sys.exit()

  def __str__(self):
    return (
     f"{self.__deviceName}: {{ "
     f"port: {self.__uartOps.port}, "
     f"baud: {self.__uartOps.baud}  }}"
    )

  def __sendAT(self, command: str) -> ATResponse:
    """Sends an AT command to the device and processes the response.

    Args:
        command (str): The AT command to send.

    Returns:
        ATResponse: The response object containing the echo, response, and
        success status.
    """
    self.__serial.write(f"{command}\r\n".encode())
    self.__serial.flush()

    response_lines = [line.decode().strip()
                      for line in self.__serial.readlines()]

    echo = response_lines[0] if response_lines else ""
    success = response_lines[-1] == "OK" if response_lines else False
    response = response_lines[1:-1] if success else response_lines[1:]

    return ATResponse(echo=echo, response=response, success=success)

  def getSignalQuality(self) -> ATResponse:
    """Fetches the signal quality of the device.

    Returns:
        ATResponse: The response to the "AT+CSQ" command containing signal
        quality information.
    """
    return self.__sendAT("AT+CSQ")

  def getFirmwareVersion(self) -> ATResponse:
    """Fetches the firmware version of the device.

    Returns:
        ATResponse: The response to the "AT+CGMR" command containing the
        firmware version.
    """
    return self.__sendAT("AT+CGMR")

  def getInternetRegisterStatus(self) -> ATResponse:
    """Fetches the device's internet registration status.

    Returns:
        ATResponse: The response to the "AT+CGREG?" command indicating
        registration status.
    """
    return self.__sendAT("AT+CGREG?")

  def getPDPStatus(self) -> ATResponse:
    """Fetches the Packet Data Protocol (PDP) status of the device.

    Returns:
        ATResponse: The response to the "AT+CGACT?" command indicating PDP
        status.
    """
    return self.__sendAT("AT+CGACT?")

  def getInternetInfo(self) -> ATResponse:
    """Fetches information about the device's internet connection.

    Returns:
        ATResponse: The response to the "AT+COPS?" command containing internet
        connection info.
    """
    return self.__sendAT("AT+COPS?")

  def getInternetStatus(self) -> ATResponse:
    """Fetches the internet connection status of the device.

    Returns:
        ATResponse: The response to the "AT+CGCONTRDP" command with connection
        status information.
    """
    return self.__sendAT("AT+CGCONTRDP")

  def createTCPConnection(self, sockObj):
    resp = self.__sendAT(sockObj.getConnCommand())
    if resp.success and (len(resp.response)>=1):
      return resp.response[0].split(" ")[1]
    else:
      return None
