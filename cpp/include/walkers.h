#ifndef WALKER_H
#define WALKER_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <chrono>
#include <random>
#include <climits>
#include <algorithm>
#include <numeric>
#include <utility>
#include <functional>

#include <solution.h>

static constexpr float inf = std::numeric_limits<float>::infinity();

namespace walker
{
  template<typename Func>
  solution bat(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, float A = .5f,             float r = .5f,             float Qmin = 0.f,          float Qmax = 2.f,          float step = 1e-3f,        std::size_t seed = 0, int verbose = 1, int nth = 4 );

  template<typename Func>
  solution cfa(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, std::size_t seed = 0, int verbose = 1, int nth = 4);

  template<typename Func>
  solution cs(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, float pa = .25f, std::size_t seed = 0, int verbose = 1, int nth = 4 );

  template<typename Func>
  solution gwo(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, std::size_t seed = 0, int verbose = 1, int nth = 4);

  template<typename Func>
  solution pso(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, float Vmax = 6.f, float wmax = .9f, float wmin = .2f, float c1   = 2.f, float c2   = 2.f, std::size_t seed = 0, int verbose = 1, int nth = 4);

  template<typename Func>
  solution woa(Func objfunc, const float &lower_bound, const float &upper_bound, const int &dim, const int &n_population, const int &max_iters, float b = 1.f, std::size_t seed = 0, int verbose = 1, int nth = 4);
}


#endif // WALKER_H
