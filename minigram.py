#!/usr/bin/env python

# Nils Richter <n_richter10@cs.uni-kl.de>

import argparse
from pylab import *
import scipy
import scipy.ndimage
import math
import random
import PIL.Image

#minigram [-f filter-name] [-o output.png] [other filter parameters] image.png

parser = argparse.ArgumentParser(description='Apply some filters')
parser.add_argument('parameters', metavar='... image.png', nargs='+',
                   help='image to process')
parser.add_argument('-f', dest='filter', default='posterize',
                   help="""highlight: r g b imgage.png
filmgrain: probability image.png
fisheye:   image.png
posterize: image.png""")

parser.add_argument('-o', dest='output', default="output.png",
                   help='file to output')
args = parser.parse_args()

out = True

def limit (input, min=0, max=255):
    l = not isinstance(input, list)
    if l: input = [input]        
    for i,d in enumerate(input):
        if d<min: input[i] = min
        elif d>max: input[i] = max
    if l: input = input[0]
    return input
    
def grain (rgb,probability=30,effect=20):
    #print rgb,probability,effect
    rgb = map(int, rgb)
    rgb = [ int( sum( rgb )/3.0 ) ]*3 # avg 3-tupel
    rand = random.randrange(0,100)
    if   rand>100-probability/2: rgb = limit( map(lambda x:x-effect,rgb) )
    elif rand>100-probability:   rgb = limit( map(lambda x:x+effect,rgb) )
    rgb = limit( [ int(rgb[0]*1.08), int(rgb[1]*1), int(rgb[2]*0.78) ] ) # sepia
    return rgb

def highlight (rgb,inputrgb,delta):
    r,g,b = rgb
    ir,ig,ib = inputrgb
    if not ( abs(ir-r)<delta and abs(ig-g)<delta and abs(ib-b)<delta ):
        return [ int( math.trunc( sum(rgb)/3.0 ) ) ]*3
    return rgb

if args.filter=='posterize':
    result = floor( 4*imread(args.parameters[0]) )/4.0   # reads floats where 0<=value<=1
    #result =  array(im*255, dtype='uint8')

elif args.filter=='filmgrain':
    im = scipy.misc.imread(args.parameters[1])[:,:,0:3]
    result =  map(lambda x: map(lambda y: grain(y,50,20),x),im)

elif args.filter=='highlight':
    print args
    im = scipy.misc.imread(args.parameters[4])[:,:,0:3]
    inputrgb = map(int, args.parameters[0:3])
    delta = int(args.parameters[3])
    result = map(lambda y: map(lambda x:highlight(x,inputrgb,delta),y) , im)

# fisheye klappt leider nicht
# die Einteilung in Bloecke ist da, der Rest fehlt
# die Idee war den Abstand zum Mittelpunkt zu berechnen und die Bloecke
# mit einem daraus abgeleiteten Faktor zu vergroessern, aber keine Zeit mehr...
elif args.filter=='fisheye':
    im = PIL.Image.open(args.parameters[0])
    blocks = 10
    w,h = im.size
    mx = int(w/2.0)
    my = int(h/2.0)
    blockw = int(w/blocks)
    blockh = int(h/blocks)
    
    data = []
    for x in range(blocks):
        for y in range(blocks):
            data.append( (
                            (x*blockw,y*blockh,(x+1)*blockw-2,(y+1)*blockh-2), # out
                            (
                               x*blockw , y*blockh, # in
                               x*blockw , (y+1)*blockh,
                               (x+1)*blockw, (y+1)*blockh,
                               (x+1)*blockw , y*blockh
                            )
                         ) )
    im.transform(im.size, PIL.Image.MESH, data).save(args.output)
    out = False
else: 
    print "no known filter"
    out = False

if out:
    scipy.misc.imsave(args.output, result);
