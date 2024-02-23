import pydicom
import matplotlib.pyplot as plt
import numpy as np

#root@59ce3c027d02:/home/research/preprocessing_test# python3 cut_circle.py
#Center: (255.89996955819126, 256.22024493947936), Radius: 261.86061992836966

# find_circle_center_and_radius関数の定義
def find_circle_center_and_radius(x1, y1, x2, y2, x3, y3):
    # 中点を求める
    mid_x1, mid_y1 = (x1 + x2) / 2, (y1 + y2) / 2
    mid_x2, mid_y2 = (x2 + x3) / 2, (y2 + y3) / 2
    
    # 傾きを求める
    slope1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')
    slope2 = (y3 - y2) / (x3 - x2) if x3 != x2 else float('inf')
    
    # 垂直二等分線の傾き
    perp_slope1 = -1 / slope1 if slope1 != 0 else float('inf')
    perp_slope2 = -1 / slope2 if slope2 != 0 else float('inf')
    
    # 二直線が交わる点（円の中心）を求める
    if perp_slope1 != float('inf') and perp_slope2 != float('inf'):
        A = np.array([[1, -perp_slope1], [1, -perp_slope2]])
        b = np.array([mid_y1 - perp_slope1 * mid_x1, mid_y2 - perp_slope2 * mid_x2])
        center_x, center_y = np.linalg.solve(A, b)
    elif perp_slope1 == float('inf'):
        center_x = mid_x1
        center_y = perp_slope2 * (center_x - mid_x2) + mid_y2
    else:
        center_x = mid_x2
        center_y = perp_slope1 * (center_x - mid_x1) + mid_y1
    
    # 半径を求める
    radius = np.sqrt((x1 - center_x)**2 + (y1 - center_y)**2)
    
    return center_x, center_y, radius

# DICOMファイルの読み込みと表示
dcm_path = '/home/research/preprocessing_test/preCBCT_41/CT.1.2.246.352.63.1.4912167392745633826.5984605804961339052.dcm'  # DICOMファイルへのパスを指定
dcm_data = pydicom.dcmread(dcm_path)
image = dcm_data.pixel_array

plt.imshow(image, cmap='gray')
plt.title('Click on three points on the edge of the circle')

# ユーザーが3点を選択
points = plt.ginput(3)
plt.show()

# 選択された3点の座標
x1, y1 = points[0]
x2, y2 = points[1]
x3, y3 = points[2]

# 円の中心と半径を計算
center_x, center_y, radius = find_circle_center_and_radius(x1, y1, x2, y2, x3, y3)
print(f'Center: ({center_x}, {center_y}), Radius: {radius}')
