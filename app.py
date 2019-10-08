from PIL import Image, ImageDraw, ImageFont
import sys
import requests
from io import  BytesIO


# Add poster to image
def poster(org, post, img):

    # org = Image.open(inimage)
    # post = Image.open(pimage)

    # resize logo
    wsize = int(min(org.size[0], org.size[1]) * 0.25)
    wpercent = (wsize / float(post.size[0]))
    hsize = int((float(post.size[1]) * float(wpercent)))

    mod = post.resize((wsize, hsize))
    mbox = org.getbbox()
    sbox = mod.getbbox()

    # right bottom corner
    box = (mbox[2] - sbox[2], mbox[3] - sbox[3])
    org.paste(mod, box)
    return org



# Argument vars
title = ''
query = ''
# Get the title from the user
for i,text in enumerate(sys.argv):
    print(i)
    try:
        if i is not 0 and sys.argv[i+1] is not None:
            title = title + sys.argv[i] + " "
            query = query + sys.argv[i] + "%20"
    except IndexError:
        title = title + sys.argv[i] + " "
        query = query + sys.argv[i]
data = requests.get("http://www.omdbapi.com/?t="+query+"&apikey=f5133c86")
if data.status_code == 200:
    print('Success!')
elif data.status_code == 404:
    print('Not Found.')


res = (600,1080)
img = Image.new('RGB', res, color = (255,255,255))

print('Query : '+query)
data = data.json()
print(data)
print(data['Title'])
d = ImageDraw.Draw(img)
d.text((10,10), ("Title : "+title), fill=(255, 255, 0))


post_resp = requests.get(data['Poster'])
post_image = Image.open(BytesIO(post_resp.content))




img = poster(img,post_image,img)
post_image.save('poster.png')

img.save('hw.png')
