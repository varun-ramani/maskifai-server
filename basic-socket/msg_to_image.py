from PIL import Image

img = Image.new('RGBA', (1920, 1080), 'black')

pixels = img.load()

with open('message.raw', 'rb') as file:
    row = 0
    col = 0

    for i in file.read():
        pixels[row, col] = 

img.show()
