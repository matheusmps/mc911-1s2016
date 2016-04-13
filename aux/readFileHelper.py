import sys

class FileHelper(object):
	def __init__(self, filePath):
		self.filePath = filePath

	def readFile(self):
		with open(self.filePath, 'r') as myFile:
			data = myFile.read()
		return data