*************WARNING****************

First print one time manually, and adjust parameters: scale, fit, etc. Afterwards, the shell schript will work.

If you don't do this, the printer will print empty pages.

# Photo size
4 x 6 inch (100 x 148 mm)

# Install imagemagick on a Mac
brew update && brew install imagemagick

# With bash script

NOTE: Another approach is to create a page (convert -page 4x6) first and then center a plot on it and put the logo and the website.

The script is print.sh. It takes two arguments: input file and output file that is printed. The files can be in any raster image type. We use png here.

Use imagemagick for image manipulation. Cannot do vector operations, only raster operations. PDFs are rasterized.

The printer supplies its own margins.

## See if printer is recognized and get its name

WARNING: Even if the printer is not listed here lpr might still work.

lpstat -p -d

## Add logo to bottom right corner of file.
Use the larger file, which is scaled by a factor 1.5.
Don't move relative by border (0px) as the printer has its own margins.

convert praat.png logo-lab.png -gravity southeast -geometry +0+0 -composite output.png

## Print file to printer. Fit to page.

IMPORTANT: If lpr says "lpr: No such file or directory", it means
that the printer is not found in the network.

lpr -P Canon_SELPHY_CP1300 -o fit-to-page output.png

# Possible useful commands

* Resize something to something.

convert in.pdf -resize 595x595 out.png

* Rescale something

convert logo-lab.png -scale 200% logo-lab-larger.png
