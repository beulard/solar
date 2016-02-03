import sfml as sf

###	Loads and returns resources like sfml textures and fonts
class Manager:
	##	make this a Borg object
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state
		self.textures = {}
		self.fonts = {}

	##	add a texture to the available resources
	def load_tex(self, file):
		self.textures[file] = sf.Texture.from_file(file)
		return self.textures[file]

	##	add a font to the available resources
	def load_font(self, file):
		self.fonts[file] = sf.Font.from_file(file)
		return self.fonts[file]