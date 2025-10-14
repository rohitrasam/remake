from typing import List
import pygame as pg
from random import randint

# 1. TODO: scrolling background parallax
# 2. TODO: Collision


SCREEN_WIDTH, SCREEN_HEIGHT = 720, 720
DISPLAY_WIDTH, DISPLAY_HEIGHT = 180, 180
PLAYER_START = [90, 165]
ENEMY_SPEED = 1.5
PLAYER_SPEED = 100
BULLET_SPEED = 300


def animate(key: float, length: int, frame_speed: float) -> float:
    key += frame_speed
    if key >= length:
        key = 0
    return key


def get_rect(surf: pg.Surface, pos: pg.Vector2 | List[int]) -> pg.Rect:
    return surf.get_rect(center=pos)


def enemy_movement(enemy_pos: List[List[int]], delta: float, direction: int) -> None:
    for idx in range(len(enemy_pos)):
        enemy_pos[idx][0] += direction * delta
        

def player_bullet_movement(
    bullet_pos: List[pg.Vector2], delta: float
) -> List[pg.Vector2]:
    bullet_pos = list(filter(lambda pos: pos.y > 0, bullet_pos))

    for pos in bullet_pos:
        pos.y -= BULLET_SPEED * delta

    return bullet_pos
            
    
def enemy_bullet_movement(
    bullet_pos: List[pg.Vector2], delta: float
) -> List[pg.Vector2]:
    bullet_pos = list(filter(lambda pos: pos.y < DISPLAY_HEIGHT, bullet_pos))
    for pos in bullet_pos:
        pos.y += BULLET_SPEED * delta

    return bullet_pos


def player_movement(pos: pg.Vector2, delta: float, player: pg.Surface) -> None:
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        pos.x -= PLAYER_SPEED * delta
    if keys[pg.K_d]:
        pos.x += PLAYER_SPEED * delta

    if pos.x <= player.size[0] // 2:
        pos.x = player.size[0] // 2
    if pos.x >= DISPLAY_WIDTH - player.size[0] // 2:
        pos.x = DISPLAY_WIDTH - player.size[0] // 2


def main() -> None:
    pg.display.set_caption("Space invaders")
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    display = pg.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    clock = pg.Clock()
    running = True

    # background = pg.image.load("assets/images/background.png")

    # Player
    player: List[pg.Surface] = [
        pg.transform.rotate(pg.image.load("assets/images/player/1.png"), 90),
        pg.transform.rotate(pg.image.load("assets/images/player/2.png"), 90),
    ]
    player_key = 0
    player_pos = pg.Vector2(PLAYER_START)

    # Enemy
    enemy_rows = 4
    enemy_cols = 11
    enemy1: pg.Surface = pg.image.load("assets/images/enemy/1.png")
    enemy2: pg.Surface = pg.image.load("assets/images/enemy/2.png")
    enemy_pos: List[List[int]] = [
        [col * (8 + 8) + 10, row * (8 + 8) + 10, row]  # [x, y, enemy_colour]
        for row in range(enemy_rows)
        for col in range(enemy_cols)
    ]
    enemy_right = True

    # Defense
    defense: List[pg.Surface] = [
        pg.image.load("assets/images/defense/1.png"),
        pg.image.load("assets/images/defense/2.png"),
        pg.image.load("assets/images/defense/3.png"),
        pg.image.load("assets/images/defense/4.png"),
        pg.image.load("assets/images/defense/5.png"),
    ]
    defense_pos: List[List[int]] = [
        [(i * 16) + 10, 145, 0] for i in range(11)
    ]  # (x, y, frame)
    defense_key = 0

    # Bullet
    player_bullet: pg.Surface = pg.image.load("assets/images/bullet/2.png")
    enemy_bullet: pg.Surface = pg.image.load("assets/images/bullet/1.png")
    player_bullets_pos: List[pg.Vector2] = list()
    enemy_bullets_pos: List[pg.Vector2] = list()
    enemy_shoot = pg.USEREVENT + 1
    pg.time.set_timer(enemy_shoot, 1000)

    while running:
        delta = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                player_bullets_pos.append(player_pos.copy())
            if event.type == enemy_shoot:
                idx = randint(0, len(enemy_pos) - 1)
                pos = pg.Vector2(
                    enemy_pos[idx][:2]
                )
                enemy_bullets_pos.append(pos)

        display.fill((0, 0, 0))

        player_key = animate(player_key, len(player), 0.1)

        # Bullet render
        for pos in player_bullets_pos:
            display.blit(player_bullet, get_rect(player_bullet, pos))

        for pos in enemy_bullets_pos:
            display.blit(enemy_bullet, get_rect(enemy_bullet, pos))

        # Enemy render
        for pos in enemy_pos:
            if pos[2] % 2 == 0:
                display.blit(enemy1, get_rect(enemy1, pos[:2]))
            else:
                display.blit(enemy2, get_rect(enemy2, pos[:2]))

        # Player render
        display.blit(
            player[int(player_key)], get_rect(player[int(player_key)], player_pos)
        )

        # Defence render
        for pos in defense_pos:
            display.blit(defense[defense_key], get_rect(defense[defense_key], pos[:2]))


        # enemies going out of screen, because checking for the last element in enemy_pos
        if enemy_pos:
            if enemy_pos[0][0] <= enemy1.size[0] // 2:
                enemy_right = True
                for pos in enemy_pos:
                    pos[1] += 1
            elif enemy_pos[-1][0] >= DISPLAY_WIDTH - enemy1.size[0] // 2:
                enemy_right = False
                for pos in enemy_pos:
                    pos[1] += 1

        # Collisions
        for i, bullet_pos in sorted(enumerate(player_bullets_pos)):
            bullet_rect = get_rect(player_bullet, bullet_pos)
            for j, e_pos in sorted(enumerate(enemy_pos)):
                enemy = enemy1 if e_pos[2] % 2 == 0 else enemy2
                enemy_rect = get_rect(enemy, e_pos[:2])
                if bullet_rect.colliderect(enemy_rect):
                    player_bullets_pos.pop(i)
                    enemy_pos.pop(j)
                    break
                        
        enemy_dir = ENEMY_SPEED if enemy_right else -ENEMY_SPEED

        player_bullets_pos = player_bullet_movement(player_bullets_pos, delta)
        enemy_bullets_pos = enemy_bullet_movement(enemy_bullets_pos, delta)
        enemy_movement(enemy_pos, delta, enemy_dir)
        player_movement(player_pos, delta, player[int(player_key)])

        screen.blit(pg.transform.scale(display, screen.size), (0, 0))

        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
