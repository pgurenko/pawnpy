//-----------------------------------------------------------------------------
#include "compiler.h"
//-----------------------------------------------------------------------------
namespace pawn {
#include "pawn/compiler/sc.h"
}
//-----------------------------------------------------------------------------

void cc(string input, string output) {
  cout << __FUNCTION__ << " " << input << " " << output << endl;

  vector<string> args;
  args.push_back("pawnpyTest");
  args.push_back(input);

  if(!output.empty()) {
    stringstream ss;
    ss << "-o" << output;
    args.push_back(ss.str());
  }

  vector<char*> argv;
  for(auto& s: args) {
    argv.push_back(&s[0]);
  }
  argv.push_back("\0");
  pawn::pc_compile(argv.size(), argv.data());
}
//-----------------------------------------------------------------------------
