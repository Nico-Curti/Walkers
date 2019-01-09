#include <draw.h>
#include <sphere.h>
#include <walkers.h>
#include <landscape.h>
#include <iostream>

enum { _bat = 0,
       _bbo,
       _cfa,
       _cs,
       _gwo,
       _pso,
       _ssa,
       _woa
}; // optimizers

enum { _Ackley = 0,
       _Booth,
       _BukinN6,
       _CrossInTray,
       _DixonPrice,
       _DropWave,
       _Eggholder,
       _GramacyLee,
       _GrieWank,
       _HolderTable,
       _Levy,
       _LevyN13,
       _Matyas,
       _McCormick,
       _Rastring,
       _Rosenbrock,
       _SchafferN2,
       _SchafferN4,
       _Schwefel,
       _Shubert,
       _SixHumpCamel,
       _ThreeHumpCamel,
       _Zakharov
}; // landscape functions

static constexpr int n_population = 50;
static constexpr int max_iters    = 500;
Solution sol;
float max_x, max_y, max_z;
float min_x, min_y, min_z;
static SolidSphere sphere(.02f, 12, 24);

static constexpr float MAX_W = 2.f; // aka (1.f - (-1.f))
static constexpr float MIN_W = 1.f;

void display()
{
  float x, y, z;
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear color and depth buffers
  glMatrixMode(GL_MODELVIEW);                         // To operate on model-view matrix
                                                      // Clear window and null buffer Z
                                                      // glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                                                      // Reset transformation
  glLoadIdentity();

  glPushMatrix();
  glRotatef(rotate_x, 1.0, 0.0, 0.0);
  glRotatef(rotate_y, 0.0, 1.0, 0.0);
  glTranslated(transl_x, transl_y, 0.f);
  glScalef(zoom, zoom, zoom);
  x = ((sol.walk[0][0] - min_x) / (max_x - min_x))*MAX_W - MIN_W;
  y = ((sol.walk[0][1] - min_y) / (max_y - min_y))*MAX_W - MIN_W;
  z = ((sol.walk[0][2] - min_z) / (max_z - min_z))*MAX_W - MIN_W;
  x = ( std::isnan(x) || std::isinf(x) ) ? 0.f : x;
  y = ( std::isnan(y) || std::isinf(y) ) ? 0.f : y;
  z = ( std::isnan(z) || std::isinf(z) ) ? 0.f : z;
  sphere.draw( x, y, z, 1, 1, 1);

  x = ((sol.walk[max_iters - 1][0] - min_x) / (max_x - min_x))*MAX_W - MIN_W;
  y = ((sol.walk[max_iters - 1][1] - min_y) / (max_y - min_y))*MAX_W - MIN_W;
  z = ((sol.walk[max_iters - 1][2] - min_z) / (max_z - min_z))*MAX_W - MIN_W;
  x = ( std::isnan(x) || std::isinf(x) ) ? 0.f : x;
  y = ( std::isnan(y) || std::isinf(y) ) ? 0.f : y;
  z = ( std::isnan(z) || std::isinf(z) ) ? 0.f : z;

  sphere.draw( x, y, z, 1, 0, 0);
  glPopMatrix();

  glPushMatrix();
  glRotatef(rotate_x, 1.0, 0.0, 0.0);
  glRotatef(rotate_y, 0.0, 1.0, 0.0);
  glTranslated(transl_x, transl_y, 0.f);
  glScalef(zoom, zoom, zoom);
  glBegin(GL_LINE_STRIP);
  glNormal3f(1.f, 1.f, 1.f);
  glColor3f(1.f, 1.f, 1.f);

  for (int i = 0; i < max_iters; ++i)
  {
    x = ((sol.walk[i][0] - min_x) / (max_x - min_x))*MAX_W - MIN_W;
    y = ((sol.walk[i][1] - min_y) / (max_y - min_y))*MAX_W - MIN_W;
    z = ((sol.walk[i][2] - min_z) / (max_z - min_z))*MAX_W - MIN_W;
    x = ( std::isnan(x) || std::isinf(x) ) ? 0.f : x;
    y = ( std::isnan(y) || std::isinf(y) ) ? 0.f : y;
    z = ( std::isnan(z) || std::isinf(z) ) ? 0.f : z;
    glVertex3f(x, y, z);
  }
  glEnd();
  glPopMatrix();

  glFlush();
  glutSwapBuffers();
}


static void usage()
{
  std::cout << "Walkers example usage: ./run optimizer landscape"    << std::endl
            << std::endl
            << "positional arguments:"                               << std::endl
            << "   optimizer          Optimizer type as integer"     << std::endl
            << "   landscape          Landscape function as integer" << std::endl
            << std::endl
            << "List of Optimizers:"                                 << std::endl
            << "   0   ->  bat"                                      << std::endl
            << "   1   ->  bbo"                                      << std::endl
            << "   2   ->  cfa"                                      << std::endl
            << "   3   ->  cs"                                       << std::endl
            << "   4   ->  gwo"                                      << std::endl
            << "   5   ->  pso"                                      << std::endl
            << "   6   ->  ssa"                                      << std::endl
            << "   7   ->  woa"                                      << std::endl
            << std::endl
            << std::endl
            << "List of Landscape functions:"                        << std::endl
            << "   0   ->  Ackley function"                          << std::endl
            << "   1   ->  Booth function"                           << std::endl
            << "   2   ->  BukinN6 function"                         << std::endl
            << "   3   ->  CrossInTray function"                     << std::endl
            << "   4   ->  DixonPrice function"                      << std::endl
            << "   5   ->  DropWave function"                        << std::endl
            << "   6   ->  Eggholder function"                       << std::endl
            << "   7   ->  GramacyLee function"                      << std::endl
            << "   8   ->  GrieWank function"                        << std::endl
            << "   9   ->  HolderTable function"                     << std::endl
            << "   10  ->  Levy function"                            << std::endl
            << "   11  ->  LevyN13 function"                         << std::endl
            << "   12  ->  Matyas function"                          << std::endl
            << "   13  ->  McCormick function"                       << std::endl
            << "   14  ->  Rastring function"                        << std::endl
            << "   15  ->  Rosenbrock function"                      << std::endl
            << "   16  ->  SchafferN2 function"                      << std::endl
            << "   17  ->  SchafferN4 function"                      << std::endl
            << "   18  ->  Schwefel function"                        << std::endl
            << "   19  ->  Shubert function"                         << std::endl
            << "   20  ->  SixHumpCamel function"                    << std::endl
            << "   21  ->  ThreeHumpCamel function"                  << std::endl
            << "   22  ->  Zakharov function"                        << std::endl
            << std::endl;
}

int main(int argc, char **argv)
{
  const int dim = 2;
  int optimizer, landscape;

  if (argc < 3)
  {
    usage();
    std::exit(1);
  }

  optimizer = std::stoi(argv[1]);
  landscape = std::stoi(argv[2]);

  switch (optimizer)
  {
    case _bat:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::bat(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::bat(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::bat(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::bat(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::bat(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::bat(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::bat(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::bat(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::bat(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::bat(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::bat(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::bat(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::bat(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::bat(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::bat(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::bat(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::bat(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::bat(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::bat(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::bat(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::bat(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::bat(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::bat(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _bbo:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::bbo(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::bbo(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::bbo(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::bbo(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::bbo(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::bbo(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::bbo(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::bbo(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::bbo(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::bbo(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::bbo(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::bbo(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::bbo(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::bbo(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::bbo(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::bbo(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::bbo(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::bbo(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::bbo(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::bbo(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::bbo(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::bbo(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::bbo(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _cfa:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::cfa(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::cfa(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::cfa(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::cfa(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::cfa(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::cfa(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::cfa(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::cfa(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::cfa(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::cfa(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::cfa(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::cfa(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::cfa(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::cfa(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::cfa(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::cfa(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::cfa(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::cfa(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::cfa(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::cfa(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::cfa(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::cfa(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::cfa(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _cs:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::cs(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::cs(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::cs(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::cs(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::cs(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::cs(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::cs(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::cs(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::cs(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::cs(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::cs(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::cs(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::cs(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::cs(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::cs(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::cs(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::cs(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::cs(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::cs(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::cs(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::cs(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::cs(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::cs(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _gwo:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::gwo(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::gwo(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::gwo(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::gwo(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::gwo(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::gwo(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::gwo(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::gwo(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::gwo(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::gwo(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::gwo(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::gwo(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::gwo(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::gwo(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::gwo(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::gwo(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::gwo(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::gwo(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::gwo(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::gwo(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::gwo(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::gwo(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::gwo(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _pso:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::pso(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::pso(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::pso(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::pso(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::pso(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::pso(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::pso(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::pso(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::pso(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::pso(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::pso(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::pso(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::pso(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::pso(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::pso(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::pso(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::pso(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::pso(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::pso(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::pso(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::pso(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::pso(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::pso(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _ssa:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::ssa(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::ssa(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::ssa(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::ssa(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::ssa(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::ssa(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::ssa(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::ssa(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::ssa(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::ssa(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::ssa(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::ssa(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::ssa(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::ssa(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::ssa(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::ssa(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::ssa(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::ssa(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::ssa(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::ssa(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::ssa(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::ssa(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::ssa(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

    case _woa:
    {
      switch(landscape)
      {
        case _Ackley:         sol = walker::woa(Ackley, Ackley.lb, Ackley.ub, dim, n_population, max_iters);
        break;
        case _Booth:          sol = walker::woa(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);
        break;
        case _BukinN6:        sol = walker::woa(BukinN6, BukinN6.lb, BukinN6.ub, dim, n_population, max_iters);
        break;
        case _CrossInTray:    sol = walker::woa(CrossInTray, CrossInTray.lb, CrossInTray.ub, dim, n_population, max_iters);
        break;
        case _DixonPrice:     sol = walker::woa(DixonPrice, DixonPrice.lb, DixonPrice.ub, dim, n_population, max_iters);
        break;
        case _DropWave:       sol = walker::woa(DropWave, DropWave.lb, DropWave.ub, dim, n_population, max_iters);
        break;
        case _Eggholder:      sol = walker::woa(Eggholder, Eggholder.lb, Eggholder.ub, dim, n_population, max_iters);
        break;
        case _GramacyLee:     sol = walker::woa(GramacyLee, GramacyLee.lb, GramacyLee.ub, dim, n_population, max_iters);
        break;
        case _GrieWank:       sol = walker::woa(GrieWank, GrieWank.lb, GrieWank.ub, dim, n_population, max_iters);
        break;
        case _HolderTable:    sol = walker::woa(HolderTable, HolderTable.lb, HolderTable.ub, dim, n_population, max_iters);
        break;
        case _Levy:           sol = walker::woa(Levy, Levy.lb, Levy.ub, dim, n_population, max_iters);
        break;
        case _LevyN13:        sol = walker::woa(LevyN13, LevyN13.lb, LevyN13.ub, dim, n_population, max_iters);
        break;
        case _Matyas:         sol = walker::woa(Matyas, Matyas.lb, Matyas.ub, dim, n_population, max_iters);
        break;
        case _McCormick:      sol = walker::woa(McCormick, McCormick.lb, McCormick.ub, dim, n_population, max_iters);
        break;
        case _Rastring:       sol = walker::woa(Rastring, Rastring.lb, Rastring.ub, dim, n_population, max_iters);
        break;
        case _Rosenbrock:     sol = walker::woa(Rosenbrock, Rosenbrock.lb, Rosenbrock.ub, dim, n_population, max_iters);
        break;
        case _SchafferN2:     sol = walker::woa(SchafferN2, SchafferN2.lb, SchafferN2.ub, dim, n_population, max_iters);
        break;
        case _SchafferN4:     sol = walker::woa(SchafferN4, SchafferN4.lb, SchafferN4.ub, dim, n_population, max_iters);
        break;
        case _Schwefel:       sol = walker::woa(Schwefel, Schwefel.lb, Schwefel.ub, dim, n_population, max_iters);
        break;
        case _Shubert:        sol = walker::woa(Shubert, Shubert.lb, Shubert.ub, dim, n_population, max_iters);
        break;
        case _SixHumpCamel:   sol = walker::woa(SixHumpCamel, SixHumpCamel.lb, SixHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _ThreeHumpCamel: sol = walker::woa(ThreeHumpCamel, ThreeHumpCamel.lb, ThreeHumpCamel.ub, dim, n_population, max_iters);
        break;
        case _Zakharov:       sol = walker::woa(Zakharov, Zakharov.lb, Zakharov.ub, dim, n_population, max_iters);
        break;
      }
    } break;

  }

  if (sol.optimizer.empty())
  {
    // no landscape or optimizer given (wrong range!)
    usage();
    std::exit(1);
  }

  max_x = -inf;
  max_y = -inf;
  max_z = -inf;

  min_x = +inf;
  min_y = +inf;
  min_z = +inf;

  for (int i = 0; i < max_iters; ++i)
  {
    max_x = (sol.walk[i][0] > max_x) ? sol.walk[i][0] : max_x;
    max_y = (sol.walk[i][1] > max_y) ? sol.walk[i][1] : max_y;
    max_z = (sol.walk[i][2] > max_z) ? sol.walk[i][2] : max_z;
    min_x = (sol.walk[i][0] < min_x) ? sol.walk[i][0] : min_x;
    min_y = (sol.walk[i][1] < min_y) ? sol.walk[i][1] : min_y;
    min_z = (sol.walk[i][2] < min_z) ? sol.walk[i][2] : min_z;
  }

  draw_window(argc, argv, "Window");

  return 0;
}
