#ifndef LANDSCAPE_H
#define LANDSCAPE_H

#include <cmath>
#include <numeric>
#include <algorithm>
#ifdef DEBUG
#include <assert.h>
#endif

struct
{
private:
  static constexpr float a = 20.f;
  static constexpr float b = .2f;
  static constexpr float c = M_PI * 2.f;
  static constexpr float e_1 = std::exp(1);

public:
  static constexpr float lb = -32.768f;
  static constexpr float ub =  32.768f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float s_ = std::accumulate(x, x + dim, 0.f);
    float c_ = std::accumulate(x, x + dim, 0.f, [&](const float &r, const float &i){return r + std::cos(c * i);});
    return -a * std::exp(-b * std::sqrt(s_) / dim) - std::exp(c_ / dim) + a + e_1;
  }

} Ackley;


struct
{
  static constexpr float lb = -10.f;
  static constexpr float ub =  10.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return (x[0] + 2.f * x[1] - 7.f) * (x[0] + 2.f * x[1] - 7.f) +
           (2.f * x[0] + x[1] - 5.f) * (2.f * x[0] + x[1] - 5.f);
  }

} Booth;

struct
{
  static constexpr float lb = -15.f;
  static constexpr float ub =  3.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return 100.f * std::sqrt(std::fabs(x[1] - 1e-2f * x[0]*x[0])) + 1e-2f * std::fabs(x[1] + 10.f);
  }

} BukinN6;

struct
{
  static constexpr float lb = -10.f;
  static constexpr float ub =  10.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return -1e-4f * std::pow(std::fabs(std::sin(x[0]) * std::sin(x[0]) * std::exp(std::fabs(100.f - std::sqrt(x[0]*x[0] + x[1]*x[1]) / M_PI))) + 1.f, 1e-1f);
  }

} CrossInTray;

#endif // LANDSCAPE_H
