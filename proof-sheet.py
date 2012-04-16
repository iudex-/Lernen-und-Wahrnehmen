#!/usr/bin/env python

import argparse

#proof-sheet [-h] [-W output-width] [-w maxwidth] [-h maxheight] [-d] [-o output.png] image1.png image2.png image3.png ...


parser = argparse.ArgumentParser(description='Process some images.')
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
print(args.outputwidth)
print(args.maxwidth)
print(args.maxheight)
print(args.display)
print(args.output)
print(args.images)
