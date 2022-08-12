content_type = 'image/jpeg'
headers = {'content-type': content_type}

import requests
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle

script_dir = os.path.dirname(os.path.realpath(__file__))
rel_path = str(sys.argv[1])
abs_file_path = script_dir + "/" + rel_path 
print("Path to image file: " + abs_file_path)

screen = open(abs_file_path, 'rb')
files={'file': ('image.jpg', screen, content_type)}
res = requests.post('http://localhost:8000/upload', files=files)

print("Status Code: " + str(res.status_code))
print("Server Message: " + res.json()["message"])
print(res.json()["preds"])

bboxes = res.json()["preds"]["bboxes"]

print("Displaying Image...")

fig, ax = plt.subplots()

img = mpimg.imread(abs_file_path)

ax.imshow(img)
for bbox in bboxes:
    ax.add_patch(Rectangle((bbox[0], bbox[1]), (bbox[2] - bbox[0]), (bbox[3] - bbox[1]),
                           lw=1,
                           edgecolor = "red",
                           fill=False))
plt.show()

print("Closing...")
