# -*- coding: utf-8 -*-

from PIL import Image,ImageDraw,ImageFont
import matplotlib.pyplot as plt
import random
import os
import cairocffi as cairo
import editdistance
import numpy as np
from scipy import ndimage
from sys import getdefaultencoding
import sys
import random
import matplotlib.pyplot as plt
from keras.preprocessing import image

d = getdefaultencoding()
if d != "utf-8":
    reload(sys)
    sys.setdefaultencoding("utf-8")


def speckle(img):
    severity = np.random.uniform(0, 0.0)
    blur = ndimage.gaussian_filter(np.random.randn(*img.shape) * severity, 1)
    img_speck = (img + blur)
    img_speck[img_speck > 1] = 1
    img_speck[img_speck <= 0] = 0
    return img_speck


# paints the string in a random location the bounding box
# also uses a random font, a slight random rotation,
# and a random amount of speckle noise
def imsave(fname, arr, vmin=None, vmax=None, cmap='gray', format=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure

    fig = Figure(figsize=arr.shape[::-1], dpi=1, frameon=False)
    canvas = FigureCanvas(fig)
    fig.figimage(arr, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin)
    fig.savefig(fname, dpi=1, format=format)

def paint_text(text, w, h,  rotate=False, ud=True, multi_fonts=False):
    newtext = ""
    import random
    banglachars = "অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়ঃৎং"
    # text = "নড়চড়"
    chars = []
    for i in range(0,len(banglachars),3):
        chars.append(banglachars[i:i+3])
    for i in range(0,len(text),3):
        ch=text[i:i+3]
        itsoke= 1
        for j in chars:
            if j==ch:
                itsoke = 0

    # text="অ"
    w=random.randint(300,1900)
    h=random.randint(40,200)
    LargeWidth=0

    if(w>1000):
        LargeWidth=1
        if(h<100):
            h=random.randint(100,200)

    fontsize = random.randint(30, 40)

    if(LargeWidth==1):
        fontsize = random.randint(40,55)

    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h)
    import random

    FlagBlack = random.randint(0, 4)
    # FlagBlack = 1
    with cairo.Context(surface) as context:
        if (FlagBlack == 2):
            context.set_source_rgb(0, 0, 0)  # White
        else:
            context.set_source_rgb(1, 1, 1)  # White

        context.paint()
        # this font list works in CentOS 7
        multi_fonts=True

        if multi_fonts:
            fonts = ['Solaimanlipi','Bangla','AponaLohit','Nikosh', 'Siyamrupali', 'kalpurush','AdorshoLipi','Likhan','Lohit Bengali','SutonnyBanglaOMJ','Sagar','Rupali','Mukti']
            context.select_font_face(np.random.choice(fonts), cairo.FONT_SLANT_NORMAL,
                                     np.random.choice([cairo.FONT_WEIGHT_BOLD, cairo.FONT_WEIGHT_NORMAL]))
        else:
           context.select_font_face('Mukti' , cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        import random

        context.set_font_size(fontsize)
        box = context.text_extents(text)
        border_w_h = (4, 4)
        if box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):

            Flag = 0
            while box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
                fontsize -= 1
                if (fontsize == 0):
                    Flag = -1
                    break
                # print(fontsize)
                context.set_font_size(fontsize)
                box = context.text_extents(text)
            if Flag == -1:
                fontsize = 20
                text = "ক"
                context.set_font_size(fontsize)
                box = context.text_extents(text)

            # while box[2] > (w - 2 * border_w_h[1]) or box[3] > (h - 2 * border_w_h[0]):
            #     idx=len(text)-1
            #     for i in range(len(text)-1,0,-1):
            #         # print(text[i])
            #         if text[i]==" ":
            #             idx=i
            #             break
            #     text=text[0:idx]
            #     box = context.text_extents(text)
            # # print(text)
            # text1="মঠ"
            # text2="যগ"
            # text3="যগ"
            # Fl=random.randint(0,3)
            # if(Fl==0):
            #     box = context.text_extents(text1)
            # elif(Fl==1):
            #     box = context.text_extents(text2)
            # else:
            #     box = context.text_extents(text3)


            # raise IOError('Could not fit string into image. Max char count is too large for given image width.')

        # teach the RNN translational invariance by
        # fitting text box randomly on canvas, with some room to rotate


        max_shift_x = w - box[2]
        max_shift_y = h - box[3] - border_w_h[1]
        top_left_x = np.random.randint(0, int(max_shift_x))
        if ud:
            rando= np.random.randint(0, int(max_shift_y))

            top_left_y =  rando
        else:
            if fontsize>40:
                top_left_y = h // 6
            elif fontsize>35:
                top_left_y = h // 4
            elif fontsize>30:
                top_left_y = h // 3
            else:
                top_left_y = h // 2


        context.move_to(top_left_x - int(box[0]), top_left_y - int(box[1]))
        if (FlagBlack == 2):
            context.set_source_rgb(1, 1, 1)
        else:
            context.set_source_rgb(0, 0, 0)

        # print(text)
        context.show_text(text)

    buf = surface.get_data()
    a = np.frombuffer(buf, np.uint8)
    a.shape = (h, w, 4)
    a = a[:, :, 0]  # grab single channel
    import cv2
    vis2 = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
    vis2 = cv2.resize(vis2, (564, 64))
    a=np.asarray(vis2)
    a = a[:, :, 0]  # grab single channel

    # imsave('file_'+str(random.randint(0,1999))+'.png',a)
    # plt.imshow(a,cmap='gray')
    # plt.show()

    # a = speckle(a)

    a = a.astype(np.float32) / 255

    a = np.expand_dims(a, 0)
    if rotate:
        a = image.random_rotation(a, 3 * (w - top_left_x) / w + 1)
    a = speckle(a)


    return a

# paint_text("আগামীকাল ঢাকা ফাকা হবার কথা",1,1)
# ঢাকা এদেশের রাজধানী