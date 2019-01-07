// g++ run.cpp sphere.cpp -o run -O3 -std=c++17 -I. -lGL -lGLU -lglut
#include <draw.h>
#include <sphere.h>
#include <walkers.h>
#include <landscape.h>

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


int main(int argc, char **argv)
{
  const int dim = 2;
  sol = walker::bat(Booth, Booth.lb, Booth.ub, dim, n_population, max_iters);

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
