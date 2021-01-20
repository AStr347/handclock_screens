from PIL import Image, ImageDraw
import re

h = 16
w = 16

c_trans = {0 : 'white', 255 : 'red', 2730 : 'gray', 2735 : 'orange', 3855 : 'green', 4095 : 'black', 15 : 'yellow'}
b_c_trans = {0 : 255, 1 : 0, 2 : 15, 3 : 240, 4 : 170}

def draw_block(x, y, pixels, idraw):
    index = 0
    for i in range(h):
        for j in range(w):
            idraw.point((x+j, y+i), c_trans[pixels[index]])
            index += 1

def b2c(b):
    return b_c_trans[int(b)]

def line2pixels(line : str):
    tmp = []
    bytes = [b2c(s) for s in line[:-1]]
            
    for j in range(0,384,3):
        tmp1 = (((bytes[j]>>4) & 0b1111)<<8) + (((bytes[j]>>0) & 0b1111)<<4) + ((bytes[j+1]>>4) & 0b1111)
        tmp2 = (((bytes[j+1]>>0) & 0b1111)<<8) + (((bytes[j+2]>>4) & 0b1111)<<4) + ((bytes[j+2]>>0) & 0b1111)
        tmp.append(tmp1)
        tmp.append(tmp2)
    return tmp

def prints(pixels:list):
    print(len(pixels),len(pixels[0]),len(pixels)*len(pixels[0]))

    colors = set()
    for i in pixels:
        for j in i:
            colors.add(j)
    print(colors)

def creImg(pixels:list, iindex):
    #we know that final image 240x320 or 240x240
    width , height = 240,320
    img = Image.new('RGBA', (width,height), 'white')
    idraw = ImageDraw.Draw(img)
    # block 48x5
    index = 0
    for y in range(0,height,h):
        for x in range(0,width,w):
            draw_block(x,y,pixels[index], idraw)
            index += 1

    #draw.point((x, y), (sr, sr, sr))
    #img.show()
    img = img.crop((0,0,240,240))
    print('logo240x240_'+ str(iindex) + '.png\n\n')
    img.save('imgs/logo240x240__'+ str(iindex) + '.png')

def img_form_lines(finds, index):
    im,trash = finds
    pixels = []
    lines = re.findall(r"\d{384}\n", im)
    for line in lines:
        if(line[0] != '\n'):
            pixels.append(line2pixels(line))

    prints(pixels)
    creImg(pixels, index)

if(__name__ == "__main__"):
    f = open('D:/proj_svist/putty.log', 'r')
    log = "".join(f.readlines())
    finds = re.findall(r"((\d{384}\n){300}\n\n)", log)
    for a in range(len(finds)):
        img_form_lines(finds[a], a)

       