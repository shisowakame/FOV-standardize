import os, glob
from arguments import dicom_viewer_arguments
from dicom_utils import dicom2ndarray, sort_dicom_files, save_ndarray_as_dicom
from image_processing import fill_circle_outside, resize_image, clip_image
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import gridspec
import pydicom
import numpy as np

#python3 main-circle.py RT-CT_41 preCBCT_41

def find_circle_center_and_radius():
    dcm_path = '/home/research/preprocessing_test/preCBCT_41/CT.1.2.246.352.63.1.4912167392745633826.5984605804961339052.dcm'  # DICOMファイルへのパスを指定
    dcm_data = pydicom.dcmread(dcm_path)
    image = dcm_data.pixel_array

    plt.imshow(image, cmap='gray')
    plt.title('Click on three points on the edge of the circle')

    # ユーザーが3点を選択
    points = plt.ginput(3)
    plt.close()

    # 選択された3点の座標
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]

    # 円の中心と半径を計算
    #center_x, center_y, radius = find_circle_center_and_radius(x1, y1, x2, y2, x3, y3)
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
    print(f'Center: ({center_x}, {center_y}), Radius: {radius}')
    return center_x, center_y, radius


def dicom_viewer(args, skip, center_x, center_y, radius):
    # DICOM画像をビューアで表示
    file_num_list = []
    dcm_path_list = []
    all_images = []

    # 2つのディレクトリのパスを取得
    planct_dir = [d for d in args.img_folders if 'CBCT' not in d][0]
    cbct_dir = [d for d in args.img_folders if 'CBCT' in d][0]

    # CBCTのPixel Spacingを取得
    cbct_file = glob.glob(os.path.join(cbct_dir, f'*.{args.image_type}'))[0]
    cbct_img, cbct_ref = dicom2ndarray(cbct_file)
    cbct_pixel_spacing = cbct_ref.PixelSpacing
    cbct_rows, cbct_columns = cbct_ref.Rows, cbct_ref.Columns

    file_num_list = []
    dcm_path_list = []
    for dcm_folder in args.img_folders:
        if not os.path.isdir(dcm_folder):
            print(f"引数にディレクトリではないものがある: {dcm_folder}")
            return

        dicom_files = glob.glob(os.path.join(dcm_folder, f'*.{args.image_type}'))
        sorted_files = sort_dicom_files(dicom_files)
        dcm_path_list.append(sorted_files)
        file_num_list.append(len(sorted_files))

        images = []
        center = (center_x, center_y)  # 円の中心座標
        #radius = 261.86  # 円の半径
        
        #出力用ディレクトリを作成
        output_folder = dcm_folder + "_fixed"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)

        j = 0
        k = 0
        
        for i, dcm_file in enumerate(sorted_files):

            """cbctのソートを作る用
            if dcm_folder == cbct_dir:
                k = k + 1
                save_ndarray_as_dicom(cbct_img, cbct_ref, k, output_folder)
            """
            

            if dcm_folder == planct_dir and i % skip != 0:
                continue  # どちらかのCT画像が大幅に多い場合、数枚おきにスキップしてスライス箇所を合わせる

            img, ref = dicom2ndarray(dcm_file)
            #filename = str(i+1)
            if img is not None:
                if dcm_folder == planct_dir:
                    j = j + 1 #ファイル名
                    # PlanCTの画像をリサイズ、クリップ、円形に切り抜き
                    img = resize_image(img, cbct_pixel_spacing, ref.PixelSpacing)
                    img = clip_image(img, cbct_rows, cbct_columns)
                    img = fill_circle_outside(img, center, radius)

                    save_ndarray_as_dicom(img, ref, j, output_folder)
                
                images.append(img)
        all_images.append(images)
        file_num_list.append(len(images))

    # 画像ビューアの設定
    min_file_num = min(file_num_list)
    init_slice = min_file_num // 2  # 初期スライスを中間に設定

    fig = plt.figure()
    dir_num = len(args.img_folders)
    gs = gridspec.GridSpec(2, dir_num, height_ratios=[20, 1])
    axes = []
    image_tables = []

    for i, images in enumerate(all_images):
        ax = fig.add_subplot(gs[0, i])
        ax.axis('off')
        axes.append(ax)
        image_table = ax.imshow(images[init_slice], cmap='gray')
        image_tables.append(image_table)

    # スライダーの設定
    ax_slider = fig.add_subplot(gs[1, :])
    slice_slider = Slider(ax=ax_slider, label="Slice", valmin=0, valmax=min_file_num-1, valinit=init_slice, valfmt='%0.0f')

    def update(val):
        slice_idx = int(slice_slider.val)
        for i, image_table in enumerate(image_tables):
            image_table.set_data(all_images[i][slice_idx])
            axes[i].draw_artist(image_table)
        fig.canvas.draw_idle()

    slice_slider.on_changed(update)

    plt.title('results of the process\n\n( close this window after you have confirmed the process. )', y=1)
    plt.show()

if __name__ == '__main__':
    center_x, center_y, radius = find_circle_center_and_radius()

    args, skip = dicom_viewer_arguments()
    dicom_viewer(args, skip, center_x, center_y, radius)
