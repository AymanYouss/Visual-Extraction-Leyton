from spire.pdf.common import *
from spire.pdf import *

# Create a PdfDocument object
doc = PdfDocument()

# Load a PDF document
doc.LoadFromFile('C:/Users/Administrator/Desktop/input.pdf')

# Get a specific page
page = doc.Pages[1]

# Extract images from the page
images = []
for image in page.ExtractImages():
    images.append(image)

# Save images to specified location with specified format extension
index = 0
for image in images:
    imageFileName = 'C:/Users/Administrator/Desktop/Extracted/Image-{0:d}.png'.format(index)
    index += 1
    image.Save(imageFileName, ImageFormat.get_Png())
doc.Close()