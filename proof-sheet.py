#!/usr/bin/env python

# Nils Richter <n_richter10@cs.uni-kl.de>

# note:
# can not handle non-rgb images, alpha channel is removed
# displaying an image with "scipy.misc.imshow(result)" does not work for me

import argparse
import scipy
import scipy.ndimage
import math
from numpy import  zeros

#proof-sheet [-h] [-W output-width] [-w maxwidth] [-h maxheight] [-d] [-o output.png] image1.png image2.png image3.png ...

parser = argparse.ArgumentParser(description='Creates a proofsheet with the thumbnail of the input images')
parser.add_argument('images', metavar='image.png', nargs='+',
                   help='image to process')
parser.add_argument('-W', dest='outputwidth', type=int, default=1200,
                   help='output width (default: 1200 px)')
parser.add_argument('-w', dest='maxwidth', type=int, default=200,
                   help='maximum width of a thumbnail')
parser.add_argument('-g', dest='maxheight', type=int, default=200,
                   help='maximum height of a thumbnail')
parser.add_argument('-d', dest='display', action='store_const',
                   const=True, default=False, help='display image')
parser.add_argument('-o', dest='output', default="output.png",
                   help='file to output')

args = parser.parse_args()

# catch an error
if args.outputwidth < args.maxwidth:
    print "The maximum width of the proofsheet is lower than the maximum width of an image."
    print "Proofsheet width set to:", args.maxwidth
    args.outputwidth = args.maxwidth


def center( ima ): # center an image in the maximum space for a thumbnail
    res = zeros([args.maxheight,args.maxwidth,3])
    y = int(args.maxheight/float(2) - len(ima)/float(2))
    x = int(args.maxwidth/float(2) - len(ima[0])/float(2))
    res[  y:y+len(ima) , x:x+len(ima[0]) , : ] = ima
    return res

# compute size of result image
col = args.outputwidth / float(args.maxwidth)
if col>len(args.images): col = len(args.images)
row = int( math.ceil( len(args.images)/col ))
col = int(col)
w = col*args.maxwidth
h = row*args.maxheight

result = zeros([h,w,3])

#process each image
for i in range( len(args.images)):
    print 'processing', args.images[i]+'...'
    im = scipy.misc.imread(args.images[i])
    im = im[0:len(im),0:len(im[0]), 0:3 ] # remove alpha channel

    # resize factors
    fy = float(args.maxheight-2)/len(im)
    fx = float(args.maxwidth-2)/len(im[0])
    
    if fx<1 or fy<1:
        if fy>fx: fac = fx #use smalles factor
        else: fac = fy
    else: fac = 1 #dont resize fitting images

    #compute possition in result image
    iy = int(i%col)
    ix = int( math.floor(i/col) )
    py0 = iy*args.maxwidth
    py1 = (iy+1)*args.maxwidth
    px0 = ix*args.maxheight
    px1 = (ix+1)*args.maxheight
    
    result[ px0:px1 , py0:py1 , : ] = center( scipy.ndimage.interpolation.zoom(im, [fac, fac, 1]) )

print "Done!"

if args.display:
    scipy.misc.imshow(result)
else:
    scipy.misc.imsave(args.output,result)

