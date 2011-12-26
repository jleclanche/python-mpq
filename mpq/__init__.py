# -*- coding: utf-8 -*-
"""
Python wrapper around Storm C API bindings
"""
import os.path
import storm
from os import SEEK_SET, SEEK_CUR, SEEK_END


class MPQFile(object):
	"""
	An MPQ archive
	"""
	ATTRIBUTES = "(attributes)"
	LISTFILE = "(listfile)"

	def __init__(self, name, flags=0):
		priority = 0 # Unused by StormLib
		self._mpq = storm.SFileOpenArchive(name, priority, flags)
		self.name = name
		self._listfile = []

	def __contains__(self, name):
		return storm.SFileHasFile(self._mpq, name)

	def close(self):
		storm.SFileCloseArchive(self._mpq)

	def flush(self):
		storm.SFileFlushArchive(self._mpq)

	def getinfo(self, f):
		if isinstance(f, basestring):
			f = self.open(f.replace("/", "\\"))
		return MPQInfo(f)

	def infolist(self):
		return [self.getinfo(x) for x in self.namelist()]

	def is_patched(self):
		return storm.SFileIsPatchedArchive(self._mpq)

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
		flags = 0
		if isinstance(name, int):
			name = "File%08x.xxx" % (int)

		if patched:
			flags |= storm.SFILE_OPEN_PATCHED_FILE

		return MPQExtFile(storm.SFileOpenFileEx(self._mpq, name, flags), name)

	def patch(self, name, prefix=None, flags=0):
		storm.SFileOpenPatchArchive(self._mpq, name, prefix, flags)

	def extract(self, member, path="."):
		storm.SFileExtractFile(self._mpq, member, path)

	def printdir(self):
		print "%-85s %12s %12s" % ("File Name", "Size", "    Packed Size")
		for x in self.infolist():
			#date = "%d-%02d-%02d %02d:%02d:%02d" % x.date_time[:6]
			print "%-85s %12d %12d" % (x.filename, x.file_size, x.compress_size)

	def read(self, name):
		pass

	def testmpq(self):
		pass


class MPQExtFile(object):
	def __init__(self, file, name):
		self._file = file
		self.name = name

	def _info(self, type):
		return storm.SFileGetFileInfo(self._file, type)

	def close(self):
		storm.SFileCloseFile(self._file)

	def read(self, size=None):
		if size is None:
			size = self.size() - self.tell()
		return storm.SFileReadFile(self._file, size)

	def seek(self, offset, whence=SEEK_SET):
		storm.SFileSetFilePointer(self._file, offset, whence)

	def size(self):
		return storm.SFileGetFileSize(self._file)

	def tell(self):
		return storm.SFileSetFilePointer(self._file, 0, SEEK_CUR)

class MPQInfo(object):
	def __init__(self, file):
		self._file = file

	@property
	def basename(self):
		return os.path.basename(self.filename)

	@property
	def filename(self):
		return self._file.name.replace("\\", "/")

	@property
	def date_time(self):
		return self._file._info(storm.SFILE_INFO_FILETIME)

	@property
	def compress_type(self):
		raise NotImplementedError

	@property
	def CRC(self):
		raise NotImplementedError

	@property
	def compress_size(self):
		return self._file._info(storm.SFILE_INFO_COMPRESSED_SIZE)

	@property
	def file_size(self):
		return self._file._info(storm.SFILE_INFO_FILE_SIZE)
