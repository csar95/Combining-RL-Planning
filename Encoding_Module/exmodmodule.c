#include <Python.h>

static PyObject* exmod_get_legal_actions(PyObject *self, PyObject *args)
{
  PyObject *state, *allActions, *immutableProps;
  PyObject *legalActions = PySet_New(NULL);

  if (!PyArg_ParseTuple(args, "OOO", &state, &immutableProps, &allActions)) return NULL;

  PyObject *action, *definition, *pre, *targetValue, *stateValue;
  Py_ssize_t pos1 = 0, pos2 = 0;
  int legal;

  while (PyDict_Next(allActions, &pos1, &action, &definition))
  {
    legal = 1;  // True
    pos2 = 0;
    while (PyDict_Next(PyDict_GetItemString(definition, "precondition"), &pos2, &pre, &targetValue))
    {
      stateValue = PyDict_GetItem(state, pre);

      if ((stateValue == NULL && PySet_Contains(immutableProps, pre) != 1) ||  // If pre not in state and pre is not found in immutableProps
          (stateValue != NULL && PyObject_RichCompareBool(PyDict_GetItem(state, pre), targetValue, Py_EQ) == 0))  // If pre in state and it is False that they are equal
      {
        legal = 0;  // False
        break;
      }
    }

    if (legal == 1) PySet_Add(legalActions, action);
  }

  return Py_BuildValue("O", legalActions);
}

static PyObject* exmod_is_legal(PyObject *self, PyObject *args)
{
  PyObject *state, *preconditions, *immutableProps;

  if (!PyArg_ParseTuple(args, "OOO", &state, &immutableProps, &preconditions)) return NULL;

  PyObject *pre, *targetValue, *stateValue;
  Py_ssize_t pos = 0;
  int legal = 1;  // True

  while (PyDict_Next(preconditions, &pos, &pre, &targetValue))
  {
    stateValue = PyDict_GetItem(state, pre);

    if ((stateValue == NULL && PySet_Contains(immutableProps, pre) != 1) ||  // If pre not in state and pre is not found in immutableProps
        (stateValue != NULL && PyObject_RichCompareBool(PyDict_GetItem(state, pre), targetValue, Py_EQ) == 0))  // If pre in state and it is False that they are equal
    {
      legal = 0;  // False
      break;
    }
  }

  return Py_BuildValue("i", legal);
}

static PyMethodDef exmod_methods[] = {
  {"get_legal_actions", exmod_get_legal_actions, METH_VARARGS, "Get legal actions from the current state"},
  {"is_legal", exmod_is_legal, METH_VARARGS, "Returns whether the action is legal"},
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef exmod =
{
    PyModuleDef_HEAD_INIT,
    "exmod", /* name of module */
    NULL,          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    exmod_methods
};

PyMODINIT_FUNC PyInit_exmod(void)
{
  return PyModule_Create(&exmod);
}
