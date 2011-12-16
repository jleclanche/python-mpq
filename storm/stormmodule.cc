#include <Python.h>
#define STORM_MODULE
#include "stormmodule.h"

#ifdef __cplusplus
extern "C" {
#endif

static PyObject *StormError;

/*
 * Manipulating MPQ archives
 */

static PyObject * Storm_SFileOpenArchive(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	char *name;
	int priority;
	int flags;
	bool result;

	if (!PyArg_ParseTuple(args, "sii:SFileOpenArchive", &name, &priority, &flags)) {
		return NULL;
	}
	result = SFileOpenArchive(name, priority, MPQ_OPEN_READ_ONLY, &mpq);

	if (!result) {
		PyErr_SetString(StormError, "Error opening archive");
		return NULL;
	}

	return Py_BuildValue("l", mpq);
}

static PyObject * Storm_SFileCloseArchive(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	bool result;

	if (!PyArg_ParseTuple(args, "i:SFileCloseArchive", &mpq)) {
		return NULL;
	}
	result = SFileCloseArchive(mpq);

	if (!result) {
		PyErr_SetString(StormError, "Error closing archive");
		return NULL;
	}

	Py_RETURN_NONE;
}

/*
 * Using Patched archives
 */

static PyObject * Storm_SFileOpenPatchArchive(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	char *name;
	char *prefix;
	int flags;
	bool result;

	if (!PyArg_ParseTuple(args, "issi:SFileIsPatchedArchive", &mpq, &name, &prefix, &flags)) {
		return NULL;
	}
	result = SFileOpenPatchArchive(mpq, name, prefix, flags);

	if (!result) {
		PyErr_SetString(StormError, "Could not patch archive");
		return NULL;
	}

	Py_RETURN_TRUE;
}

static PyObject * Storm_SFileIsPatchedArchive(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	bool result;

	if (!PyArg_ParseTuple(args, "i:SFileIsPatchedArchive", &mpq)) {
		return NULL;
	}
	result = SFileIsPatchedArchive(mpq);

	if (!result) {
		Py_RETURN_FALSE;
	}

	Py_RETURN_TRUE;
}

/*
 * Reading Files
 */

static PyObject * Storm_SFileOpenFileEx(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	char *name;
	int scope;
	HANDLE file = NULL;
	bool result;

	if (!PyArg_ParseTuple(args, "isi:SFileOpenFileEx", &mpq, &name, &scope)) {
		return NULL;
	}
	result = SFileOpenFileEx(mpq, name, scope, &file);

	if (!result) {
		PyErr_SetString(StormError, "Error opening file");
		return NULL;
	}

	return Py_BuildValue("l", file);
}

static PyObject * Storm_SFileGetFileSize(PyObject *self, PyObject *args) {
	HANDLE file = NULL;
	unsigned int sizeLow;
	unsigned int sizeHigh;

	if (!PyArg_ParseTuple(args, "i:SFileGetFileSize", &file)) {
		return NULL;
	}
	sizeLow = SFileGetFileSize(file, &sizeHigh);

	if (sizeLow == SFILE_INVALID_SIZE) {
		PyErr_SetString(StormError, "Error searching for file");
		return NULL;
	}

	return Py_BuildValue("l", sizeLow | sizeHigh);
}

static PyObject * Storm_SFileSetFilePointer(PyObject *self, PyObject *args) {
	HANDLE file = NULL;
	unsigned long offset;
	int whence;
	int posLow;
	int posHigh;
	unsigned int result;

	if (!PyArg_ParseTuple(args, "iii:SFileSetFilePointer", &file, &offset, &whence)) {
		return NULL;
	}

	posLow = (unsigned int) offset;
	posHigh = (unsigned int)(offset >> 32);

	result = SFileSetFilePointer(file, posLow, &posHigh, whence);

	Py_RETURN_NONE;
}

static PyObject * Storm_SFileReadFile(PyObject *self, PyObject *args) {
	HANDLE file = NULL;
	char * buffer;
	unsigned int size;
	unsigned int bytesRead;
	void * overlapped = 0;
	bool result;
	PyObject * ret;

	if (!PyArg_ParseTuple(args, "ii:SFileReadFile", &file, &size)) {
		return NULL;
	}

	buffer = (char*)malloc(size);

	result = SFileReadFile(file, buffer, size, &bytesRead, &overlapped);

	if (!result) {
		PyErr_SetString(StormError, "Error reading file");
		return NULL;
	}

	ret = Py_BuildValue("s#", buffer, bytesRead);
	free(buffer);

	return ret;
}

static PyObject * Storm_SFileCloseFile(PyObject *self, PyObject *args) {
	HANDLE file = NULL;

	bool result;
	if (!PyArg_ParseTuple(args, "i:SFileCloseFile", &file)) {
		return NULL;
	}
	result = SFileCloseFile(file);

	if (!result) {
		PyErr_SetString(StormError, "Error closing file");
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyObject * Storm_SFileHasFile(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	char *name;
	bool result;

	if (!PyArg_ParseTuple(args, "is:SFileHasFile", &mpq, &name)) {
		return NULL;
	}
	result = SFileHasFile(mpq, name);

	if (!result) {
		if (GetLastError() == ERROR_FILE_NOT_FOUND) {
			Py_RETURN_FALSE;
		} else {
			PyErr_SetString(StormError, "Error searching for file");
			return NULL;
		}
	}

	Py_RETURN_TRUE;
}

static PyObject * Storm_SFileExtractFile(PyObject *self, PyObject *args) {
	HANDLE mpq = NULL;
	char *name;
	char *localName;
	bool result;

	if (!PyArg_ParseTuple(args, "iss:SFileExtractFile", &mpq, &name, &localName)) {
		return NULL;
	}
	result = SFileExtractFile(mpq, name, localName);

	if (!result) {
		PyErr_SetString(StormError, "Error extracting file");
		return NULL;
	}

	Py_RETURN_NONE;
}


static PyMethodDef StormMethods[] = {
	{"SFileOpenArchive",  Storm_SFileOpenArchive, METH_VARARGS, "Open an MPQ archive."},
	{"SFileCloseArchive",  Storm_SFileCloseArchive, METH_VARARGS, "Close an MPQ archive."},

	{"SFileIsPatchedArchive",  Storm_SFileIsPatchedArchive, METH_VARARGS, "Determines if an MPQ archive has been patched"},
	{"SFileOpenPatchArchive", Storm_SFileOpenPatchArchive, METH_VARARGS, "Adds a patch archive to an MPQ archive"},

	{"SFileOpenFileEx", Storm_SFileOpenFileEx, METH_VARARGS, "Open a file from an MPQ archive"},
	{"SFileGetFileSize", Storm_SFileGetFileSize, METH_VARARGS, "Retrieve the size of a file within an MPQ archive"},
	{"SFileSetFilePointer", Storm_SFileSetFilePointer, METH_VARARGS, "Seeks to a position within archive file"},
	{"SFileReadFile", Storm_SFileReadFile, METH_VARARGS, "Reads bytes in an open file"},
	{"SFileCloseFile", Storm_SFileCloseFile, METH_VARARGS, "Close an open file"},
	{"SFileHasFile", Storm_SFileHasFile, METH_VARARGS, "Check if a file exists within an MPQ archive"},
	{"SFileExtractFile", Storm_SFileExtractFile, METH_VARARGS, "Extracts a file from an MPQ archive to the local drive"},
	{NULL, NULL, 0, NULL} /* Sentinel */
};

PyMODINIT_FUNC initstorm(void) {
	PyObject *m;

	m = Py_InitModule("storm", StormMethods);
	if (m == NULL) return;

	StormError = PyErr_NewException((char *)"storm.error", NULL, NULL);
	Py_INCREF(StormError);
	PyModule_AddObject(m, "error", StormError);
}

#ifdef __cplusplus
}
#endif
