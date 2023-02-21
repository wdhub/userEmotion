import json
import requests
from IPython.display import HTML
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

import configparser

# prepare keys, images and URLs
conf = configparser.ConfigParser()
conf.read("config.ini", encoding="utf-8")
subscription_key = conf['APIs']['faceAPI']
assert subscription_key
face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
image_url = 'https://how-old.net/Images/faces2/main007.jpg'

headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

response = requests.post(face_api_url, params=params, headers=headers, json={"url": image_url})
faces = response.json()
print(json.dumps(faces))
HTML("<font size=5>Detected <font color='blue'>%d</font> faces in the image</font>" % len(faces))

# matplotlib inline
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

plt.figure(figsize=(8, 8))
ax = plt.imshow(image, alpha=0.6)
for face in faces:
    fr = face["faceRectangle"]
    fa = face["faceAttributes"]
    origin = (fr["left"], fr["top"])
    p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
    ax.axes.add_patch(p)
    plt.text(origin[0], origin[1], "%s" % (max(fa["emotion"], key=fa["emotion"].get)), fontsize=30, weight="bold",
             va="bottom")
_ = plt.axis("off")

# https: // blog.csdn.net / weixin_38253705 / article / details / 89517874