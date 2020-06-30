import PIL
import imutils.paths
import numpy as np
import skimage.io
import skimage.morphology
import skimage.util

paths = sorted(
    filter(
        lambda p: 'obstacle.png' in p,
        [p for p in imutils.paths.list_images('/home/pablo/iungo_platform/app/apps/static/skins')]
    )
)

for p in paths:
    print(p)

    #
    image = skimage.io.imread(p)

    [rows, columns] = np.where(
        skimage.morphology.convex_hull_image(
            image[:, :, 3]
        )
    )

    row1 = min(rows)
    row2 = max(rows)
    col1 = min(columns)
    col2 = max(columns)

    dr = row2 - row1
    dc = col2 - col1

    if dr > dc:
        n = int((dr - dc) / 2)
        if col1 - n >= 0:
            col1 -= n
        else:
            0

        if col2 + n <= image.shape[1]:
            col2 += n
        else:
            col2 = image.shape[1]

    if dc > dr:
        n = int((dc - dr) / 2)

        if row1 - n >= 0:
            row1 -= n
        else:
            0

        if row2 + n <= image.shape[0]:
            row2 += n
        else:
            row2 = image.shape[0]

    image = PIL.Image.open(p)
    region = image.crop((col1, row1, col2, row2))
    region = region.resize((50, 50))
    region.save(p)
