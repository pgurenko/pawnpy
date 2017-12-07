//-----------------------------------------------------------------------------
#include "amx.h"
#include "compiler.h"
//-----------------------------------------------------------------------------
using namespace boost::python;
//-----------------------------------------------------------------------------

void translator(exception const& e) {
  PyErr_SetString(PyExc_RuntimeError, e.what());
}
//-----------------------------------------------------------------------------

BOOST_PYTHON_MODULE(pawnpy) {
  register_exception_translator<exception>(translator);

  def("cc", cc, (boost::python::arg("input"), boost::python::arg("output") = ""));

  class_<AMX>("AMX", init<std::string>())
      .def_readonly("size", &AMX::size)
      ;
}
//-----------------------------------------------------------------------------
