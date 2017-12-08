//-----------------------------------------------------------------------------
#include "common.h"
//-----------------------------------------------------------------------------
namespace pawn {
#include "pawn/amx/amx.h"
}
//-----------------------------------------------------------------------------

class AMX
{
public:
  AMX(const string& filename);
  ~AMX();

  int NumNatives();
  int NumPublics();
  int NumPubVars();
  int NumTags();

  string GetPublic(int index);

private:
  string _filename;
  vector<uint8_t> _data;

  pawn::AMX _amx;
};
//-----------------------------------------------------------------------------

