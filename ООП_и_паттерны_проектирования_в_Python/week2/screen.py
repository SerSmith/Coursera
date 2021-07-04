#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d:
    def __init__(self, coords):
        self.coords = coords

    def __add__(self, other):
        """Cумма двух векторов"""
        return Vec2d([self.coords[0] + other.coords[0],
                      self.coords[1] + other.coords[1]])

    def __sub__(self, other):
        """"Разность двух векторов"""
        return Vec2d([self.coords[0] - other.coords[0],
                      self.coords[1] - other.coords[1]])

    def __mul__(self, k):
        """Произведение вектора на число"""
        return Vec2d([self.coords[0] * k,
                      self.coords[1] * k])

    def length(self):
        """Длина вектора"""
        return math.sqrt(self.coords[0] * self.coords[0] + self.coords[1] * self.coords[1])

    def int_pair(self):
        """Возвращет координаты"""
        return self.coords[0], self.coords[1]


class Polyline:
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        """Добавление точки"""
        self.points.append(point)
        self.speeds.append(speed)
    
    def del_last_point(self):
        """Удаление последней добавленной точки"""
        if len(self.points) > 0:
            self.points = self.points[:-1]
            self.speeds = self.speeds[:-1]

    def set_points(self):
        """Перерасчет координат опорных точек"""
        for num in range(len(self.points)):
            self.points[num] = self.points[num] + self.speeds[num]

            if self.points[num].coords[0] > SCREEN_DIM[0] or self.points[num].coords[0] < 0:
                self.speeds[num] = Vec2d([-self.speeds[num].coords[0], self.speeds[num].coords[1]])

            if self.points[num].coords[1] > SCREEN_DIM[1] or self.points[num].coords[1] < 0:
                self.speeds[num] = Vec2d([self.speeds[num].coords[0], -self.speeds[num].coords[1]])

    def draw_points(self, width=3, color=(255, 255, 255)):
        """функция отрисовки точек на экране"""
        for p in self.points:
            pygame.draw.circle(gameDisplay,
                               color,
                               (int(p.coords[0]), int(p.coords[1])),
                               width)

    def speed_change(self, mult):
        """Кратное изменений скорости"""
        for s in range(len(self.speeds)):
            self.speeds[s].coords = [mult * i for i in self.speeds[s].coords]


class Knot(Polyline):

    def __init__(self):
        super().__init__()
        self.knots = []
    
    def draw_lines(self, width=3, color=(255, 255, 255)):
        """функция отрисовки линий на экране"""
        for p_n in range(-1, len(self.knots) - 1):
            pygame.draw.line(gameDisplay,
                             color,
                             (int(self.knots[p_n].coords[0]), int(self.knots[p_n].coords[1])),
                             (int(self.knots[p_n + 1].coords[0]), int(self.knots[p_n + 1].coords[1])),
                             width)

    def draw_knots(self, count, width=3, color=(255, 255, 255)):
        """Расчет и отрисовка кривой"""
        self.calculate_knots(count)
        self.draw_lines(width, color)

    def calculate_knots(self, count):
        if len(self.points) < 3:
            self.knots = []
        else:
            res = []
            for i in range(-2, len(self.points) - 2):
                ptn = []
                ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

                res.extend(Knot.get_points(ptn, count))
            self.knots = res

    @staticmethod
    def get_points(base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(Knot.get_point(base_points, i * alpha))
        return res

    @staticmethod
    def get_point(points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + Knot.get_point(points, alpha, deg - 1) * (1 - alpha)


def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["F", "Speed X2"])
    data.append(["S", "Speed X1/2"])
    data.append(["BackSpace", "Delete last point"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay,
                      (255, 50, 50, 255),
                      True,
                      [(0, 0),
                       (800, 0),
                       (800, 600),
                       (0, 600)],
                      5)

    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(text[0],
                                      True,
                                      (128, 128, 255)),
                         (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(text[1],
                                      True,
                                      (128, 128, 255)),
                         (200, 100 + 30 * i))

# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    speed_mult = 2
    working = True
    knots = Knot()
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    knots = Knot()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_f:
                    knots.speed_change(speed_mult)
                if event.key == pygame.K_s:
                    knots.speed_change(1 / speed_mult)
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_BACKSPACE:
                    knots.del_last_point()
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = Vec2d(event.pos)
                speed = Vec2d([random.random() * 2, random.random() * 2])

                knots.add_point(pos, speed)


        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        knots.draw_points()
        knots.draw_knots(steps, 3, color)
        if not pause:
            knots.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
