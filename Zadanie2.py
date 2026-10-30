from PIL import Image
import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def main():
    #https://upload.wikimedia.org/wikipedia/commons/f/f9/Road_CS-240_at_Coll_d%27Ordino_%282%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original
    #https://upload.wikimedia.org/wikipedia/commons/9/94/Underexposed_photo.JPG?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original
    #print(len(requests.get("https://aijaz.net/wp/underPlain.jpg").content))
    
    headers = {"User-Agent": "Mozilla/5.0 (grzegorz.pacia@student.wsb.edu.pl)"}
    imageNormal = Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/f/ff/Road%2C_Mary_Peters_Track%2C_Belfast_-_geograph.org.uk_-_2493800.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw)
    imageOverexposed = Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/5/5c/Irvin_Kershner_%282004%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw)
    imageUnderexposed = Image.open(requests.get("https://upload.wikimedia.org/wikipedia/commons/5/51/Organo_Cripta_Monte.jpg?utm_source=commons.wikimedia.org&utm_campaign=index&utm_content=original", headers=headers, stream=True).raw)
    
    imageNormalArray = np.asarray(imageNormal)
    imageOverexposedArray = np.asarray(imageOverexposed)
    imageUnderexposedArray = np.asarray(imageUnderexposed)

    #print(str(imageUnderexposedArray))
    plt.imshow(imageNormalArray, cmap=cm.gray, vmin=0, vmax=255)
    plt.show()
    plt.imshow(imageOverexposedArray, cmap=cm.gray, vmin=0, vmax=255)
    plt.show()
    plt.imshow(imageUnderexposedArray, cmap=cm.gray, vmin=0, vmax=255)
    plt.show()
    
if __name__ == "__main__":
    main()