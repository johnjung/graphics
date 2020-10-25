#!/usr/bin/env python
"""Usage: update_thumbnails.py --orig-dir <orig-dir> --web-photoalbum-dir <web-photoalbum-dir>
"""

import os
import shutil
import sys
from docopt import docopt
from PIL import Image, ExifTags

# <orig-dir> should contain a sequence of subdirectories like aluminum,
# commercial, residential, etc. Each of those subdirectories should contain
# JPEG images.

# <web-photoalbum-dir> is a directory in the website where thumbnails and
# fullsized images will be stored.  for each directory in <orig-dir>, create a
# directory in <web-photoalbum-dir>. Each of those subdirectories should
# contain two directories, THUMBS, and FULLSIZE. Those directories will be
# populated with images that fit into a 975x500 box, and that are 48px square.

THUMBS = 'thumbnails'
FULLSIZE = 'fullsize'

if __name__=='__main__':
    arguments = docopt(__doc__)
 
    # loop over directories (e.g. 'commercial')
    for d in os.listdir(arguments['<orig-dir>']):
        if not os.path.isdir('{}/{}'.format(arguments['<orig-dir>'], d)):
            continue

        sys.stdout.write('PROCESSING {}\n'.format(d))

        # delete temporary directory, if it exists.
        if os.path.isdir('/tmp/{}'.format(d)):
            shutil.rmtree('/tmp/{}'.format(d))

        # move website directory (e.g. 'commercial') to /tmp.
        if os.path.isdir('{}/{}'.format(arguments['<web-photoalbum-dir>'], d)):
            shutil.move(
                '{}/{}'.format(arguments['<web-photoalbum-dir>'], d),
                '/tmp'
            )

        # make directories for thumbnails and full-sized images. 
        os.makedirs('{}/{}/{}'.format(arguments['<web-photoalbum-dir>'], d, THUMBS))
        os.makedirs('{}/{}/{}'.format(arguments['<web-photoalbum-dir>'], d, FULLSIZE))

        # loop over images.
        for f in os.listdir('{}/{}'.format(arguments['<orig-dir>'], d)):
            sys.stdout.write('processing {}\n'.format(f))

            # be sure file is jpeg. 
            if not os.path.splitext(f)[1] in ('.jpg', '.png'):
                continue

            # save thumbnails.
            img = Image.open('{}/{}/{}'.format(arguments['<orig-dir>'], d, f))
            exif = img._getexif()
            try:
                if exif[274] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[274] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[274] == 8:
                    img = img.rotate(90, expand=True)
            except (KeyError, TypeError):
                pass

            crop_size = min(img.size)
            img = img.crop(((img.size[0] - crop_size) // 2,
                      (img.size[1] - crop_size) // 2,
                      (img.size[0] + crop_size) // 2,
                      (img.size[1] + crop_size) // 2))
            img = img.resize((72, 72), Image.ANTIALIAS)
            img.save('{}/{}/{}/{}.jpg'.format(arguments['<web-photoalbum-dir>'], d, THUMBS, os.path.splitext(f)[0]), 'JPEG')

            # save fullsized image.
            img = Image.open('{}/{}/{}'.format(arguments['<orig-dir>'], d, f))
            exif = img._getexif()
            try:
                if exif[274] == 3:
                    img = img.rotate(180, expand=True)
                elif exif[274] == 6:
                    img = img.rotate(270, expand=True)
                elif exif[274] == 8:
                    img = img.rotate(90, expand=True)
            except (KeyError, TypeError):
                pass

            # get scaling factor so x is no greater than 975 and y is no
            # greater than 500.
            s = min((975.0 / img.size[0], 500.0 / img.size[1]))
            img = img.resize((int(img.size[0] * s), int(img.size[1] * s)), Image.ANTIALIAS)
            
            img.save('{}/{}/{}/{}.jpg'.format(arguments['<web-photoalbum-dir>'], d, FULLSIZE, os.path.splitext(f)[0]), 'JPEG')
