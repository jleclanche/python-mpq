# -*- coding: utf-8 -*-
"""
Python wrapper around Storm C API bindings
"""
import storm

MPQ_OPEN_NO_LISTFILE = 0x010
MPQ_OPEN_NO_ATTRIBUTES = 0x020
MPQ_OPEN_FORCE_MPQ_V1 = 0x040
MPQ_OPEN_CHECK_SECTOR_CRC = 0x080
MPQ_OPEN_READ_ONLY = 0x100

class MPQ(object):
	"""
	An MPQ archive
	"""
	ATTRIBUTES = "(attributes)"
	LISTFILE = "(listfile)"

	def __init__(self, name, flags=MPQ_OPEN_READ_ONLY):
		priority = 0 # Unused by StormLib
		self._mpq = storm.SFileOpenArchive(name, priority, flags)

	def close(self):
		storm.SFileCloseArchive(self._mpq)

	def getinfo(self):
		pass

	def namelist(self):
		pass

class MPQFile(object):
	pass

def test():
	base = "/home/adys/mpq/WoW/12911.direct/Data/expansion1.MPQ"

if __name__ == "__main__":
	test()
