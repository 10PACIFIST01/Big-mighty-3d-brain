import pygame
from matrix_functions import *
import numpy as np
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
	return np.any((arr == a) | (arr == b))


class Object:
	def __init__(self, render, vertexes, faces):
		self.render = render
		self.vertexes = np.array([np.array(v) for v in vertexes])

		self.faces = np.array([np.array(face) for ind, face in enumerate(faces) if ind % 20 == 0])
		self.draw_vertexes = False

	def draw(self):
		self.screen_projection()
		#self.movement()

	def movement(self):
		self.rotate_y(pygame.time.get_ticks() % 0.005)

	def screen_projection(self):
		vertexes = self.vertexes @ self.render.camera.camera_matrix()
		vertexes = vertexes @ self.render.projection.projection_matrix
		vertexes /= vertexes[:, -1].reshape(-1, 1)
		vertexes[(vertexes > 2) | (vertexes < -2)] = 0
		vertexes = vertexes @ self.render.projection.to_screen_matrix
		vertexes = vertexes[:, :2]

		for face in self.faces:
			polygon = vertexes[face]
			if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
				pygame.draw.polygon(self.render.screen, pygame.Color("orange"), polygon, 1)

		if self.draw_vertexes:
			for vertex in vertexes:
				if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
					pygame.draw.circle(self.render.screen, pygame.Color("white"), vertex, 2)

	def translate(self, pos):
		self.vertexes = self.vertexes @ translate(pos)

	def scale(self, scale_to):
		self.vertexes = self.vertexes @ scale(scale_to)

	def rotate_x(self, angle):
		self.vertexes = self.vertexes @ rotate_x(angle)

	def rotate_y(self, angle):
		self.vertexes = self.vertexes @ rotate_y(angle)

	def rotate_z(self, angle):
		self.vertexes = self.vertexes @ rotate_z(angle)