# -*- coding: utf-8 -*-
"""
Python wrapper around Storm C API bindings
"""
import os.path
import storm
from os import SEEK_SET, SEEK_CUR, SEEK_END


SFILE_OPEN_FROM_MPQ = 0x00000000
SFILE_OPEN_PATCHED_FILE = 0x00000001
SFILE_OPEN_BY_INDEX = 0x00000002

MPQ_OPEN_NO_LISTFILE = 0x010
MPQ_OPEN_NO_ATTRIBUTES = 0x020
MPQ_OPEN_FORCE_MPQ_V1 = 0x040
MPQ_OPEN_CHECK_SECTOR_CRC = 0x080
MPQ_OPEN_READ_ONLY = 0x100

class MPQFile(object):
	"""
	An MPQ archive
	"""
	ATTRIBUTES = "(attributes)"
	LISTFILE = "(listfile)"

	def __init__(self, name, flags=MPQ_OPEN_READ_ONLY):
		priority = 0 # Unused by StormLib
		self._mpq = storm.SFileOpenArchive(name, priority, flags)
		self._name = os.path.basename(name)
		self._listfile = []

	def __contains__(self, name):
		return storm.SFileHasFile(self._mpq, name)

	def close(self):
		storm.SFileCloseArchive(self._mpq)

	def getinfo(self, member):
		return MPQInfo(member)

	def infoList(self):
		pass

	def is_patched(self):
		return storm.SFileIsPatchedArchive(self._mpq)

	def name(self):
		return self._name

	def namelist(self):
		if not self._listfile:
			from cStringIO import StringIO
			# fill the listfile
			f = self.open("(listfile)")
			lf = f.read().split("\r\n")
			# Get the cleaned listfile
			self._listfile = [x.replace("\\", "/") for x in lf if x]

		return self._listfile

	def open(self, name, mode="r", patched=True):
		if isinstance(name, int):
			raise NotImplementedError("Opening by index not implemented")

		flags = SFILE_OPEN_FROM_MPQ

		return MPQExtFile(storm.SFileOpenFileEx(self._mpq, name, flags))

	def patch(self, name, prefix=None, flags=0):
		storm.SFileOpenPatchArchive(self._mpq, name, prefix, flags)

	def extract(self, member, path="."):
		storm.SFileExtractFile(self._mpq, member, path)

	def printdir(self):
		for name in self.namelist():
			print name

	def read(self, name):
		pass

	def testmpq(self):
		pass


class MPQExtFile(object):
	def __init__(self, file):
		self._file = file

	def close(self):
		storm.SFileCloseFile(self._file)

	def read(self, size=None):
		if size is None:
			# Careful, this may break. Waiting for a proper stormlib api for this.
			size = self.size()
		return storm.SFileReadFile(self._file, size)

	def seek(self, offset, whence=SEEK_SET):
		storm.SFileSetFilePointer(self._file, offset, whence)

	def size(self):
		return storm.SFileGetFileSize(self._file)

class MPQInfo(object):
	def __init__(self, info):
		self._info = info

	def filename(self):
		return "(not implemented)"

	def date_time(self):
		raise NotImplementedError

	def compress_type(self):
		raise NotImplementedError

	def CRC(self):
		raise NotImplementedError

	def compress_size(self):
		return 0

	def file_size(self):
		return 0

def test():
	base = "/home/adys/mpq/WoW/12911.direct/Data/expansion1.MPQ"
	f = MPQFile(base)
	f.printdir()

if __name__ == "__main__":
	test()
