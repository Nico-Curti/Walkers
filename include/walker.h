#ifndef WALKER_H
#define WALKER_H
#include <memory>
#include <algorithm>
#include <cmath>
#include <random>
#ifdef DEBUG
#include <cassert>
#endif

static constexpr int seed = 123;

struct walkers
{
  int nstep;
  std::unique_ptr<float[]> x, y, z;

  walkers(){};
  walkers(const int &nstep);
  walkers(const walkers &w);
  walkers& operator=(const walkers &w);

  void levy(const float &beta);
};

#endif // WALKER_H
