from tkinter import *
import random

GAME_WIDTH = 500
GAME_HEIGHT = 500
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#04d43c"
FOOD_COLOR = "#fc0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR, outline='#000000', tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                           fill=FOOD_COLOR, outline='', tag="food")


def next_turn(snake, food):
    global score, direction

    # Move player's snake
    x, y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, outline='#000000')
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions (walls or self-collision)
    if check_collisions(snake):
        game_over()
    else:
        # Schedule the next turn
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 40,
                       font=('consolas', 70), text="GAME OVER", fill='red', tag='gameover')

    # Create "Play Again" button
    play_again_button = Button(window, text="Play Again", command=reset_game, font=('consolas', 20))
    play_again_button.pack()

    # Position the button below the "GAME OVER" message
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, window=play_again_button)


def reset_game():
    global score, snake, food, direction

    # Clear the canvas and reset the game variables
    canvas.delete(ALL)

    # Reset score and direction
    score = 0
    label.config(text=f"Score: {score}")

    # Reinitialize the snake and food
    snake = Snake()
    food = Food()
    direction = 'right'

    # Start the game again
    next_turn(snake, food)

    # Remove the "Play Again" button
    for widget in window.pack_slaves():
        if isinstance(widget, Button):
            widget.pack_forget()


# Set up the window
window = Tk()
window.title("SnakeGame")

# Set the window geometry to match the game area, ensuring it matches the canvas size
window.geometry(f"{GAME_WIDTH+4}x{GAME_HEIGHT+4}")  # Extra space for padding or borders
window.resizable(False, False)

# Set up the score
score = 0
direction = "right"
label = Label(window, text="Score:{}".format(score), font=("Arial", 20))
label.pack()

# Create the game canvas with the exact dimensions
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the window on the screen
window.update()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (GAME_WIDTH / 2))
y = int((screen_height / 2) - (GAME_HEIGHT / 2))
window.geometry(f"{GAME_WIDTH+4}x{GAME_HEIGHT+4}+{x}+{y}")

# Bind the arrow keys to control the snake
window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))

# Initialize the snake and food, and start the game
snake = Snake()
food = Food()
next_turn(snake, food)

# Start the game loop
window.mainloop()