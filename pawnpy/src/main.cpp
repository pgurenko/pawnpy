//-----------------------------------------------------------------------------
#include <iostream>
#include <fstream>
#include <boost/python.hpp>
//-----------------------------------------------------------------------------
namespace pawn {
#include "pawn/compiler/sc.h"
#include "pawn/amx/amx.h"
}
//-----------------------------------------------------------------------------
using namespace std;
using namespace boost::python;
//-----------------------------------------------------------------------------

class IOError : exception
{
public:
  const char* what() throw() { return "IOError"; }
};
//-----------------------------------------------------------------------------

class AMX
{
public:
  AMX(const string& filename) throw()
    : _filename(filename) {
    cout << __FUNCTION__ <<  " filename=" << _filename << endl;

    ifstream file(filename);
    if(!file.is_open())
      throw IOError();

    size_t size = file.tellg();
    _data.resize(size);
    file.seekg (0, ios::beg);
    file.read (reinterpret_cast<char*>(_data.data()), size);
    file.close();

    _hdr = reinterpret_cast<pawn::AMX_HEADER*>(_data.data());
  }

  int32_t size() const {
    return _hdr->size;
  }

private:
  string _filename;
  vector<uint8_t> _data;

  pawn::AMX_HEADER* _hdr;
};
//-----------------------------------------------------------------------------

int cc()
{
  cout << __FUNCTION__ << endl;
  // filling proper argc and argv based on parameters
  return pawn::pc_compile(0, NULL);
}
//-----------------------------------------------------------------------------

void translator(exception const& e) {
  PyErr_SetString(PyExc_RuntimeError, e.what());
}
//-----------------------------------------------------------------------------

BOOST_PYTHON_MODULE(pawnpy) {
  register_exception_translator<exception>(translator);

  def("cc", cc);

  class_<AMX>("AMX", init<std::string>())
      .def_readonly("size", &AMX::size)
      ;
}
//-----------------------------------------------------------------------------
