//-----------------------------------------------------------------------------
#include "compiler.h"
//-----------------------------------------------------------------------------
namespace pawn {
#include "pawn/compiler/sc.h"
}
//-----------------------------------------------------------------------------

void cc(string input, string output, string includes) {
  cout << __FUNCTION__ << " " << input << " " << output << " " << includes << endl;

  vector<string> args;
  args.push_back("pawncc");
  args.push_back(input);

  if(!output.empty()) {
    stringstream ss;
    ss << "-o" << output;
    args.push_back(ss.str());
  }

  if(!includes.empty()) {
    stringstream ss;
    ss << "-i" << includes;
    args.push_back(ss.str());
  }

  vector<char*> argv;
  for(auto& s: args) {
    argv.push_back(&s[0]);
  }
  argv.push_back(NULL);
  pawn::pc_compile(argv.size() - 1, &argv[0]);
}
//-----------------------------------------------------------------------------
