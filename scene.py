import pygame

###	Handles the sfml window as well as the drawing of sprites and the window event loop. ###
class Scene:
	##	make this a Borg object
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state
		self.window = None

	def open_window(self, size, title, antialias):
		self.window = pygame.display.set_mode(size)
		pygame.display.set_caption(title)
		# Antialias

	def set_window_icon(self, image):
		self.window.icon = image.pixels

	def close_window(self):
		self.window.close()

	def get_window_size(self):
		return self.window.size

	##	is the window still open?
	def running(self):
		return self.window.is_open

	##	clears the window with provided color
	def clear(self, color=(0, 0, 0)):
		self.window.fill(color)

	##	returns default view
	def default_view(self):
		return self.window.default_view

	##	returns window size
	def size(self):
		return self.window.size

	##	draw a sprite with the provided view or the default one
	def draw(self, sprite, view = None):
		if view is None:
			self.window.view = self.window.default_view
		else:
			self.window.view = view
		self.window.draw(sprite)

	##	display the window
	def update(self):
		pygame.display.flip()


