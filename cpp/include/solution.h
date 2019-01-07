#ifndef SOLUTION_H
#define SOLUTION_H
#include <memory>

struct Solution
{
  int dim;
  int popsize;
  int maxiters;
  float best;
  float execution_time;
  std::shared_ptr<std::shared_ptr<float[]>[]> walk;
  std::string optimizer;

  Solution() : dim(0), popsize(0), maxiters(0), best(0.f), execution_time(0.f), walk(nullptr), optimizer("")
  {};
  Solution(const int &popsize, const int &dim, const int &iters, const std::string &opt)
  {
    this->dim       = dim;
    this->popsize   = popsize;
    this->maxiters  = iters;
    this->optimizer = opt;
    this->walk.reset( new std::shared_ptr<float[]>[iters] );
  };
  ~Solution() = default;
};

#endif // SOLUTION_H
