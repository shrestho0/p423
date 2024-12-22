from OpenGL.GL import *
from OpenGL.GLUT import *


# Draw text using bitmap
def draw_text(x, y, text, color=(1, 1, 1)):
    glColor3f(*color)
    glRasterPos2f(x / 400 - 1, 1 - y / 300)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

# Midpoint Line Algorithm
def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    y = y1

    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        glVertex2f(x / 400, y / 300)  # Normalized to screen coordinates
        if d > 0:
            y += 1
            d += 2 * (dy - dx)
        else:
            d += 2 * dy
    glEnd()

# Midpoint Circle Algorithm
def midpoint_circle(cx, cy, radius):
    x = 0
    y = radius
    d = 1 - radius

    glBegin(GL_POINTS)
    while x <= y:
        # Plot all eight octants
        glVertex2f((cx + x) / 400, (cy + y) / 300)
        glVertex2f((cx - x) / 400, (cy + y) / 300)
        glVertex2f((cx + x) / 400, (cy - y) / 300)
        glVertex2f((cx - x) / 400, (cy - y) / 300)
        glVertex2f((cx + y) / 400, (cy + x) / 300)
        glVertex2f((cx - y) / 400, (cy + x) / 300)
        glVertex2f((cx + y) / 400, (cy - x) / 300)
        glVertex2f((cx - y) / 400, (cy - x) / 300)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    glEnd()