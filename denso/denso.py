"""

denso.py

@author: derricw

First attempt at a TCP interface for robot controller.

"""

import socket
import time


class DensoSocket(object):
	"""
	Control socket client for DENSO robot.
	"""
	def __init__(self,
				 address,
				 port,
				 timeout=10.0,
				 buffer_size=256):

		super(DensoSocket, self).__init__()
		self.address = address
		self.port = port
		self.timeout = timeout
		self.buffer_size = buffer_size
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.address, self.port))
		time.sleep(4)  #wait for connection
		self.sock.settimeout(self.timeout)

	def send(self, msg):
		"""
		Sends a message to the robot.
		"""
		self.sock.send(msg)

	def receive(self):
		"""
		Receives a message from the robot.
		"""
		return self.sock.recv(self.buffer_size)

	def close(self):
		"""
		Close the socket.
		"""
		self.sock.close()


class DensoRobot(object):
	"""
	Denso robot object.  Methods for basic robot movement
		and IO interaction.
	"""
	def __init__(self, ip, port):
		super(DensoRobot, self).__init__()
		self.ip = ip
		self.port = port

		self._setup_socket()

	def _setup_socket(self):
		"""
		Socket setup.
		"""
		self.sock = DensoSocket(self.ip, self.port)
		
	def move_absolute(self, x, y, z):
		"""
		Move position relative to zero.

		? Will this work ? What is zero for XYZ?

		"""
		cmd_str = self.command(['MA',str(x), str(y), str(z)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def move_relative(self, x, y, z):
		"""
		Move position relative to current position.
		"""
		cmd_str = self.command(['MR',str(x), str(y), str(z)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def movej_absolute(self, joint, magnitude):
		"""
		Move joint position relative to zero.
		"""
		cmd_str = self.command(['MJA',str(joint), str(magnitude)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def movej_relative(self, joint, magnitude):
		"""
		Move joint position relative to current position.
		"""
		cmd_str = self.command(['MJR', str(joint), str(magnitude)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def move_point(self, point):
		"""
		Move to a saved point.
		
		for example 'P50'

		"""
		cmd_str = self.command(["MP", str(point)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def set_speed(self, speed):
		"""
		Set speed.
		"""
		cmd_str = self.command(["SS", str(speed)])
		self.sock.send(cmd_str)
		return self.wait_for_completion()

	def get_speed(self):
		"""
		Get speed.
		"""
		cmd_str = self.command(["GS"])
		self.sock.send(cmd_str)
		response = self.sock.receive()
		return response

	def get_pos(self):
		"""
		Get position.
		"""
		cmd_str = self.command(["GP"])
		self.sock.send(cmd_str)
		response = self.sock.receive()
		return response

	def get_jpos(self):
		"""
		Get joint position.
		"""
		cmd_str = self.command(['GPJ'])
		self.sock.send(cmd_str)
		response = self.sock.receive()
		return response

	def close(self):
		"""
		Close the robot connection.
		"""
		self.sock.close()

	def wait_for_completion(self):
		"""
		Gets response code.  Not sure what to
			do with it yet.
		"""
		data = self.sock.receive()
		if "DONE" in data:
			return 0
		else:
			return 1

	def command(self, cmd_list):
		"""
		Creates a CR delimited command string.
		"""
		length = len(cmd_list)
		pad = "0\r"*(4-length)
		cmd = "\r".join(cmd_list) + "\r" + pad
		return cmd

if __name__ == '__main__':
	dr = DensoRobot(ip='192.168.1.10', port=5001)
	dr.move_absolute(4,5,6)
	dr.close()