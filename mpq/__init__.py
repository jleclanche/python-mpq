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

	def __init__(self, name=None, flags=0):
		self._archives = []
		if name is not None:
			self.add_archive(name, flags)

	def __contains__(self, name):
		for mpq in self._archives:
			if storm.SFileHasFile(mpq, name):
				return True
		return False

	def _archive_contains(self, name):
		for mpq in self._archives:
			if storm.SFileHasFile(mpq, name):
				return mpq

	def _regenerate_listfile(self):
		self._listfile = []
		for mpq in self._archives:
			# Here we manually open each listfile as mpq.open() would
			# only get us the first available file
			f = MPQExtFile(storm.SFileOpenFileEx(mpq, self.LISTFILE, 0), self.LISTFILE)
			lf = f.read().split("\r\n")
			# We clean the listfile first...
			self._listfile += [x.replace("\\", "/") for x in lf if x]

	def add_archive(self, name, flags=0):
		priority = 0 # Unused by StormLib
		self._archives.append(storm.SFileOpenArchive(name, priority, flags))
		self.name = name
		self._listfile = []

	def close(self):
		for mpq in self._archives:
			storm.SFileCloseArchive(mpq)

	def flush(self):
		for mpq in self._archives:
			storm.SFileFlushArchive(mpq)

	def getinfo(self, f):
		if isinstance(f, basestring):
			f = self.open(f.replace("/", "\\"))
		return MPQInfo(f)

	def infolist(self):
		return [self.getinfo(x) for x in self.namelist()]

	def is_patched(self):
		for mpq in self._archives:
			if storm.SFileIsPatchedArchive(mpq, name):
				return True
		return False

	def namelist(self):
		if not self._listfile:
			self._regenerate_listfile()
		return self._listfile

	def open(self, name, mode="r", patched=True):
		flags = 0
		if isinstance(name, int):
			name = "File%08x.xxx" % (int)

		if patched:
			flags |= storm.SFILE_OPEN_PATCHED_FILE

		mpq = self._archive_contains(name)
		if not mpq:
			raise KeyError("There is no item named %r in the archive" % (name))

		return MPQExtFile(storm.SFileOpenFileEx(mpq, name, flags), name)

	def patch(self, name, prefix=None, flags=0):
		for mpq in self._archives:
			storm.SFileOpenPatchArchive(mpq, name, prefix, flags)

	def extract(self, member, path="."):
		mpq = self._archive_contains(name)
		if not mpq:
			raise KeyError("There is no item named %r in the archive" % (name))
		storm.SFileExtractFile(mpq, member, path)

	def printdir(self):
		print("%-85s %12s %12s" % ("File Name", "Size", "    Packed Size"))
		for x in self.infolist():
			#date = "%d-%02d-%02d %02d:%02d:%02d" % x.date_time[:6]
			print("%-85s %12d %12d" % (x.filename, x.file_size, x.compress_size))

	def read(self, name):
		if isinstance(name, MPQInfo):
			name = name.name
		f = self.open(name)
		return f.read()

	def testmpq(self):
		pass


class MPQExtFile(object):
	def __init__(self, file, name):
		self._file = file
		self.name = name

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.name)

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
