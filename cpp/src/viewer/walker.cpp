#include <walker.h>

std::mt19937 eng(seed);
std::normal_distribution<float> normal_box(0.f, 1.f);

walkers::walkers(const int &nstep)
{
  this->nstep = nstep;
  this->x = std::make_unique<float[]>(nstep);
  this->y = std::make_unique<float[]>(nstep);
  this->z = std::make_unique<float[]>(nstep);
}
walkers::walkers(const walkers &w)
{
  this->nstep = w.nstep;
  this->x = std::make_unique<float[]>(w.nstep);
  this->y = std::make_unique<float[]>(w.nstep);
  this->z = std::make_unique<float[]>(w.nstep);

  std::copy_n(w.x.get(), w.nstep, this->x.get());
  std::copy_n(w.y.get(), w.nstep, this->y.get());
  std::copy_n(w.z.get(), w.nstep, this->z.get());
}
walkers& walkers::operator=(const walkers &w)
{
  this->nstep = w.nstep;
  this->x = std::make_unique<float[]>(w.nstep);
  this->y = std::make_unique<float[]>(w.nstep);
  this->z = std::make_unique<float[]>(w.nstep);

  std::copy_n(w.x.get(), w.nstep, this->x.get());
  std::copy_n(w.y.get(), w.nstep, this->y.get());
  std::copy_n(w.z.get(), w.nstep, this->z.get());
  return *this;
}


// https://it.mathworks.com/matlabcentral/fileexchange/54203-levy-n-m-beta
void walkers::levy(const float &beta)
{
#ifdef DEBUG
  assert(beta < 2.f && beta > 1.f);
#endif

  const float beta_inv = 1.f / beta;
  const float num = std::tgamma( 1.f + beta) * std::sin(3.141519f * beta * .5f); // used for Numerator
  const float den = std::tgamma((1.f + beta) * .5f) * beta * static_cast<float>(std::pow(2.f, (beta - 1.f) * .5f));
  const float sigma_u = static_cast<float>(std::pow(num / den, beta_inv));

  std::normal_distribution<float> normal2(0.f, sigma_u*sigma_u);

  this->x[0] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv));
  this->y[0] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv));
  this->z[0] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv));

  float m = std::max(std::max(std::fabs(this->x[0]), std::fabs(this->y[0])), std::fabs(this->z[0]));
  float mu_x = this->x[0],
        mu_y = this->y[0],
        mu_z = this->z[0];

  for (int i = 1; i < this->nstep; ++i)
  {
    this->x[i] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv)) + this->x[i - 1];
    this->y[i] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv)) + this->y[i - 1];
    this->z[i] = normal2(eng) / (std::pow(std::fabs(normal_box(eng)), beta_inv)) + this->z[i - 1];

    m = std::max(std::max(std::fabs(this->x[i]), std::fabs(this->y[i])), std::fabs(this->z[i]));
    mu_x += this->x[i];
    mu_y += this->y[i];
    mu_z += this->z[i];
  }

  mu_x /= this->nstep;
  mu_y /= this->nstep;
  mu_z /= this->nstep;
  m     = 1.f / m;

  for(int i = 0; i < this->nstep; ++i)
  {
    this->x[i] = (this->x[i] - mu_x) * m;
    this->y[i] = (this->y[i] - mu_y) * m;
    this->z[i] = (this->z[i] - mu_z) * m;
  }

}

