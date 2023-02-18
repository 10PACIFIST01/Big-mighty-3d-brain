from object_3d import *
from camera import *
from projection import *
import pygame


class SoftwareRender:
	def __init__(self):
		pygame.init()
		self.RES = self.WIDTH, self.HEIGHT = 1300, 700
		self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
		self.FPS = 60

		self.screen = pygame.display.set_mode(self.RES)
		self.clock = pygame.time.Clock()
		self.create_objects()

	def create_objects(self):
		self.camera = Camera(self, [-5, -5, 7])
		self.projection = Projection(self)
		self.object = self.get_object_from_file("Brain_Model.obj")
		self.object.rotate_z(3.14)

	def get_object_from_file(self, filename):
		vertexes, faces = [], []
		with open(filename) as file:
			for line in file.readlines():
				if line.startswith("v "):
					vertexes.append([float(i) for i in line.split()[1:]] + [1])
				elif line.startswith("f"):
					faces_ = line.split()[1:]
					faces.append([int(face_.split("/")[0]) - 1 for face_ in faces_])
		return Object(self, vertexes, faces)

	def draw(self):
		self.screen.fill(pygame.Color("darkslategray"))
		self.object.draw()

	def run(self):
		while True:
			self.draw()

			self.camera.control()
			[exit() for i in pygame.event.get() if i.type == pygame.QUIT]
			pygame.display.set_caption(str(self.clock.get_fps()))

			pygame.display.flip()
			self.clock.tick(self.FPS)

if __name__ == "__main__":
	app = SoftwareRender()
	app.run()