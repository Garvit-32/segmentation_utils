# https://stackoverflow.com/questions/50805634/how-to-create-mask-images-from-coco-dataset

from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


coco = COCO('test.json')
img_dir = 'image'
image_id = 0

img = coco.imgs[image_id]

# loading annotations into memory

image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
# image = np.array(Image.open(os.path.join(img_dir, img['file_name'])).convert('RGB'))
plt.imshow(image, interpolation='nearest')
plt.show()

plt.imshow(image)
cat_ids = coco.getCatIds()
anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
anns = coco.loadAnns(anns_ids)
coco.showAnns(anns)
plt.savefig('test.png')
plt.show()


# mask = coco.annToMask(anns[0])
# for i in range(len(anns)):
#     mask += coco.annToMask(anns[i])

# plt.imshow(mask)
# plt.show()