//-----------------------------------------------------------------------------
#include <iostream>
#include <fstream>
#include <sstream>
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

void cc(string input, string output = "") {
  cout << __FUNCTION__ << " " << input << " " << output << endl;

  vector<string> args;
  args.push_back(input);

  if(!output.empty()) {
    stringstream ss;
    ss << "-o " << output;
    args.push_back(ss.str());
  }

  vector<char*> argv;
  for(auto s: args) {
    argv.push_back(const_cast<char*>(s.c_str()));
  }
  //pawn::pc_compile(argv.size(), argv.data());
}
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
