# Write your code here :-)

from microbit import *
import time

ll, lm, mm, rm, rr = -500, -250, 0, 250, 500

def convert(image):
    return Image(
        ":".join("".join(("9" if n else "0") for n in line) for line in image)
    )

def empty():
    return [[0]*5 for _ in range(5)]

def add(img1, img2):
    im = empty()
    for y in range(5):
        for x in range(5):
            im[x][y] = (img1[x][y] + img2[x][y]) % 2
    return im

def points(pts):
    img = empty()
    for x, y in pts:
        img[y][x] = 1
    return img

def grid_coordinate(raw):
    i = 0
    if lm < raw < rm:
        i = 2
    elif ll < raw < lm:
        i = 1
    elif raw < ll:
        i = 0
    elif rm < raw < rr:
        i = 3
    elif rr < raw:
        i = 4
    return i

def to_grid(x_raw, y_raw):
    return grid_coordinate(x_raw), grid_coordinate(y_raw)

def neighbours(x, y, world):
    n = 0
    coords = [
        (x-1, y-1),
        (x-1, y),
        (x-1, y+1),
        (x, y-1),
        (x, y+1),
        (x+1, y-1),
        (x+1, y),
        (x+1, y+1),
    ]
    for c in coords:
        if (c[0] % 5, c[1] % 5) in world:
            n += 1
    return n

def evolve(world):
    new = set()
    for y in range(5):
        for x in range(5):
            n = neighbours(x, y, world)
            if n == 3:
                new.add((x, y))
            if n == 2 and (x, y) in world:
                new.add((x, y))
    return new

while True:
    world = set()
    tmp_sum = empty()
    tmp_x, tmp_y = 0, 0

    while not button_a.is_pressed():
        x_raw, y_raw, z_raw = accelerometer.get_values()
        x, y = to_grid(x_raw, y_raw)
        if x != tmp_x or y != tmp_y:
            tmp_sum = points(world)
        img = points([(x, y)])
        tmp_sum = add(tmp_sum, img)
        display.show(convert(tmp_sum))
        if button_b.is_pressed():
            if (x, y) in world:
                world.remove((x, y))
            else:
                world.add((x, y))
            time.sleep(0.15)
        tmp_x, tmp_y = x, y
        time.sleep(0.1)

    while not button_b.is_pressed():
        world = evolve(world)
        display.show(convert(points(world)))
        time.sleep(0.2)

    time.sleep(0.2)