#ifndef SOLUTION_H
#define SOLUTION_H
#include <memory>

struct solution
{
  int dim               = 0;
  int popsize           = 0;
  int maxiters          = 0;
  float best            = 0.f;
  float execution_time  = 0.f;
  float **walk          = nullptr;
  std::string optimizer = "";

  solution(const int &popsize, const int &dim, const int &iters, const std::string &opt)
  {
    this->dim       = dim;
    this->popsize   = popsize;
    this->maxiters  = iters;
    this->optimizer = opt;
    this->walk = new float*[iters];
    //std::generate_n(this->walk, iters, [](){return new float[dim];})
  };
  ~solution()
  {
    if (walk)
    {
      for (int i = 0; i < this->maxiters; ++i) delete[] this->walk[i];
      delete[] this->walk;
    }
  }
};

#endif // SOLUTION_H
