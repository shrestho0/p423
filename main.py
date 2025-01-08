from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from utils import draw_text, midpoint_line, midpoint_circle

## Constants
W_WIDTH, W_HEIGHT = 800, 600

DEFAULT_COLOR = (0.9,0.9,0.9)
PADDLE_COLOR = (0.176, 1, 0.624)
TEXT_LIVES_COLOR = (1,.7,0)
TEXT_LEVELS_COLOR = TEXT_LIVES_COLOR
TEXT_SCORE_COLOR = (0.7,0,1)
SCORE_BOUNDARY_COLOR=(1,0,.7)
BALL_COLOR = (0.9, 0.9, 0.4)
BRICK_COLOR=(1,0,.7)

PADDLE_HEIGHT=20
PADDLE_WIDTH=120
PADDLE_SPEED = 35

BRICK_WIDTH = 60
BRICK_HEIGHT = 20
BRICK_MARGIN = 10  

BALL_RADIUS = 10
BALL_SPEED = 4
BALL_SPEED_INCREMENT = 1

## Game Data
class GameState:
     
    game_started = False
    game_over = False
    game_complete = False
    
    total_lives = 3
    current_live = 3
    total_levels = 5
    current_level = 1
    score = 0

    paddle_pos_x = 0
    paddle_pos_y = -280

    ball_pos_x = 0
    ball_pos_y = -250  # Just above the paddle

    ball_speed_x = BALL_SPEED  # Horizontal speed 
    ball_speed_y = BALL_SPEED  # Vertical speed 


    boundary_x_left = -W_WIDTH//2 # half of -W_WIDTH
    boundary_x_right = W_WIDTH//2 # half of W_WIDTH
    boundary_y_top = W_HEIGHT//2 - 30  # top half
    boundary_y_bottom = -W_HEIGHT//2 # bottom half

    paddle_half_width = PADDLE_WIDTH//2

    brick_half_w = BRICK_WIDTH//2
    brick_half_h = BRICK_HEIGHT//2

    bricks = []

    @classmethod
    def start_game(cls):
        """Start the game."""
        cls.bricks = cls.calculate_bricks()
        cls.game_started = True
        cls.game_over = False
        cls.game_complete = False
        cls.score = 0
    
    @classmethod
    def restart_game(cls):
        """Restart the game."""
        cls.paddle_pos_x = 0
        cls.current_level = 1
        cls.current_live = cls.total_lives
        cls.ball_speed_x = BALL_SPEED
        cls.ball_speed_y = BALL_SPEED
        cls.start_game()
    

    @classmethod
    def progress_level(cls):
        """Progress to the next level."""
        if cls.current_level + 1 > cls.total_levels:
            cls.game_complete = True
            cls.game_over = True
        else:
            # new level will have new bricks
            cls.current_level += 1
            cls.bricks = cls.calculate_bricks()
            # game goes on
            # ball speed increases with level by 1
            cls.ball_speed_x += BALL_SPEED_INCREMENT if cls.ball_speed_x > 0 else -BALL_SPEED_INCREMENT
            cls.ball_speed_y += BALL_SPEED_INCREMENT if cls.ball_speed_y > 0 else -BALL_SPEED_INCREMENT

    @classmethod
    def decrease_live(cls):
        """Decrease the number of lives by 1."""
        if cls.current_live-1 == 0:
            cls.game_over = True
        else:
            cls.current_live -= 1

    
    @classmethod
    def move_paddle(cls, left: bool = True):
        """Move the paddle left or right."""
        if left:
            if (cls.paddle_pos_x - cls.paddle_half_width - PADDLE_SPEED) > cls.boundary_x_left:
                cls.paddle_pos_x -= PADDLE_SPEED
            else:
                print("Invalid move [left]: Paddle at left boundary.")
        else:
            if (cls.paddle_pos_x + cls.paddle_half_width + PADDLE_SPEED) < cls.boundary_x_right:
                cls.paddle_pos_x += PADDLE_SPEED
            else:
                print("Invalid move [right]: Paddle at right boundary.")

    @classmethod
    def move_ball(cls):
        """Move the ball based on its speed."""
        cls.ball_pos_x += cls.ball_speed_x
        cls.ball_pos_y += cls.ball_speed_y

    @classmethod
    def handle_collisions(cls):
        """Handle collisions of the ball with the walls, bricks, and paddle."""
        # check collision with walls
        # if collision with wall top, wall left, wall right then negate ball speed
        next_ball = [cls.ball_pos_x+cls.ball_speed_x, cls.ball_pos_y+cls.ball_speed_y]
        wall_boundary_hit = False
        if next_ball[0] + BALL_RADIUS >= cls.boundary_x_right or next_ball[0]-BALL_RADIUS <= cls.boundary_x_left:
            cls.ball_speed_x *= -1
            wall_boundary_hit = True
        if next_ball[1] + BALL_RADIUS >= cls.boundary_y_top:
            cls.ball_speed_y *= - 1
            wall_boundary_hit = True
        
        if wall_boundary_hit:
            cls.move_ball()
        else:

            # handle collision with bricks
            if len(cls.bricks) == 0:
                cls.progress_level()
                return 
            else:
                for brick in cls.bricks:
                    x, y = brick
                    # Calculate the four corners of the brick
                    top_left = (x, y)
                    top_right = (x + BRICK_WIDTH, y)
                    bottom_left = (x, y - BRICK_HEIGHT)
                    bottom_right = (x + BRICK_WIDTH, y - BRICK_HEIGHT)
                    # check if ball is within the brick boundary
                    if top_left[0] <= next_ball[0] <= top_right[0] and bottom_left[1] <= next_ball[1] <= top_left[1]:
                        # ball hit the brick
                        cls.ball_speed_y *= -1
                        cls.score += 1
                        cls.bricks.remove(brick)
                        cls.move_ball()
                        # constant: only one brick can be hit at a time 
                        break
            

            # handle collision on paddle
            paddle_top_edge = cls.paddle_pos_y + PADDLE_HEIGHT / 2 # - as y negative
            if next_ball[1] - BALL_RADIUS <= paddle_top_edge and cls.paddle_pos_x - PADDLE_WIDTH / 2 <= next_ball[0] <= cls.paddle_pos_x + PADDLE_WIDTH / 2:
                cls.ball_speed_y *= -1
                cls.ball_speed_x = (cls.ball_pos_x - cls.paddle_pos_x) / 10
                # cls.move_ball()
            elif next_ball[1] - BALL_RADIUS <= cls.boundary_y_bottom:
                # handle ball hitting the bottom boundary (e.g., lose a life or reset ball position)
                
                # same game, so, speed remains same
                temp_ball_speed_x = cls.ball_speed_x if cls.ball_speed_x > 0 else -cls.ball_speed_x
                temp_ball_speed_y = cls.ball_speed_y if cls.ball_speed_y > 0 else -cls.ball_speed_y
                cls.reset_ball()
                cls.ball_speed_x = temp_ball_speed_x
                cls.ball_speed_y = temp_ball_speed_y

                cls.decrease_live()
                cls.reset_paddle()
                return                
            cls.move_ball()
 

        # check collision with bricks

    @classmethod
    def reset_ball(cls):
        """Reset the ball to its starting position."""
        cls.ball_pos_x = 0
        cls.ball_pos_y = -250  # Reset just above the paddle
        cls.ball_speed_x = BALL_SPEED  # Reset horizontal speed
        cls.ball_speed_y = -BALL_SPEED  # Reset vertical speed

    @classmethod
    def reset_paddle(cls):
        """Reset the paddle to its starting position and size."""
        cls.paddle_pos_x = 0  # Center the paddle horizontally
        cls.paddle_pos_y = -280  # Position the paddle just above the bottom of the screen
 

    @classmethod
    def calculate_bricks(cls):
        """Calculate the positions of the bricks in the grid."""
        rows = 1 + GameState.current_level  # at least one row
        cols = 2 + (GameState.current_level * 1)  # at least two columns
        # Calculate the total width of the brick grid (including margins)
        total_width = cols * BRICK_WIDTH + (cols - 1) * BRICK_MARGIN

        # Starting positions for the first brick (top-left corner)
        start_x = -total_width // 2  # center horizontally
        start_y = 200  # start slightly below the top of the window

        bricks = []

        for row in range(rows):
            for col in range(cols):
                # Calculate the top-left corner of each brick, considering the margin
                x = start_x + col * (BRICK_WIDTH + BRICK_MARGIN)
                y = start_y - row * (BRICK_HEIGHT + BRICK_MARGIN)
                
                # Store the brick's position in the bricks list
                bricks.append([x,y])
        
        return bricks

 
### Game Screen / View
def draw_cords():
    midpoint_line(-20,0,20,0)
    midpoint_line(0,-20,0,20)
 
 

def draw_game_start_overlay():
    draw_text(W_WIDTH //2 -140+20, W_HEIGHT // 2 - 30, "Welcome to DX Ball Mini")
    draw_text(W_WIDTH //2  - 140+20, W_HEIGHT // 2 , "Press `Spacebar` to Start")

def draw_game_over_overlay():
    # game complete is also game over, thus taking game_complete first
    draw_text(W_WIDTH//2 -20, W_HEIGHT // 2 - 60 , f"Score: {GameState.score}")
    if GameState.game_complete:
        draw_text(W_WIDTH // 2 - 150+20, W_HEIGHT // 2 - 30, "Congratulations! Game Complete")
    elif GameState.game_over:
        draw_text(W_WIDTH // 2 - 60+20, W_HEIGHT // 2 - 30, "Game Over")
    draw_text(W_WIDTH//2 - 140+20, W_HEIGHT // 2 , "Press `R` to Restart, `Q` to Quit")

def draw_info():
    start_x = 10
    start_y = 20
    draw_text(start_x, start_y , f"Lives: {GameState.current_live}/{GameState.total_lives}", color=TEXT_LIVES_COLOR)
    draw_text(start_x+100, start_y, f"Level: {GameState.current_level}/{GameState.total_levels}", color=TEXT_LEVELS_COLOR)
    draw_text(W_WIDTH-start_x-100, start_y, f"Score: {GameState.score}", color=TEXT_SCORE_COLOR)
    

    # top boundary
    glColor3f(*SCORE_BOUNDARY_COLOR)
    midpoint_line(-400,270, 400, 270, point_size=4) 
    glColor3f(*DEFAULT_COLOR)

 

def draw_paddle():
    half_w = PADDLE_WIDTH//2
    half_h = PADDLE_HEIGHT//2
    x,y = GameState.paddle_pos_x, GameState.paddle_pos_y
    # Calculate the four corners of the rectangle
    top_left = (x - half_w, y + half_h)
    top_right = (x + half_w, y + half_h)
    bottom_left = (x - half_w, y - half_h)
    bottom_right = (x + half_w, y - half_h)

    glColor3f(*PADDLE_COLOR)
    # Draw edges of the rectangle
    midpoint_line(top_left[0], top_left[1], top_right[0], top_right[1])       # Top edge
    midpoint_line(top_right[0], top_right[1], bottom_right[0], bottom_right[1])  # Right edge
    midpoint_line(bottom_right[0], bottom_right[1], bottom_left[0], bottom_left[1]) # Bottom edge
    midpoint_line(bottom_left[0], bottom_left[1], top_left[0], top_left[1])      # Left edge
    glColor3f(*DEFAULT_COLOR)

def draw_ball():
    glColor3f(*BALL_COLOR)
    midpoint_circle(GameState.ball_pos_x, GameState.ball_pos_y, BALL_RADIUS, point_size=3)
    glColor3f(*DEFAULT_COLOR)  # Reset color

 
def draw_bricks():
    for brick in GameState.bricks:
        x, y = brick
        
        # Calculate the four corners of the brick
        top_left = (x, y)
        top_right = (x + BRICK_WIDTH, y)
        bottom_left = (x, y - BRICK_HEIGHT)
        bottom_right = (x + BRICK_WIDTH, y - BRICK_HEIGHT)

        glColor3f(*BRICK_COLOR)  
        midpoint_line(top_left[0], top_left[1], top_right[0], top_right[1])  # Top edge
        midpoint_line(top_right[0], top_right[1], bottom_right[0], bottom_right[1])  # Right edge
        midpoint_line(bottom_right[0], bottom_right[1], bottom_left[0], bottom_left[1])  # Bottom edge
        midpoint_line(bottom_left[0], bottom_left[1], top_left[0], top_left[1])  # Left edge

# Draw scene
def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if GameState.game_over:
        draw_game_over_overlay()
    elif not GameState.game_started:
        draw_game_start_overlay()
    else:
        draw_cords()
        draw_info()
        draw_bricks()
        draw_paddle()
        draw_ball()

    glutSwapBuffers()



### Game Logic
def update(value):
    """ Updates game upon actions """
    if GameState.game_started and not GameState.game_over:
        GameState.handle_collisions()

    glutTimerFunc(16, update, 0)

# Keyboard input
def keyboard_handler(key, x, y):
    """ Set game logic from keyboard event """
    # if key == b" " and not GameState.game_over and not GameState.game_complete:
    if key == b" " and not GameState.game_started:
        GameState.start_game()
        return
    elif key == b'q' and GameState.game_over:
        glutLeaveMainLoop()
    elif key == b"r" and GameState.game_over:
        GameState.restart_game()
        
    
    # Cheat sheet (for simplicity)
    if key == b'o':
        GameState.game_over = True
    elif key == b'n':
        GameState.progress_level()
    elif key == b"c":
        GameState.current_level = GameState.total_levels-1
        GameState.progress_level()
    elif key == b"k":
        GameState.decrease_live()

    print(key,x,y)

def special_key_handler(key,x,y):
    if GameState.game_complete or GameState.game_over:
        print("game over, special keys are useless now")
        return
    if key == GLUT_KEY_LEFT:
        GameState.move_paddle(True)
    if key == GLUT_KEY_RIGHT:
        GameState.move_paddle(False)

# Main function
def main():
    if not hasattr(glutInit, "__call__"):
        print("ERROR: Glut is not available")
        exit(1)
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(W_WIDTH, W_HEIGHT)
    glutCreateWindow(b"DX Ball with GL_POINTS")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(draw)
    glutIdleFunc(draw)
    glutKeyboardFunc(keyboard_handler)
    glutSpecialFunc(special_key_handler)
    glutTimerFunc(16, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
