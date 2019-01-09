#ifndef SPHERE_H
#define SPHERE_H
#include <vector>
#include <cmath>
#ifdef _WIN32
#include <windows.h>
#endif
#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif
#include <memory>
static constexpr float m_pi   = 3.141519f;
static constexpr float m_pi_2 = 1.570759f;
static constexpr float m_pi2  = m_pi * 2.f;

class SolidSphere
{
protected:
  int nindices;
  std::unique_ptr<GLfloat[]> vertices, normals, texcoords;
  std::unique_ptr<GLushort[]> indices;

public:
  SolidSphere() {};
  SolidSphere(const float &radius, const int &rings, const int &sectors);
  void draw(const GLfloat &x, const GLfloat &y, const GLfloat &z, const GLfloat &R, const GLfloat &G, const GLfloat &B );
};

#endif // SPHERE_H
