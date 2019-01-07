#ifndef WALKER_H
#define WALKER_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <array>
#include <chrono>
#include <random>
#include <climits>
#include <algorithm>
#include <numeric>
#include <utility>
#include <functional>

#include <solution.h>

static constexpr float inf = std::numeric_limits<float>::infinity();

#include <bat.hpp>
#include <bbo.hpp>
#include <cfa.hpp>
#include <cs.hpp>
#include <gwo.hpp>
#include <pso.hpp>
#include <ssa.hpp>
#include <woa.hpp>

#endif // WALKER_H
