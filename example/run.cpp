// g++ run.cpp sphere.cpp walker.cpp -o run -O3 -std=c++17 -I. -lGL -lGLU -lglut
#include <draw.h>
#include <sphere.h>
#include <walker.h>

static constexpr int nstep  = 100000;
static constexpr float beta = 1.65f;
static SolidSphere sphere(.05f, 12, 24);
walkers walker(nstep);

void display()
{
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Clear color and depth buffers
  glMatrixMode(GL_MODELVIEW);                         // To operate on model-view matrix
                                                      // Clear window and null buffer Z
                                                      // glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
                                                      // Reset transformation
  glLoadIdentity();

  //glPushMatrix();
  //glRotatef(rotate_x, 1.0, 0.0, 0.0);
  //glRotatef(rotate_y, 0.0, 1.0, 0.0);
  //glTranslated(transl_x, transl_y, 0.f);
  //glScalef(zoom, zoom, zoom);
  //sphere.draw(0.f, 0.f, 0.f, 1, 0, 0);
  //glPopMatrix();

  glPushMatrix();
  glRotatef(rotate_x, 1.0, 0.0, 0.0);
  glRotatef(rotate_y, 0.0, 1.0, 0.0);
  glTranslated(transl_x, transl_y, 0.f);
  glScalef(zoom, zoom, zoom);
  glBegin(GL_LINE_STRIP);
  glNormal3f(1.f, 1.f, 1.f);
  glColor3f(1.f, 1.f, 1.f);
  for (int i = 0; i < nstep; ++i) glVertex3f(walker.x[i], walker.y[i], walker.z[i]);
  glEnd();
  glPopMatrix();

  glFlush();
  glutSwapBuffers();
}

int main(int argc, char **argv)
{
  walker.levy(beta);
  draw_window(argc, argv, "Window");
}
