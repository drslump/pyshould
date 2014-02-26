"""
Patches cpython's root object to expose should assertions as 
properties.

The code is heavily based on the one originally found in the
sure library (https://github.com/gabrielfalcao/sure), used
with permission (https://github.com/gabrielfalcao/sure/issues/50)
"""

import platform

__author__ = "Ivan -DrSlump- Montes"
__email__ = "drslump@pollinimini.net"
__license__ = "MIT"


is_cpython = (
    hasattr(platform, 'python_implementation')
    and platform.python_implementation().lower() == 'cpython')

if is_cpython:

    import ctypes

    DictProxyType = type(object.__dict__)

    Py_ssize_t = \
        hasattr(ctypes.pythonapi, 'Py_InitModule4_64') \
            and ctypes.c_int64 or ctypes.c_int

    class PyObject(ctypes.Structure):
        pass

    PyObject._fields_ = [
        ('ob_refcnt', Py_ssize_t),
        ('ob_type', ctypes.POINTER(PyObject)),
    ]

    class SlotsProxy(PyObject):
        _fields_ = [('dict', ctypes.POINTER(PyObject))]

    def patchable_builtin(klass):
        name = klass.__name__
        target = getattr(klass, '__dict__', name)

        if not isinstance(target, DictProxyType):
            return target

        proxy_dict = SlotsProxy.from_address(id(target))
        namespace = {}

        ctypes.pythonapi.PyDict_SetItem(
            ctypes.py_object(namespace),
            ctypes.py_object(name),
            proxy_dict.dict,
        )

        return namespace[name]

    try:
        import __builtin__ as builtins
    except ImportError:
        import builtins

    def make_prop(exp, is_none=False):
        return builtins.property(
            fget=lambda self: exp(self),
            fset=lambda self, other: None,
            fdel=lambda self, *args, **kwargs: None
        )

    from pyshould.expectation import Expectation, ExpectationNot, ExpectationAll, \
                                     ExpectationAny, ExpectationNone

    object_handler = patchable_builtin(object)
    object_handler['should'] = make_prop(Expectation)
    object_handler['should_not'] = make_prop(ExpectationNot)
    object_handler['should_all'] = make_prop(ExpectationAll)
    object_handler['should_any'] = make_prop(ExpectationAny)
    object_handler['should_none'] = make_prop(ExpectationNone)

    # None does not have a tp_dict associated to its PyObject, so this
    # is the only way we could make it work like we expected.
    none_handler = patchable_builtin(None.__class__)
    none_handler['should'] = Expectation(None)
    none_handler['should_not'] = ExpectationNot(None)
    none_handler['should_all'] = ExpectationAll(None)
    none_handler['should_any'] = ExpectationAny(None)
    none_handler['should_none'] = ExpectationNone(None)

else:
    from warnings import warn
    warn("pyshould's patch is only supported on cpython", DeprecationWarning)
    