

def tasks(tasklist, manifest):
	from image_scripts import ImageExecuteCommand, ImageExecuteScript
	tasklist.add(ImageExecuteCommand())
	tasklist.add(ImageExecuteScript())
