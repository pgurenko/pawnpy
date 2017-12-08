//-----------------------------------------------------------------------------
#include "amx.h"
//-----------------------------------------------------------------------------

class IOError : exception
{
private:
  string _filename;
public:
  IOError(string filename) : _filename(filename) {}
  string what() {
    stringstream ss;
    ss << "Could not open " << _filename;
    return ss.str();
  }
};
//-----------------------------------------------------------------------------

class AMXError : exception
{
private:
  int _err;
public:
  AMXError(int err) : _err(err) {}
  string what() {
    stringstream ss;
    ss << "AMX error code=" << _err;
    return ss.str().c_str();
  }
};
//-----------------------------------------------------------------------------

AMX::AMX(const string& filename)
  : _filename(filename) {
  cout << __FUNCTION__ <<  " filename=" << _filename << endl;

  ifstream file(filename, ios::in);
  if(!file.is_open())
    throw IOError(_filename);

  pawn::AMX_HEADER hdr;
  file.read(reinterpret_cast<char*>(&hdr), sizeof(pawn::AMX_HEADER));
  if (hdr.magic != AMX_MAGIC)
    throw AMXError(pawn::AMX_ERR_FORMAT);

  file.seekg (0, ios::end);
  size_t size = file.tellg();
  _data.resize(size);
  file.seekg (0, ios::beg);
  file.read (reinterpret_cast<char*>(_data.data()), size);
  file.close();

  memset(&_amx, 0, sizeof(pawn::AMX));

  int result = pawn::amx_Init(&_amx, _data.data());
  if (result != pawn::AMX_ERR_NONE)
    throw AMXError(result);
}
//-----------------------------------------------------------------------------

AMX::~AMX() {
  if (_amx.base!=NULL) {
    amx_Cleanup(&_amx);
    memset(&_amx, 0, sizeof(pawn::AMX));
  }
}
//-----------------------------------------------------------------------------

int AMX::NumNatives() {
  int number = 0;
  int result = pawn::amx_NumNatives(&_amx, &number);
  if (result != pawn::AMX_ERR_NONE) {
    throw AMXError(result);
  }
  return number;
}
//-----------------------------------------------------------------------------

int AMX::NumPublics() {
  int number = 0;
  int result = pawn::amx_NumPublics(&_amx, &number);
  if (result != pawn::AMX_ERR_NONE)
    throw AMXError(result);
  return number;
}
//-----------------------------------------------------------------------------

int AMX::NumPubVars() {
  int number = 0;
  int result = pawn::amx_NumPubVars(&_amx, &number);
  if (result != pawn::AMX_ERR_NONE)
    throw AMXError(result);
  return number;
}
//-----------------------------------------------------------------------------

int AMX::NumTags() {
  int number = 0;
  int result = pawn::amx_NumTags(&_amx, &number);
  if (result != pawn::AMX_ERR_NONE)
    throw AMXError(result);
  return number;
}
//-----------------------------------------------------------------------------

string AMX::GetPublic(int index) {
  char name[sNAMEMAX+1];
  int result = pawn::amx_GetPublic(&_amx, index, name, NULL);
  if (result != pawn::AMX_ERR_NONE)
    throw AMXError(result);
  return string(name);
}
//-----------------------------------------------------------------------------
