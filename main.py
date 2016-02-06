import resource
import scene
import solar
import sfml as sf

def main():
	##	read settings from settings.json and store them
	settings = resource.parse_json("settings.json")

	##	initialize resource manager
	res_man = resource.Manager()

	##	open window
	scn = scene.Scene()
	scn.open_window(sf.VideoMode(settings["window"]["width"], settings["window"]["height"]), settings["window"]["name"], sf.window.Style.CLOSE, sf.ContextSettings(0, 0, settings["window"]["antialias"], 2, 0))
	scn.set_window_icon(sf.Image.from_file("sun.png"))

	##	send all that to the app
	app = solar.Solar(res_man, scn)
	app.init()

	while scn.running():
		scn.handle_events()

		app.update()
		app.render()



if __name__ == "__main__":
	main()