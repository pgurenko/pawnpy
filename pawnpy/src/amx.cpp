//-----------------------------------------------------------------------------
#include "amx.h"
//-----------------------------------------------------------------------------

class IOError : exception
{
public:
  const char* what() throw() { return "IOError"; }
};
//-----------------------------------------------------------------------------

AMX::AMX(const string& filename) throw()
  : _filename(filename) {
  cout << __FUNCTION__ <<  " filename=" << _filename << endl;

  ifstream file(filename, ios::in);
  if(!file.is_open())
    throw IOError();

  file.seekg (0, ios::end);
  size_t size = file.tellg();
  _data.resize(size);
  cout << size << endl;
  file.seekg (0, ios::beg);
  file.read (reinterpret_cast<char*>(_data.data()), size);
  file.close();

  _hdr = reinterpret_cast<pawn::AMX_HEADER*>(_data.data());
}
//-----------------------------------------------------------------------------

int32_t publics;          /* offset to the "public functions" table */
int32_t natives;          /* offset to the "native functions" table */
int32_t libraries;        /* offset to the table of libraries */
int32_t pubvars;          /* offset to the "public variables" table */
int32_t tags;             /* offset to the "public tagnames" table */
int32_t nametable;        /* offset to the name table */
int32_t overlays;         /* offset to the overlay table */

int32_t AMX::size() const {
  return _hdr->size;
}
//-----------------------------------------------------------------------------
