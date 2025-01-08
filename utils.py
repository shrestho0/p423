from OpenGL.GL import *
from OpenGL.GLUT import *


# Draw text using bitmap
def draw_text(x, y, text, color=(1, 1, 1)):
    glColor3f(*color)
    glRasterPos2f(x / 400 - 1, 1 - y / 300)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
def midpoint_line(x1, y1, x2, y2, point_size=1):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    steep = dy > dx  # Check if the line is steep

    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = x2 - x1
    dy = y2 - y1
    y_step = 1 if y1 < y2 else -1   
    d = 2 * dy - dx   

    y = y1

    glPointSize(point_size)

    glBegin(GL_POINTS)
    for x in range(x1, x2 + 1):
        if steep:
            glVertex2f(y / 400, x / 300)  
        else:
            glVertex2f(x / 400, y / 300)

        if d > 0:
            y += y_step
            d -= 2 * dx
        d += 2 * dy
    glEnd()
    # reset to 1
    glPointSize(1)


# Midpoint Circle Algorithm
def midpoint_circle(cx, cy, radius, point_size=1):
    x = 0
    y = radius
    d = 1 - radius

    glPointSize(point_size)
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
    # reset to 1
    glPointSize(1)