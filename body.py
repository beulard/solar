from sfml import sf
import math

##	Body holds an orbiting body's properties (physical and graphical). This data can be populated with the 'populate' function.
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


	##	Transform the data held by a json object into this Body. A 'quality' value can be given if the amount of vertices in the 
	##	ellipse is inappropriate.
	def populate(self, json_body, quality = 100):
		self.a = json_body["orbit"]["semimajor"]
		self.e = json_body["orbit"]["eccentricity"]
		self.incl = json_body["orbit"]["inclination"]
		self.peri = json_body["orbit"]["arg_of_peri"]
		self.col = json_body["color"]
		
		##	compute semiminor axis from definitions of f (focal point) and e (eccentricity): f^2 = a^2 - self^2, e = f/a  =>  self = a*sqrt(-e^2 + 1)
		self.b = self.a * math.sqrt(-self.e**2 + 1)
		
		##	create the body's orbit using sfml's convex shape object
		self.ellipse.point_count = quality
		##	draw as many points as 'quality' goes
		for i in range(quality):
			theta = math.pi * 2.0 * i / quality
			self.ellipse.set_point(i, (self.a * math.cos(theta) * math.cos(self.incl * 2. * math.pi / 360.), self.b * math.sin(theta)))
			self.ellipse.fill_color = sf.Color.TRANSPARENT
			self.ellipse.outline_color = sf.Color(self.col[0], self.col[1], self.col[2], self.col[3])
			##	scale the thickness as semimajor increases (might need tweaking for very big/small orbits)
			self.ellipse.outline_thickness = 0.015 * self.a
		##	place the shape's origin at (-focus, 0) so that its origin is the same as the sun's
		focus = self.a * self.e
		self.ellipse.origin = (-focus, 0)
		##	we can then rotate it according to its 'Argument of perihelion'
		self.ellipse.rotate(self.peri)
