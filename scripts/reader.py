from PIL import Image
from pytesseract import pytesseract
import urllib.request

###
# Code between these lines were leveraged from Geeks for Geeks
# https://www.geeksforgeeks.org/how-to-extract-text-from-images-with-python/
#  ----------------------------------------------------------------------------
###

# tesseract
tesseractexe_path = r"/usr/local/bin/tesseract"

# image to be read
urllib.request.urlretrieve("https://media-prd.coachella.com/content/tile_images/76/Er4Yzu3r6iiCKgNbOoDseeJaH1ceqtQImXiRSpDA.jpeg", "image.jpeg")

# open and store image as object
img = Image.open("image.jpeg")
img.show()

# Providing tesseract executable location to pytesseract lib
pytesseract.tesseract_cmd = tesseractexe_path

# Pass image object to image_to_string() function to extract text
text = pytesseract.image_to_string(img)

print(text)

# -----------------------------------------------------------------------------