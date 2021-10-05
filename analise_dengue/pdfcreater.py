import glob
from PIL import Image

mainImage = Image.open(r"figures/Angra dos Reis.png")
finalMainImage = mainImage.convert('RGB')

imageList = []
for filename in glob.glob(r'figures/*.png'):
    if (filename != "figures/Angra dos Reis.png"):
        im = Image.open(filename)
        im1 = im.convert('RGB')
        imageList.append(im1)

finalMainImage.save(r'AnaliseDengueRJ.pdf', save_all=True, append_images=imageList)