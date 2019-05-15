from microbit import *
import random

UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)

tilt_threshold = 300

def new_snake_direction():
    global snake_direction
    x, y, _ = accelerometer.get_values()
    if x < -tilt_threshold and snake_direction != RIGHT:
        snake_direction = LEFT
    elif x > tilt_threshold and snake_direction != LEFT:
        snake_direction = RIGHT
    elif y < -tilt_threshold and snake_direction != UP:
        snake_direction = DOWN
    elif y > tilt_threshold and snake_direction != DOWN:
        snake_direction = UP
    else:
        pass

def evolve(snake):
    head = snake[0]
    new_head = ((head[0] + snake_direction[0]) % 5, (head[1] + snake_direction[1]) % 5)
    return [new_head] + snake[:-1], snake[-1]

def clear_image():
    return [[0]* 5 for _ in range(5)]

def display_image(image):
    s = ""
    for line in image:
        s += "".join(map(str, line)) + ":"
    display.show(Image(s))

def display_snake(snake):
    img = clear_image()
    for coord in snake:
        x, y = coord
        img[y][x] = 5
    head = snake[0]
    img[head[1]][head[0]] = 9
    display_image(img)

def display_game(snake, point):
    display_snake(snake + [point])
    sleep(100)
    display_snake(snake)
    sleep(100)
    display_snake(snake + [point])
    sleep(100)
    display_snake(snake)
    sleep(100)

def new_point(snake):
    coords = list(set((x, y) for x in range(5) for y in range(5)) - set(snake))
    if coords:
        return random.choice(coords)

while True:
    snake = [(random.randint(0, 4), random.randint(0, 4))]
    snake_direction = random.choice([UP, DOWN, LEFT, RIGHT])
    point = new_point(snake)
    new_game = False

    while not new_game:
        display_game(snake, point)
        new_snake_direction()
        snake, tail = evolve(snake)

        if len(snake) != len(set(snake)):
            new_game = True

        if point in snake:
            snake = snake + [tail]
            point = new_point(snake)
            if point is None:
                display.scroll("YOU WON!")
                display.show(Image.HAPPY)
                while not button_a.is_pressed():
                    sleep(100)
                new_game = True