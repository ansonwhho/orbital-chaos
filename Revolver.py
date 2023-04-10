'''
' R E V O L V E R '

28/03/2021
Alba Spahiu, Joel Beckles, Anson Ho

This is a 3D Gravity simulator: an interactive game, in which the user can create multiple dots
at the click of the mouse -> the more the mouse is kept clicked the more the mass. Each dot interacts with each other. There is an
initial dot in the centre of the window before the user has clicked, that is the star. It is 1000
times more massive that a dot of the same size. This is to represent the fact that in reality,
the Sun holds 99.8% of the mass of our solar system, interacting with objects very small that are very
far away (planets). All dots collide with each other if they can, and each influences each other's
gravity. If two dots collide their masses and areas will merge into the bigger dot.

Install:
PyGame --> https://www.pygame.org/news

Getting Started:
The goal is to find a way to make dots revolve (orbit) around the star and each other.

'''

# TODO: Start not affected drastically by merge
# TODO: Score Board
# TODO: Vector Arrow
        # Stops frame, repaints existing objects but paints over arrow shape
# TODO: Stop Button

import pygame
import pygame.locals
import time
import math
from sys import exit

pygame.display.init()
window_dimensions = (1500, 900)

Screen = pygame.display.set_mode(window_dimensions)

R = (255, 0, 0)
G = (0, 255, 0)
B = (0, 0, 255)
Y = (253, 184, 19)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

gravity_constant = 300
dots = []


class Dot:
    '''
    The Dot class determines how dots are created (where, when) and how they interact with each other.
    Dots, which represent various stars and planets, are created at the click of the user. The longer
    a dot is clicked, the more massive it will become throut functions specified outside of this class,
    though user_input.
    '''

    def __init__(self, radius, mass, position, is_star):

        self.isBehind = False
        self.isStar = is_star

        self.color = WHITE
        self.mass = mass

        self.location_x = position[0]
        self.location_y = position[1]
        self.location_z = - 250

        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0

        self.radius = radius

        self.force = [0, 0, 0]

    def revolve(self, time_change):

        self.location_x += time_change * self.velocity_x  # distance = time * speed # d=vt
        self.location_y += time_change * self.velocity_y
        self.location_z += time_change * self.velocity_z

        if not self.isStar:
            self.radius = 10 + self.location_z / 50

        if self.mass > 0:
            x_accel = time_change * self.force[0] / self.mass  # acceleration = force / mass
            y_accel = time_change * self.force[1] / self.mass
            z_accel = time_change * self.force[2] / self.mass
            self.velocity_x += x_accel  # this is so that when
            self.velocity_y += y_accel
            self.velocity_z += z_accel

        self.force[0] = 0.0
        self.force[1] = 0.0
        self.force[2] = 0.0

    def merge_force(self, dot2):

        x_change = dot2.location_x - self.location_x
        y_change = dot2.location_y - self.location_y
        z_change = dot2.location_z - self.location_z

        rad_s = x_change ** 2 + y_change ** 2 + z_change ** 2  # Pythagorean theorem to find distance
        r = rad_s ** 0.5                                       # between two dots.

        if rad_s == 0:
            rad_s = 0.00000000001
            force_mag = (gravity_constant * self.mass * dot2.mass) / float(rad_s)  # F=G*M1*M2/(r^2)
        else:
            force_mag = (gravity_constant * self.mass * dot2.mass) / float(rad_s)

        dx_now = (x_change / r) * force_mag  # This determines the displacement of the dots as directly
        dy_now = (y_change / r) * force_mag  # proportional to the gravitational force between two dots.
        dz_now = (z_change / r) * force_mag

        self.force[0] += dx_now  # This is why the initial force values were set to 0,
        self.force[1] += dy_now  # because it is a function that feeds back to itself
        self.force[2] += dz_now  # and changes force mag based on individual dot interactions.

        dot2.force[0] -= dx_now
        dot2.force[1] -= dy_now
        dot2.force[2] -= dz_now

    def go_behind(self):
        star = dots[0]
        x_change = star.location_x - self.location_x
        y_change = star.location_y - self.location_y
        if star != self:
            distance = math.sqrt(x_change ** 2 + y_change ** 2)
            add_radius = self.radius + star.radius
            if distance <= add_radius:
                if self.location_z - self.radius <= star.location_z + star.radius:
                    self.isBehind = True
                else:
                    self.isBehind = False
            else:
                self.isBehind = False

    def tell_behind(self):
        for n in range(len(dots)):
            self.go_behind()

    def disappear(self):
        self.mass = 0
        self.radius = 0

    def merge(self, dot):
        if self.radius >= dot.radius:
            # self.radius += dot.radius / 2
            # self.mass += dot.mass
            dot.disappear()
        else:
            # dot.radius += self.radius / 2
            # dot.mass += self.mass
            self.disappear()

    def dot_merge(self):
        for n in range(len(dots)):
            x_change = dots[n].location_x - self.location_x
            y_change = dots[n].location_y - self.location_y
            z_change = dots[n].location_z - self.location_z
            if dots[n] != self:
                distance = math.sqrt(x_change ** 2 + y_change ** 2 + z_change ** 2)
                add_radius = self.radius + dots[n].radius
                if distance <= add_radius:
                    self.merge(dots[n])


def dot_color(self):
    color = Y
    max_vz = 255
    min_vz = - max_vz
    scale = (max_vz - min_vz) / 255

    c = int(self.velocity_z / scale) + 127
    if not self.isStar:
        if max_vz > self.velocity_z > min_vz:
            color = (255-c, 0, c)
        elif self.velocity_z < min_vz:
            color = R
        else:
            color = B

    return color


def revolve_dots():
    total = len(dots)
    for i in range(total - 1):
        Dot.dot_merge(dots[i])
        Dot.tell_behind(dots[i])
        for j in range(i + 1, total):
            dots[i].merge_force(dots[j])
    for dot in dots:
        dot.revolve(0.008)  # 0.5/60, time_change per frame


def start_timer():
    return time.time()


def end_timer(old_time):
    return time.time() - old_time


def draw_rectangle():
    s = pygame.Surface((1500, 900), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((0, 0, 0, 5))                              # notice the alpha value in the color
    Screen.blit(s, (0, 0))


def draw_star():
    pygame.draw.circle(Screen, Y,
                       (int(dots[0].location_x),
                        int(dots[0].location_y)),
                        int(dots[0].radius))


def draw():
    draw_rectangle()
    draw_star()
    for dot in dots:
        color = dot_color(dot)
        if dot.isBehind & (not dot.isStar):
            pygame.draw.circle(Screen, color,
                               (int(dot.location_x),
                                int(dot.location_y)),
                                int(dot.radius))
            draw_star()
        else:
            pygame.draw.circle(Screen, color,
                               (int(dot.location_x),
                                int(dot.location_y)),
                               int(dot.radius))
    return pygame.display.flip()


def user_input():
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.locals.MOUSEBUTTONDOWN:
            global t, x_i, y_i
            t = start_timer()
            x_i, y_i = pygame.mouse.get_pos()
        if event.type == pygame.locals.MOUSEBUTTONUP:
            global x_f, y_f
            x_f, y_f = pygame.mouse.get_pos()
            print(x_f, y_f)
            if t > 0.0:
                time_passed = end_timer(t)
                new_dot = Dot(10, time_passed, [x_i, y_i], False)
                new_dot.velocity_x = -(x_f - x_i)
                new_dot.velocity_y = -(y_f - y_i)
                new_dot.velocity_z = 0
                dots.append(new_dot)
    return running


def main():
    Screen.fill(BLACK)

    central_dot = Dot(40, 4000, (window_dimensions[0] / 2, window_dimensions[1] / 2), True)
    central_dot.location_z = 0

    dots.append(central_dot)
    dots[0].x_velocity = 0
    dots[0].y_velocity = 0
    dots[0].z_velocity = - 10
    while True:
        if not user_input():
            break
        revolve_dots()
        draw()
    pygame.display.quit()
    pygame.quit()
    exit()


main()
