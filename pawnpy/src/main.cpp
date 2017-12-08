//-----------------------------------------------------------------------------
#include "amx.h"
#include "compiler.h"
//-----------------------------------------------------------------------------
namespace py = boost::python;
using namespace py;
//-----------------------------------------------------------------------------

void translator(exception const& e) {
  PyErr_SetString(PyExc_RuntimeError, e.what());
}
//-----------------------------------------------------------------------------

class PyAMX : public class_<AMX> {
public:
  PyAMX() : class_<AMX>("AMX", init<std::string>()) {
  };
};
//-----------------------------------------------------------------------------

BOOST_PYTHON_MODULE(pawnpy) {
  register_exception_translator<exception>(translator);

  def("cc", cc, (py::arg("input"),
                 py::arg("output") = "",
                 py::arg("includes") = ""));

  PyAMX();
}
//-----------------------------------------------------------------------------
