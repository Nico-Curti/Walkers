#ifndef LANDSCAPE_H
#define LANDSCAPE_H

#include <cmath>
#include <array>
#include <numeric>
#include <algorithm>
#ifdef DEBUG
#include <assert.h>
#endif

#ifndef M_PI
static constexpr float M_PI = 3.14159265358979323846f;
#endif

struct
{
private:
  const float a = 20.f;
  const float b = .2f;
  const float c = M_PI * 2.f;
  const float e_1 = std::exp(1);

public:
  const float lb = -32.768f;
  const float ub =  32.768f;

  template<int D = 2> auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float s_ = std::accumulate(x, x + dim, 0.f);
    float c_ = std::accumulate(x, x + dim, 0.f, [&](const float &r, const float &i){return r + std::cos(c * i);});
    return -a * std::exp(-b * std::sqrt(s_) / dim) - std::exp(c_ / dim) + a + e_1;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 0.f);
    return minimum;
  }

} Ackley;


struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return (x[0] + 2.f * x[1] - 7.f) * (x[0] + 2.f * x[1] - 7.f) +
           (2.f * x[0] + x[1] - 5.f) * (2.f * x[0] + x[1] - 5.f);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {1.f, 3.f} };
    return minimum;
  }

} Booth;

struct
{
  const float lb = -15.f;
  const float ub =  3.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return 100.f * std::sqrt(std::fabs(x[1] - 1e-2f * x[0]*x[0])) + 1e-2f * std::fabs(x[1] + 10.f);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {-10.f, 1.f} };
    return minimum;
  }

} BukinN6;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float * x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return -1e-4f * std::pow(std::fabs(std::sin(x[0]) * std::sin(x[0]) * std::exp(std::fabs(100.f - std::sqrt(x[0]*x[0] + x[1]*x[1]) / M_PI))) + 1.f, 1e-1f);
  }

  auto get_minimum()
  {
    std::array<std::array<float, 4>, 2> minimum;
    minimum[0][0] =  1.3491f; minimum[0][1] = -1.3491f;
    minimum[1][0] =  1.3491f; minimum[1][1] =  1.3491f;
    minimum[2][0] = -1.3491f; minimum[2][1] =  1.3491f;
    minimum[3][0] = -1.3491f; minimum[3][1] = -1.3491f;
    return minimum;
  }

} CrossInTray;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float s = 0.f;
    for (int i = 0; i < dim; ++i) s += (i + 2) * x[i + 1]*x[i + 1] - x[i]*x[i];
    return (x[0] - 1.f) * (x[0] - 1.f) + s;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    float idx;
    for (int i = 0; i < D; ++i)
    {
      idx = std::pow(2.f, i + 1);
      minimum[i] = std::pow(2.f, -(idx - 2.f) / idx);
    }
    return minimum;
  }

} DixonPrice;

struct
{
  const float lb = -5.12f;
  const float ub =  5.12f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float a2 = x[0]*x[0] + x[1]*x[1];
    return - (1.f + std::cos(12.f * std::sqrt(a2))) / (.5f * a2 + 2.f);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {0.f, 0.f} };
    return minimum;
  }

} DropWave;

struct
{
  const float lb = -512.f;
  const float ub =  512.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return -(x[1] + 47.f) * std::sin(std::sqrt(std::abs(x[1] + .5f * x[0] + 47.f))) - x[0] * std::sin(std::sqrt(std::abs(x[0] - (x[1] + 47.f))));
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {512.f, 404.2319f} };
    return minimum;
  }

} Eggholder;


struct
{
  const float lb = -.5f;
  const float ub =  2.5f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 1);
#endif
    return .5f * std::sin(10.f * M_PI * x[0]) / x[0] + (x[0] - 1.f)*(x[0] - 1.f)*(x[0] - 1.f)*(x[0] - 1.f);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum; // around { {.6f, -.9f} };
    return minimum;
  }

} GramacyLee;

struct
{
  const float lb = -600.f;
  const float ub =  600.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float s = 0.f,
          p = 1.f;

    for (int i = 0; i < dim; ++i)
    {
      s += x[i] * x[i] * .00025f;
      p *= std::cos(x[i] / std::sqrt(i + 1.f));
    }
    return s - p + 1.f;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 0.f);
    return minimum;
  }

} GrieWank;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float s = 0.f,
          p = 1.f;

    for (int i = 0; i < dim; ++i)
    {
      s += x[i] * x[i] * .00025f;
      p *= std::cos(x[i] / std::sqrt(i + 1.f));
    }
    return s - p + 1.f;
  }

  auto get_minimum()
  {
    std::array<std::array<float, 4>, 2> minimum;
    minimum[0][0] =  8.05502f; minimum[0][1] =  9.66459f;
    minimum[1][0] =  8.05502f; minimum[1][1] = -9.66459f;
    minimum[2][0] = -8.05502f; minimum[2][1] =  9.66459f;
    minimum[3][0] = -8.05502f; minimum[3][1] =-9.66459f;
    return minimum;
  }

} HolderTable;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return .26f * std::inner_product(x, x + dim, x, 0.f) - .48f * x[0] * x[1];
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {0.f, 0.f} };
    return minimum;
  }

} Matyas;

struct
{
  // x belongs to [-1.5f, 4.f]
  // y belongs to [-3.f,  4.f]
  const float lb = -3.f;
  const float ub =  4.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    return std::sin(std::accumulate(x, x + dim, 0.f)) + (x[0] - x[1])*(x[0] - x[1]) - 1.5f * x[0] + 2.5f * x[1] + 1.f;
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {0.f, 0.f} };
    return minimum;
  }

} McCormick;


struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float w0 = std::sin(M_PI       * 1.f + (x[0]       - 1.f) * .25f),
          wl = std::sin(M_PI * 2.f * 1.f + (x[dim - 1] - 1.f) * .25f),
          wi, tmp,
          s  = 0.f;

    for (int i = 0; i < dim - 1; ++i)
    {
      wi = 1.f + (x[i] - 1.f) * .25f;
      tmp = std::sin(M_PI * wi + 1.);
      s += (wi - 1.f)*(wi - 1.f) * (1.f + 10.f * tmp * tmp);
    }

    return w0*w0 + s + (1.f + (x[dim - 1] - 1.f) * .25f)*(1.f + (x[dim - 1] - 1.f) * .25f) * wl*wl;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 1.f);
    return minimum;
  }

} Levy;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float w0 = std::sin(3.f * M_PI * x[0]),
          w1 = std::sin(3.f * M_PI * x[1]),
          w2 = std::sin(2.f * M_PI * x[1]);

    return w0*w0 + (x[0] - 1.f)*(x[0] - 1.f) * (1.f + w1*w1) + (x[1] - 1.f)*(x[1] - 1.f) * (1.f + w2*w2);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {1.f, 1.f} };
    return minimum;
  }

} LevyN13;

struct
{
  const float lb = -5.12f;
  const float ub =  5.12f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    return 10.f * D + std::accumulate(x, x + dim, 0.f, [](const float &res, const float xi){return res + xi*xi - 10.f * std::cos(2.f * M_PI * xi);});
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 0.f);
    return minimum;
  }

} Rastring;

struct
{
  const float lb = -5.f;
  const float ub =  10.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float s = 0.f;
    for (int i = 0; i < dim - 1; ++i) s += 100.f * (x[i + 1] - x[i]*x[i]) * (x[i + 1] - x[i]*x[i]) + (x[i] - 1.f)*(x[i] - 1.f);
    return s;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 1.f);
    return minimum;
  }

} Rosenbrock;

struct
{
  const float lb = -100.f;
  const float ub =  100.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float den = 1.f + 1e-3f*(x[0]*x[0] + x[1]*x[1]);
    return .5f * (std::sin(x[0]*x[0] - x[1]*x[1]) - .5f) / ( den*den );
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {0.f, 0.f} };
    return minimum;
  }

} SchafferN2;

struct
{
  const float lb = -100.f;
  const float ub =  100.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float den = 1.f + 1e-3f*(x[0]*x[0] + x[1]*x[1]);
    return .5f + (std::cos(std::sin(std::abs(x[0]*x[0] - x[1]*x[1]))) - .5f) / (den * den);
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {inf, inf} };
    return minimum;
  }

} SchafferN4;

struct
{
  const float lb = -500.f;
  const float ub =  500.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif

    return 418.9829 * D - std::accumulate(x, x + dim, 0.f, [](const float &res, const float &xi){return res + xi * std::sin(std::sqrt(std::abs(xi)));});
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 420.9687f);
    return minimum;
  }

} Schwefel;

struct
{
  const float lb = -10.f;
  const float ub =  10.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float s1 = 0.f,
          s2 = 0.f;
    for (int i = 1; i < 6; ++i)
    {
      s1 += i * std::cos( (i + 1) * x[0] + i );
      s2 += i * std::cos( (i + 1) * x[1] + i );
    }
    return s1 * s2;
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum{ {inf, inf} };
    return minimum;
  }

} Shubert;

struct
{
  const float lb = -3.f;
  const float ub =  3.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float x2 = x[0]*x[0];
    return x2 * (4.f - 2.1f * x2 + x2*x2 * .333333333f) + x[0]*x[1] + (-4.f + 4.f * x[1]*x[1]) * std::pow(x[1], x[1]);
  }

  auto get_minimum()
  {
    std::array<std::array<float, 2>, 2> minimum;
    minimum[0][0] =  .0898f; minimum[0][1] = -.7126f;
    minimum[1][0] = -.0898f; minimum[1][1] = .7126f;
    return minimum;
  }

} SixHumpCamel;

struct
{
  const float lb = -5.f;
  const float ub =  5.f;

  auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == 2);
#endif
    float x2 = x[0]*x[0],
          x4 = x2 * x2;
    return 2.f * x2 - 1.05f * x4 + .1666666666666f * x4*x2 + x[0]*x[1] + x[1]*x[1];
  }

  auto get_minimum()
  {
    std::array<float, 2> minimum;
    std::fill(minimum.begin(), minimum.end(), 0.f);
    return minimum;
  }

} ThreeHumpCamel;

struct
{
  const float lb = -5.f;
  const float ub =  10.f;

  template<int D = 2> auto operator()(const float *x, const int &dim)
  {
#ifdef DEBUG
    assert(dim == D);
#endif
    float s1 = 0.f,
          s2 = 0.f;

    for (int i = 0; i < dim; ++i)
    {
      s1 += x[i]*x[i];
      s2 += .5f * (i + 1) * x[i];
    }
    s2 *= s2;
    return s1 + s2 + s2*s2;
  }

  template<int D = 2> auto get_minimum()
  {
    std::array<float, D> minimum;
    std::fill(minimum.begin(), minimum.end(), 0.f);
    return minimum;
  }

} Zakharov;

#endif // LANDSCAPE_H
