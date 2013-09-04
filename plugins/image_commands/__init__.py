

def tasks(tasklist, manifest):
	from image_commands import ImageExecuteCommand, ImageExecuteScript
	tasklist.add(ImageExecuteCommand())
	tasklist.add(ImageExecuteScript())
