/**
 * A catalyst adaptor for LULESH
 */

#include "lulesh.h"

#ifndef lulesh_catalyst_h
#define lulesh_catalyst_h

namespace adaptor
{
void initialize(int rank, int numranks, const std::vector<std::string>& scripts);
void process(Domain& domain);
void finalize();
}

#endif
