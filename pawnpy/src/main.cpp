//-----------------------------------------------------------------------------
#include <iostream>
#include <boost/python.hpp>
//-----------------------------------------------------------------------------
namespace pawn {
#include "pawn/compiler/sc.h"
}
//-----------------------------------------------------------------------------
using namespace std;
using namespace boost::python;
//-----------------------------------------------------------------------------

class File
{
public:
  File(const std::string& filename)
    : _filename(filename) {
    cout << __FUNCTION__ <<  " filename=" << _filename << endl;
  }
private:
  std::string _filename;
};
//-----------------------------------------------------------------------------

class AMX : public File
{
public:
  AMX(const std::string& filename)
    : File(filename) {
  }
};
//-----------------------------------------------------------------------------

class Source : public File
{
public:
  Source(const std::string& filename)
    : File(filename)
  {
  }

  int compile()
  {
    cout << __FUNCTION__ << endl;
    // filling proper argc and argv based on parameters
    return pawn::pc_compile(0, NULL);
  }

  int set_breakpoint(uint32_t line) {
    cout << __FUNCTION__ << " - line " << line << endl;
    return true;
  }
};
//-----------------------------------------------------------------------------

BOOST_PYTHON_MODULE(pawnpy)
{
    class_<Source>("Source", init<std::string>())
        .def("compile", &Source::compile)
        .def("set_breakpoint", &Source::set_breakpoint)
        ;

    class_<AMX>("AMX", init<std::string>())
        ;
}
//-----------------------------------------------------------------------------
