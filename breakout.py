import tkinter as tk

# Constants
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
PADDLE_Y = CANVAS_HEIGHT - 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
BALL_RADIUS = 10

BRICK_GAP = 5
BRICK_WIDTH = (CANVAS_WIDTH - BRICK_GAP * 9) / 10
BRICK_HEIGHT = 10

BRICKS_ROW = 10

DELAY = 10  # Milliseconds

FONT_TITLE = ("Helvetica", 50)
FONT_MEDIUM = ("Helvetica", 30)
FONT_SMALL = ("Helvetica", 20)


def main():
    # Create main window
    global root, canvas, level
    root = tk.Tk()
    root.title("The Breakout")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)

    # Level variable
    level = 1

    # Starting screen
    welcome_screen()

    # Root loop
    root.mainloop()

# Welcome screen
def welcome_screen():
    # Access global variable "level"
    global level
    
    # Click handler
    def click(e):
        start_game()

    # Clear the screen
    canvas.delete("all")

    # Set up canvas
    canvas.bind("<Button-1>", click)
    canvas.pack()

    # If last level
    if level == 4:
        canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="GAME OVER", font=FONT_TITLE
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.6,
            text="YOU WON !",
            font=FONT_MEDIUM,
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.4,
            text="Click to start again!",
            font=FONT_SMALL,
        )
        level = 1
    else:
        # Welcome text
        canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="The Breakout", font=FONT_TITLE
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.6,
            text="Click to start",
            font=FONT_SMALL,
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.5,
            text=f"Level {level}",
            font=FONT_SMALL,
        )


    # Background
    set_up_the_world(canvas)
    create_paddle(canvas)


def start_game():
    global level

    # Clear canvas
    canvas.delete("all")

    # Set up the world
    set_up_the_world(canvas)

    # Amount of bricks
    bricks_amount = 10 * BRICKS_ROW  # 10 rows of bricks

    # Create the bouncing ball
    ball = create_a_ball(canvas)

    # Create the paddle
    paddle = create_paddle(canvas)

    # Speed of ball
    ball_change = level * 3

    # Ball's x, y change
    change_x, change_y = ball_change, ball_change

    # Game state
    game_state = {
        "canvas": canvas,
        "ball": ball,
        "paddle": paddle,
        "change_x": change_x,
        "change_y": change_y,
        "ball_change": ball_change,
        "bricks_amount": bricks_amount,
    }

    # Start game loop
    game_loop(game_state)
    

def game_loop(state):
    # Access global variable "level"
    global level

    canvas = state["canvas"]
    ball = state["ball"]
    paddle = state["paddle"]
    change_x = state["change_x"]
    change_y = state["change_y"]
    ball_change = state["ball_change"]
    bricks_amount = state["bricks_amount"]

    # If touches bottom == player loses
    if change_x is False:
        canvas.create_text(
            CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, text="GAME OVER", font=FONT_TITLE
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.6,
            text="YOU LOST !",
            font=FONT_MEDIUM,
        )
        canvas.create_text(
            CANVAS_WIDTH / 2,
            CANVAS_HEIGHT / 1.4,
            text="Click to start again!",
            font=FONT_SMALL,
        )
        return
    

    # If no more bricks
    if bricks_amount == 0:
        level += 1
        welcome_screen()
        return

    # Bounce the ball
    change_x, change_y = bounce_ball(canvas, ball, change_x, change_y, ball_change)

    # Get mouse x and change paddle x
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    if mouse_x >= CANVAS_WIDTH - PADDLE_WIDTH:
        canvas.moveto(paddle, CANVAS_WIDTH - PADDLE_WIDTH, PADDLE_Y)
    else:
        canvas.moveto(paddle, mouse_x, PADDLE_Y)

    # Get ball x, y
    ball_coords = canvas.coords(ball)
    ball_x, ball_y = ball_coords[0], ball_coords[1]


    # Get colliding list
    colliding_list = canvas.find_overlapping(
        ball_x, ball_y, ball_x + BALL_RADIUS, ball_y + BALL_RADIUS
    )

    # Bounce the ball from paddle
    if paddle in colliding_list:
        change_y = -ball_change
    elif len(colliding_list) > 1:
        canvas.delete(colliding_list[0])
        change_y = ball_change
        bricks_amount -= 1

    # Update state
    state["change_x"] = change_x
    state["change_y"] = change_y
    state["bricks_amount"] = bricks_amount

    # Loop animation
    canvas.after(DELAY, game_loop, state)


# Function to set up the world with bricks
def set_up_the_world(canvas):
    create_one_color(canvas, "red", BRICK_HEIGHT + BRICK_GAP)
    create_one_color(canvas, "red", BRICK_HEIGHT * 2 + BRICK_GAP * 2)
    create_one_color(canvas, "orange", BRICK_HEIGHT * 3 + BRICK_GAP * 3)
    create_one_color(canvas, "orange", BRICK_HEIGHT * 4 + BRICK_GAP * 4)
    create_one_color(canvas, "yellow", BRICK_HEIGHT * 5 + BRICK_GAP * 5)
    create_one_color(canvas, "yellow", BRICK_HEIGHT * 6 + BRICK_GAP * 6)
    create_one_color(canvas, "green", BRICK_HEIGHT * 7 + BRICK_GAP * 7)
    create_one_color(canvas, "green", BRICK_HEIGHT * 8 + BRICK_GAP * 8)
    create_one_color(canvas, "cyan", BRICK_HEIGHT * 9 + BRICK_GAP * 9)
    create_one_color(canvas, "cyan", BRICK_HEIGHT * 10 + BRICK_GAP * 10)


# Create one row in one color function
def create_one_color(canvas, color, start_y):
    for i in range(0, BRICKS_ROW):
        start_x = (CANVAS_WIDTH / BRICKS_ROW) * i + BRICK_GAP / 4
        canvas.create_rectangle(
            start_x,
            start_y,
            start_x + BRICK_WIDTH + BRICK_GAP / 2,
            start_y + BRICK_HEIGHT + BRICK_GAP / 2,
            fill=color,
        )


# Create the ball function
def create_a_ball(canvas):
    start_x = (CANVAS_WIDTH / 2) - (BALL_RADIUS / 2)
    start_y = (CANVAS_HEIGHT / 2) - (BALL_RADIUS / 2)
    ball = canvas.create_oval(
        start_x, start_y, start_x + BALL_RADIUS, start_y + BALL_RADIUS, fill="black"
    )

    return ball


# Bounce the ball function
def bounce_ball(canvas, ball, change_x, change_y, ball_change):
    # Get ball coords
    ball_coords = canvas.coords(ball)
    ball_x, ball_y = ball_coords[0], ball_coords[1]

    # Calculate coords
    if ball_x >= CANVAS_WIDTH - BALL_RADIUS:
        change_x = -ball_change
    if ball_x <= 0:
        change_x = ball_change
    if ball_y >= CANVAS_HEIGHT - BALL_RADIUS:
        return False, False
    if ball_y <= 0:
        change_y = ball_change

    # Bounce the ball
    canvas.move(ball, change_x, change_y)
    return change_x, change_y


# Create the paddle function
def create_paddle(canvas):
    paddle = canvas.create_rectangle(
        0, PADDLE_Y, PADDLE_WIDTH, PADDLE_Y + PADDLE_HEIGHT, fill="black"
    )
    return paddle


if __name__ == "__main__":
    main()
