#include <sphere.h>

SolidSphere::SolidSphere(const float &radius, const int &rings, const int &sectors)
{
  const float R = 1.f / static_cast<float>(rings   - 1);
  const float S = 1.f / static_cast<float>(sectors - 1);
  nindices = rings * sectors;

  vertices  = std::make_unique<GLfloat[]>(nindices * 3);
  normals   = std::make_unique<GLfloat[]>(nindices * 3);
  texcoords = std::make_unique<GLfloat[]>(nindices * 2);

  int k = 0, t = 0;
  for (int r = 0; r < rings; ++r) for (int s = 0; s < sectors; ++s)
  {
    const float y = static_cast<float>(std::sin(-m_pi_2 + m_pi * r * R));
    const float x = static_cast<float>(std::cos(m_pi2 * s * S) * std::sin(m_pi * r * R));
    const float z = static_cast<float>(std::sin(m_pi2 * s * S) * std::sin(m_pi * r * R));

    texcoords[t  ] = s*S;
    texcoords[t++] = r*R;

    vertices[k ] = x * radius;
    normals[k++] = x;
    vertices[k]  = y * radius;
    normals[k++] = y;
    vertices[k]  = z * radius;
    normals[k++] = z;
  }

  indices = std::make_unique<GLushort[]>(nindices * 4);
  int i = 0;
  for (int r = 0; r < rings - 1; ++r) for (int s = 0; s < sectors - 1; ++s)
  {
    indices[i++] = r * sectors + s;
    indices[i++] = r * sectors + s + 1;
    indices[i++] = (r + 1) * sectors + (s + 1);
    indices[i++] = (r + 1) * sectors + s;
  }
}

void SolidSphere::draw( const GLfloat &x,
                        const GLfloat &y,
                        const GLfloat &z,
                        const GLfloat &R,
                        const GLfloat &G,
                        const GLfloat &B
                        )
{
  glMatrixMode(GL_MODELVIEW);
  glPushMatrix();
  glColor3f(R, G, B);
  glTranslatef(x, y, z);

  glEnableClientState(GL_VERTEX_ARRAY);
  glEnableClientState(GL_NORMAL_ARRAY);
  glEnableClientState(GL_TEXTURE_COORD_ARRAY);

  glVertexPointer(3, GL_FLOAT, 0, vertices.get());
  glNormalPointer(GL_FLOAT, 0, normals.get());
  glTexCoordPointer(2, GL_FLOAT, 0, texcoords.get());
  glDrawElements(GL_QUADS, nindices*4, GL_UNSIGNED_SHORT, indices.get());
  glPopMatrix();
}
