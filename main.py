from typing import List
import pygame as pg


def animate(key: float, length: int, frame_speed: float) -> float:
    key += frame_speed
    if key >= length:
        key = 0
    return key


def get_rect(surf: pg.Surface, pos: pg.Vector2 | List[int]) -> pg.Rect:
    return surf.get_rect(center=pos)


def enemy_movement() -> None:
    pass


def player_movement(pos: pg.Vector2, delta: float, player: pg.Surface) -> None:
    keys = pg.key.get_pressed()
    if keys[pg.K_a]:
        pos.x -= 100 * delta
    if keys[pg.K_d]:
        pos.x += 100 * delta

    if pos.x <= player.size[0] // 2:
        pos.x = player.size[0] // 2
    if pos.x >= 180 - player.size[0] // 2:
        pos.x = 180 - player.size[0] // 2


def main() -> None:
    screen = pg.display.set_mode((720, 480))
    display = pg.Surface((180, 120))
    clock = pg.Clock()
    running = True
    player: List[pg.Surface] = [
        pg.transform.rotate(pg.image.load("assets/images/player/1.png"), 90),
        pg.transform.rotate(pg.image.load("assets/images/player/2.png"), 90),
    ]
    player_key = 0
    player_pos = pg.Vector2(90, 105)

    enemy1: pg.Surface = pg.image.load("assets/images/enemy/1.png")
    enemy2: pg.Surface = pg.image.load("assets/images/enemy/2.png")
    enemy1_pos: List[List[int]] = [
        [(i * 16) + 10, 0] for i in range(11)
    ]  # [(x1, frame1)]
    enemy1_y = 15
    enemy2_pos: List[List[int]] = [
        [(i * 16) + 10, 0] for i in range(11)
    ]  # [(x1, frame1)]
    enemy2_y = 31

    defense: List[pg.Surface] = [
        pg.image.load("assets/images/defense/1.png"),
        pg.image.load("assets/images/defense/2.png"),
        pg.image.load("assets/images/defense/3.png"),
        pg.image.load("assets/images/defense/4.png"),
        pg.image.load("assets/images/defense/5.png"),
    ]
    defense_pos: List[List[int]] = [
        [(i * 16) + 10, 80, 0] for i in range(11)
    ]  # (x, y, frame)
    defense_key = 0

    while running:
        delta = clock.tick(60) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        display.fill((0, 0, 0))

        player_key = animate(player_key, len(player), 0.1)

        for pos in enemy1_pos:
            display.blit(enemy1, get_rect(enemy1, [pos[0], enemy1_y]))

        for pos in enemy2_pos:
            display.blit(enemy2, get_rect(enemy2, [pos[0], enemy2_y]))

        for pos in defense_pos:
            display.blit(defense[defense_key], get_rect(defense[defense_key], pos[:2]))

        display.blit(
            player[int(player_key)], get_rect(player[int(player_key)], player_pos)
        )

        player_movement(player_pos, delta, player[int(player_key)])

        screen.blit(pg.transform.scale(display, screen.size), (0, 0))

        pg.display.update()


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
