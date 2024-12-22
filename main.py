from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from utils import draw_text, midpoint_line, midpoint_circle
from abc import ABC

## Constants
W_WIDTH, W_HEIGHT = 800, 600
## Game Data
class GameState(ABC):
    game_over = False
    total_lives = 3
    current_lives = 3
    total_levels = 5
    current_levels = 1
    game_complete = False
 

### Game Screen / View
def test_draw():
    midpoint_line(-400, 225, 400, 225)
    midpoint_circle(-100,-100,20)
    pass

def draw_game_over_overlay():
    if GameState.game_complete:
        draw_text(W_WIDTH // 2 - 150+20, W_HEIGHT // 2-70, "Congratulations! Game Complete")
    #TODO: maybe, show either complete or over, not sure
    draw_text(W_WIDTH // 2 - 60+20, W_HEIGHT // 2 - 30, "Game Over")
    draw_text(W_WIDTH//2 - 140+20, W_HEIGHT // 2 , "Press `R` to Restart, `Q` to Quit")

def draw_info():
    start_x = 10
    start_y = 20
    draw_text(start_x, start_y , f"Lives: {GameState.current_levels}/{GameState.total_lives}", color=(1,.7,0))
    draw_text(start_x, start_y+25, f"Level: {GameState.current_levels}/{GameState.total_levels}", color=(1,0,.7))

# Draw scene
def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if GameState.game_over:
        draw_game_over_overlay()
    else:
        test_draw()
        draw_info()

    glutSwapBuffers()



### Game Logic
def update(value):
    """ Updates game upon actions """
    print(f"update-->{value}")
    glutTimerFunc(16, update, 0)

# Keyboard input
def keyboard(key, x, y):
    """ Set game logic from keyboard event """
    if key == b'o':
        GameState.game_over = True
    elif key == b"c":
        GameState.game_complete = True
    elif key == b'q' and GameState.game_over:
        glutLeaveMainLoop()

    print(key,x,y)


# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(W_WIDTH, W_HEIGHT)
    glutCreateWindow(b"DX Ball with GL_POINTS")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
