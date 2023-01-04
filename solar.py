import pygame
import math
import scene
import resource
import body
import random

class Solar:
	##	Borg object
	__shared_state = {}

	def __init__(self, res_man, scn):
		self.__dict__ = self.__shared_state

		###	Utilities given by the caller: resource manager and initialized scene with open window
		self.res = res_man
		self.scn = scn

		###	Objects of the simulation
		##	the background sprite
		self.background = None
		##	the solar system data
		self.system_data = None
		##	the actual bodies
		self.bodies = {}

		##	sfml views: the background view, which does not move, and the solar system view which can be zoomed and translated
		self.bgview = None
		self.bodyview = None

		##	sprite of the Sun
		self.sun = None

	def init(self):
		##	load some textures
		#	sun texture
		self.sun_t = self.res.load_tex("resources/sun_fullres_transparent.png")
		#self.sun_t = self.sun_t.convert_alpha()
		self.sun = pygame.transform.scale(self.sun_t, (50, 50))

		screen_w, screen_h = pygame.display.get_window_size()
		##	set up the background
		self.background = pygame.Surface((screen_w, screen_h))
		## instead of using a texture for the background, let's build it
		## procedurally by drawing stars uniformly on a black surface
		self.background.fill((0, 0, 0))
		# TODO add colours and glow to background stars
		background_star_density = 0.0075 # stars / pixel
		background_area = screen_w * screen_h

		def clamp(x, low, high):
			return max(min(x, high), low)

		for i in range(int(background_area * background_star_density)):
			x = random.randint(0, screen_w)
			y = random.randint(0, screen_h)
			# Take the radius from a Gaussian centered on zero with sigma=1
			radius = int(abs(random.gauss(0, 1)))
			intensity = int((random.gauss(150, 50)))
			blueness = int(random.gauss(0, 20))
			red = clamp(intensity - blueness, 0, 255)
			green = clamp(intensity, 0, 255)
			blue = clamp(intensity + blueness, 0, 255)
			pygame.draw.circle(self.background, (red, green, blue), (x, y), radius)


		##	parse the solar system data
		self.system_data = resource.parse_json("system.json")

		##	populate a dictionary of bodies
		# for body_data in self.system_data["bodies"]:
		# 	self.bodies[body_data["name"]] = body.Body()
		# 	self.bodies[body_data["name"]].populate(body_data)


		#self.sun.origin = (sun_t.size.x / 2., sun_t.size.y / 2.)
		#self.sun.scale((0.001, 0.001))

		# ##	initialize the views
		# self.bgview = self.scn.default_view()
		# self.bodyview = self.scn.default_view()
		
		# #	TODO setup so that initial view shows orbit of earth
		# self.bodyview.move(-self.scn.size().x / 2., -self.scn.size().y / 2.)
		# self.bodyview.zoom(0.005)

	def update(self):
		# ##	handle inputs
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
		# 	self.bodyview.move(-0.02, 0)
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.D):
		# 	self.bodyview.move(0.02, 0)
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
		# 	self.bodyview.move(0, 0.02)
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
		# 	self.bodyview.move(0, -0.02)
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.E):
		# 	self.bodyview.zoom(0.99)
		# if sf.Keyboard.is_key_pressed(sf.Keyboard.Q):
		# 	self.bodyview.zoom(1.01)
		
		##	small rotating effect on the Sun
		#self.sun.rotate(0.01)
		pass

	def draw(self):
		# self.scn.clear()
		# self.scn.draw(self.background, self.bgview)

		# for k in self.bodies:
		# 	self.scn.draw(self.bodies[k].ellipse, self.bodyview)
		# self.scn.draw(self.sun, self.bodyview)
		# self.scn.render()
		#self.sun = pygame.transform.rotate(surface, angle)(self.sun, 0.0001)
		self.scn.window.blit(self.background, (0, 0))
		sz = self.sun.get_size()
		scale = (1 + 0.1 * math.cos(2 * math.pi * 0.001 * pygame.time.get_ticks()))
		#scaled = pygame.transform.scale(self.sun, (sz[0] * scale, sz[0] * scale))
		rotated = pygame.transform.rotozoom(self.sun, -2 * math.pi * 0.001 * pygame.time.get_ticks(), 1)
		self.scn.window.blit(rotated, rotated.get_rect(center=(0, 0)))

'''
def main():

	##	read settings from settings.json and store them
	settings = parse_json("settings.json")

	##	initialize resource manager
	res_man = resource.Manager()

	##	open window
	scn = scene.Scene()
	scn.open_window(sf.VideoMode(settings["window"]["width"], settings["window"]["height"]), settings["window"]["name"], sf.window.Style.CLOSE, sf.ContextSettings(0, 0, settings["window"]["antialias"], 2, 0))
	scn.set_window_icon(sf.Image.from_file("sun.png"))



	##	get list of system bodies from a json file
	system_data = parse_json("system.json")

	##	load background image
	background_t = res_man.load_tex("stars.jpg")
	background = sf.Sprite(background_t)
	scale = settings["window"]["width"] / background_t.size.x
	background.scale((scale, scale))
	background.move((0, 0))
	##	make it a little fainter
	background.color = sf.Color(255, 255, 255, 150)

	
	##	time to process some data and populate a dictionary
	##	first define a C-struct like class called Body that will hold useful information for drawing bodies and their trajectories
	class Body:
		def __init__(self):
			##	semimajor axis
			self.a = 0
			##	semiminor axis
			self.b = 0
			##	eccentricity
			self.e = 0
			##	orbit's inclination
			self.incl = 0
			##	argument of perihelion
			self.peri = 0
			##	orbit color
			self.col = sf.Color.BLACK
			##	orbit ellipse
			self.ellipse = sf.ConvexShape()

	##	this dictionary will hold the data
	bodies = {}
	for body_data in system_data["bodies"]:
		bodies[body_data["name"]] = Body()
		b = bodies[body_data["name"]]
		
		b.a = body_data["orbit"]["semimajor"]
		b.e = body_data["orbit"]["eccentricity"]
		b.incl = body_data["orbit"]["inclination"]
		b.peri = body_data["orbit"]["arg_of_peri"]
		b.col = body_data["color"]
		
		##	compute semiminor axis from definitions of f (focal point) and e (eccentricity): f^2 = a^2 - b^2, e = f/a  =>  b = a*sqrt(-e^2 + 1)
		b.b = b.a * math.sqrt(-b.e**2 + 1)
		
		##	create the body's orbit using sfml's convex shape object
		quality = 100
		b.ellipse.point_count = quality
		##	draw as many points as 'quality' goes
		for i in range(quality):
			theta = math.pi * 2.0 * i / quality
			b.ellipse.set_point(i, (b.a * math.cos(theta) * math.cos(b.incl * 2. * math.pi / 360.), b.b * math.sin(theta)))
			b.ellipse.fill_color = sf.Color.TRANSPARENT
			b.ellipse.outline_color = sf.Color(b.col[0], b.col[1], b.col[2], b.col[3])
			##	scale the thickness as semimajor increases (might need tweaking for very big/small orbits)
			b.ellipse.outline_thickness = 0.015 * b.a
		##	place the shape's origin at (-focus, 0) so that its origin is the same as the sun's
		focus = b.a * b.e
		b.ellipse.origin = (-focus, 0)
		##	we can then rotate it according to its 'Argument of perihelion'
		b.ellipse.rotate(b.peri)

	#	draw the sun in the origin
	sun_t = res_man.load_tex("sun.png")
	sun = sf.Sprite(sun_t)
	sun.origin = (sun_t.size.x / 2., sun_t.size.y / 2.)
	sun.scale((0.001, 0.001))

	bgview = scn.default_view()
	bodyview = scn.default_view()
	
	bodyview.move(-scn.size().x / 2., -scn.size().y / 2.)
	bodyview.zoom(0.005)

	while scn.running():
		scn.handle_events()

		if sf.Keyboard.is_key_pressed(sf.Keyboard.A):
			bodyview.move(-0.02, 0)
		if sf.Keyboard.is_key_pressed(sf.Keyboard.D):
			bodyview.move(0.02, 0)
		if sf.Keyboard.is_key_pressed(sf.Keyboard.S):
			bodyview.move(0, 0.02)
		if sf.Keyboard.is_key_pressed(sf.Keyboard.W):
			bodyview.move(0, -0.02)
		if sf.Keyboard.is_key_pressed(sf.Keyboard.E):
			bodyview.zoom(0.99)
		if sf.Keyboard.is_key_pressed(sf.Keyboard.Q):
			bodyview.zoom(1.01)
		
		
		sun.rotate(0.01)

		#	render
		scn.clear()
		scn.draw(background, bgview)

		for k in bodies:
			scn.draw(bodies[k].ellipse, bodyview)
		scn.draw(sun, bodyview)
		scn.render()

'''
