import serial

import logging
import sys
from dataclasses import dataclass
from typing import Optional

@dataclass
class UART_OPS:
	port: str
	baud: int

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
		self.__serial.