import pygame
from random import randint
from copy import deepcopy
import hashlib
import json

WIDTH = 800
HEIGHT = 450
FPS = 10
cell = 50
W = WIDTH // cell
H = HEIGHT // cell

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

played_combinations = {}

next_field = [[0 for i in range(W)] for j in range(H)]

current_field_user = [[0 for i in range(W)] for j in range(H)]


def check_cell(current_field_user, x, y):
    count = 0
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            j = j % H
            i = i % W

            if current_field_user[j][i]:
                count += 1
    if current_field_user[y][x]:
        count -= 1
        if count == 2 or count == 3:
            return 1
        return 0
    else:
        if count == 3:
            return 1
        return 0


def check_live_cells(current_field_user):
    for y in range(0, len(current_field_user)):
        for x in range(0, len(current_field_user[y])):
            if current_field_user[y][x]:
                return True
    return False


def clear_next():
    for y in range(0, len(next_field)):
        for x in range(0, len(next_field[y])):
            next_field[y][x] = 0


def check_difference(current_field_user, next_field):
    for y in range(0, len(current_field_user)):
        for x in range(0, len(current_field_user[y])):
            if current_field_user[y][x] != next_field[y][x]:
                return True
    return False


def get_combination_key(next_field):
    plain_map = ''
    for y in range(0, len(current_field_user)):
        for x in range(0, len(current_field_user[y])):
            plain_map += str(next_field[y][x])

    return hashlib.md5(plain_map.encode('utf-8')).hexdigest()


def check_repeated_combination(next_field):
    key = get_combination_key(next_field)

    return key in played_combinations


def save_combination(next_field):
    key = get_combination_key(next_field)

    played_combinations[key] = True


def save(current_field_user):
    with open('saved.json', 'w') as outfile:
        json.dump(current_field_user, outfile)


def load():
    with open('saved.json') as json_file:
        data = json.load(json_file)
        for y in range(0, len(data)):
            for x in range(0, len(data[y])):
                current_field_user[y][x] = data[y][x]
        redraw()


def redraw():
    for x in range(0, W):
        for y in range(0, H):
            if current_field_user[y][x]:
                pygame.draw.rect(screen, pygame.Color('forestgreen'), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))
            else:
                pygame.draw.rect(screen, pygame.Color('black'), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))

running = False

screen.fill(pygame.Color('black'))
while True:
    if running:
        for x in range(0, W):
            for y in range(0, H):
                next_field[y][x] = check_cell(current_field_user, x, y)
                if next_field[y][x]:
                    pygame.draw.rect(screen, pygame.Color('forestgreen'), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))
                else:
                    pygame.draw.rect(screen, pygame.Color('black'), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))

        if not check_live_cells(next_field):
            running = False

        if not check_difference(current_field_user, next_field):
            running = False

        if check_repeated_combination(next_field):
            played_combinations = {}
            running = False

        if running:
            save_combination(next_field)

            current_field_user = deepcopy(next_field)
            clear_next()

    for x in range(0, WIDTH, cell):
        pygame.draw.line(screen, pygame.Color('dimgray'), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, cell):
        pygame.draw.line(screen, pygame.Color('dimgray'), (0, y), (WIDTH, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0] // 50
            y = event.pos[1] // 50
            current_field_user[y][x] = 1
            pygame.draw.rect(screen, pygame.Color('forestgreen'), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if running:
                    running = False
                else:
                    running = True
            elif event.key == pygame.K_s:
                save(current_field_user)
            elif event.key == pygame.K_l:
                load()

    pygame.display.flip()
    clock.tick(FPS)
