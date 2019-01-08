#ifndef WALKER_H
#define WALKER_H

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

#ifdef _OPENMP
#include <omp.h>
#include <merge_sort.h>
#endif

#ifdef VERBOSE
#include <iostream>
#include <iomanip>

static constexpr int PBWIDTH = 50;
auto printProgress = [](const float &now, const int &total, const std::chrono::high_resolution_clock::time_point &start_time)
                      {
                        float perc = now / total;
                        int lpad = static_cast<int>(perc * PBWIDTH);
                        std::cout << "\rOptimization progress:"
                                  << std::right << std::setw(5) << std::setprecision(3) << perc * 100.f << "%  ["
                                  << std::left  << std::setw(PBWIDTH - 1) << std::string(lpad, '|') << "] "
                                  << std::right << std::setw(5) << int(now) << "/" << std::setprecision(5) << total
                                  << " [" << std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - start_time).count() << " sec]";
                        std::cout << std::flush;
                      };
#endif // VERBOSE

#include <bat.hpp>
#include <bbo.hpp>
#include <cfa.hpp>
#include <cs.hpp>
#include <gwo.hpp>
#include <pso.hpp>
#include <ssa.hpp>
#include <woa.hpp>

#endif // WALKER_H
