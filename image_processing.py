from skimage.transform import resize
from skimage.draw import circle
import numpy as np


# 画像をリサイズ
def resize_image(image, target_pixel_spacing, original_pixel_spacing):
    scale_factors = [o / t for o, t in zip(original_pixel_spacing, target_pixel_spacing)]
    return resize(image, (int(image.shape[0] * scale_factors[0]), int(image.shape[1] * scale_factors[1])), anti_aliasing=True)

# 画像をクリッピング
def clip_image(image, target_rows, target_columns):
    start_row = (image.shape[0] - target_rows) // 2
    start_col = (image.shape[1] - target_columns) // 2
    return image[start_row:start_row + target_rows, start_col:start_col + target_columns]

#　円形に切りとる
def fill_circle_outside(image, center, radius):
    mask = np.zeros(image.shape, dtype=bool)
    rr, cc = circle(center[1], center[0], radius, shape=image.shape)
    mask[rr, cc] = True
    # マスクの外側を黒で塗りつぶす
    image[~mask] = 0
    return image