#!/bin/bash

# NOTE: I'm pretty sure these three `convert` commands can be combined into one, leading to considerably better performance.

# Input file is wave.png.
#convert wave.png -gravity North -extent 100%x111% tmp1.png
convert wave.png -gravity North -extent 100%x105% tmp1.png

convert tmp1.png logo-lab-larger.png -gravity southeast -geometry +0+0 -composite tmp2.png

convert tmp2.png website.png -gravity southwest -geometry +0+0 -composite tmp3.png

lpr -P Canon_SELPHY_CP1300 -o fit-to-page tmp3.png
#lpr -o fit-to-page tmp3.png
