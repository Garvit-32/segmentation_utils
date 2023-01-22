import matplotlib.pyplot as plt
from PIL import Image


img = Image.open('mask/0b23fb62b2624c7588da634875907631-1623259906500003313.png')
plt.imshow(img)
plt.show()