#ifndef SOLUTION_H
#define SOLUTION_H
#include <memory>

struct solution
{
  int popsize           = 0;
  int maxiters          = 0;
  float best            = 0.f;
  float execution_time  = 0.f;
  std::string optimizer = "";
  std::unique_ptr<float[]> walk;

  solution(const int &popsize, const int &iters, const std::string &opt)
  {
    this->popsize   = popsize;
    this->maxiters  = iters;
    this->optimizer = opt;
    this->step = std::make_unique<float[]>(iters);
  };
};

#endif // SOLUTION_H
