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

    # All images have 4 channels. Each pixel in channel 4 is either 225 or 0, so
    # the background is basically the ground-truth or mask for the image.
    image = skimage.io.imread(p)

    # So we extract the best polygon that encircles the image from channel 4.
    [rows, columns] = np.where(
        skimage.morphology.convex_hull_image(
            image[:, :, 3]
        )
    )

    # Now we calculate the rectangular area that encircles that polygon.
    row1 = min(rows)
    row2 = max(rows)
    col1 = min(columns)
    col2 = max(columns)

    # But we want to crop an square...
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

    # Now we load the original image. Images are indexed PNGs and we want to
    # keep the color palette unmodified.
    image = PIL.Image.open(p)

    # Crop the square we previously calculate.
    region = image.crop((col1, row1, col2, row2))

    # Resize to desired fixed dimensions.
    region = region.resize((50, 50))

    # And save the resized image.
    region.save(p)
