import resource
import scene
import solar
import pygame

def main():
	##	read settings from settings.json and store them
	settings = resource.parse_json("settings.json")

	print(settings)

	##	initialize resource manager
	res_man = resource.Manager()

	pygame.init()

	##	open window
	scn = scene.Scene()
	win_cfg = settings["window"]
	scn.open_window((win_cfg["width"], win_cfg["height"]), win_cfg["name"], win_cfg["antialias"])
		#sf.VideoMode(settings["window"]["width"], settings["window"]["height"]), settings["window"]["name"], sf.Style.CLOSE, sf.ContextSettings(0, 0, settings["window"]["antialias"], 2, 0))
	#scn.set_window_icon(sf.Image.from_file("sun.png"))
	icon_s = pygame.image.load("resources/sun_icon.png")
	pygame.display.set_icon(icon_s)

	## initialise the solar system bodies
	solarsystem = solar.Solar(res_man, scn)
	solarsystem.init()

	sunsprite = pygame.sprite.from_surface(icon_s)

	running = True
	while running:
		# Handle window events: user quits, etc
		for event in pygame.event.get():
			##	shut down if the window is closed or if escape is pressed
			if event.type == pygame.QUIT:
				# Save or ask for confirmation before quitting here
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		scn.clear()
		# Draw
		#scn.window.blit(icon_s, (0, 0))

		pygame.draw.circle(scn.window, (255, 255, 255), (win_cfg["width"]/2 - 25, win_cfg["height"]/2 - 25), 50)

		solarsystem.update()
		solarsystem.draw()
		scn.update()
	 	
	# 	app.render()

	# Clean up
	pygame.quit()



if __name__ == "__main__":
	main()
