from sfml import sf

###	Handles the sfml window as well as the drawing of sprites and the window event loop. ###
class Scene:
	##	make this a Borg object
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state
		self.window = None
		self.event_handler = None

	def open_window(self, mode, name, style, context_settings):
		self.window = sf.RenderWindow(mode, name, style, context_settings)

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
	def clear(self, color = sf.Color.BLACK):
		self.window.clear(color)

	##	returns default view
	def default_view(self):
		return self.window.default_view

	##	returns window size
	def size(self):
		return self.window.size

	##	in case you want to replace the default event handling (escape and close button close the window), you can replace it with your 
	##	own (which takes a sf.Window) in argument
	def set_event_handler(self, handler):
		self.event_handler = handler

	def handle_events(self):
		if self.event_handler is None:
			for event in self.window.events:
				##	shut down if the window is closed or if escape is pressed
				if event == sf.CloseEvent:
					self.window.close()
				elif event == sf.KeyEvent:
					if event.code == sf.Keyboard.ESCAPE:
						self.window.close()
		else:
			self.event_handler(self.window)

	##	draw a sprite with the provided view or the default one
	def draw(self, sprite, view = None):
		if view is None:
			self.window.view = self.window.default_view
		else:
			self.window.view = view
		self.window.draw(sprite)

	##	display the window
	def render(self):
		self.window.display()


