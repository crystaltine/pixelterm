import blessed
term = blessed.Terminal()

with term.cbreak():
	while True:
		key = term.inkey()

		if key.code == term.KEY_ESCAPE:
			print("exiting")
			break

		print(f"key pressed, key.name: {key.name}, key.code: {key.code}")