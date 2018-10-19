#ifndef WOA_H
#define WOA_H
#ifdef VERBOSE
#include <iostream>
#endif
#include <memory>
#include <chrono>
#include <random>
#include <climits>

static constexpr float inf = std::numeric_limits<float>::infinity();

namespace walker
{
  template<typename Func>
  auto woa(Func objfunc,
           const float &lower_bound,
           const float &upper_bound,
           const int &dim,
           const int &n_population,
           const int &max_iters,
           float b = 1.f,
           std::size_t seed = 0,
           int verbose = 1,
           int nth = 4)
  {
    typedef std::pair<int, float> best_idx;
    int iteration = 0;
    best_idx leader;
    float fitness;

    std::unique_ptr<float*, std::function<void(float**)>> positions(new float*[n_population](),
                                                                    [&](float** x)
                                                                    {
                                                                      std::for_each(x, x + dim, std::default_delete<float[]>());
                                                                      delete[] x;
                                                                    });

    solution s(n_population, max_iters, "WOA");

    std::mt19937 engine(seed);
    std::uniform_real_distribution<float> bound_rng(lower_bound, upper_bound);
    std::uniform_real_distribution<float> rng(0.f, 1.f);

    // Initialize timer for the experiment
    auto timer = std::chrono::high_resolution_clock::now();
    s.start_time = timer;

#ifdef VERBOSE
    std::cout << "WOA is optimizing..." << std::endl;
#endif

#ifdef _OPENMP
#pragma omp declare reduction (minPair : best_idx : omp_out = omp_in.second < omp_out.second ? omp_in : omp_out) initializer(omp_priv = omp_orig)
#pragma omp parallel num_threads(nth) private(fitness)
  {
#endif

#ifdef _OPENMP
#pragma omp for
    for (int i = 0; i < n_population; ++i) (positions.get()) = new float[dim];
#else
    std::generate_n(positions.get(), n_population, [](){return new float[dim];});
#endif

    // initialize the positions/solutions
#ifdef _OPENMP
#pragma omp for collapse(2)
#endif
    for (int i = 0; i < n_population; ++i)
      for (int j = 0; j < dim; ++j)
        positions[i][j] = bound_rng(engine);

    // main loop
    while(iteration < max_iters)
    {
      leader.second = inf;
      leader.first  = 0;
#ifdef _OPENMP
#pragma omp for reduction(minPair : leader)
#endif
      for (int i = 0; i < n_population; ++i)
      {
        // compute objective function for each search agent
        fitness = fit(population[i]);
        // update the leader
        leader.first  = fitness < leader.second ? i       : leader.first; // update alpha
        leader.second = fitness < leader.second ? fitness : leader.second;
      }

      float a  = 2.f - iteration * (2.f / max_iters); // a decreases linearly from 2 to 0 in Eq. (2.3)
      float a2 = 1.f + iteration * (-1.f / max_iters);// a2 linearly decreases from -1 to -2 to calculate t in Eq. (3.12)

      // update the position of search agents
#ifdef _OPENMP
#pragma omp for
#endif
      for (int i = 0; i < n_population; ++i)
      {
        float r1 = rng(engine);
        float r2 = rng(engine);

        float A    = 2.f * a * r1 - a; // Eq. (2.3) in the paper
        float C    = 2.f * r2;         // Eq. (2.4) in the paper
        float l    = (a2 - 1.f) * rng(engine) + 1.f; // parameters in Eq. (2.5)
        bool p     = static_cast<bool>(rng(engine) > .5f);      // Eq. (2.6)
        bool a_abs = static_cast<bool>(std::fabs(A) >= 1.f);

        for (int j = 0; j < dim; ++j)
        {
          position[i][j] = (p && a_abs)  ? position[][j] - A * std::fabs(C * position[][j] - position[i][j])                         :
                           (p && !a_abs) ? position[leader.first][j] - A * std::fabs(C * position[leader.first][j] - position[i][j]) :
                            std::fabs(position[leader.first][j] - position[i][j]) * std::exp(b * l) * std::cos(l * 2.f * M_PI) + position[leader.first][j];
          positions[i][j] = (positions[i][j] < lower_bound) ? lower_bound :
                            (positions[i][j] > upper_bound) ? upper_bound :
                             positions[i][j];
        }
      }

      s.walk[iteration] = positions[leader.first];

#ifdef _OPENMP
#pragma omp single
#endif
      ++iteration;
    } // end while

#ifdef _OPENMP
  } // end parallel section
#endif

    timer = std::chrono::high_resolution_clock::now();
    s.end_time = timer;
    s.execution_time = std::chrono::duration_cast<std::chrono::seconds>(s.end_time - s.start_time).count();
    s.best = leader.second;

    return s;
  }

#endif // WOA_H
