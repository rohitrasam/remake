from pygame import Vector2


def temp(b, c):
    b.x += 1
    c[1] += 1




a = Vector2(2, 3)
b = [3, 2]
print(a, b)
temp(a, b)
print(a, b)