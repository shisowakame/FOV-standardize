import os, glob
from dicom_utils import dicom2ndarray, sort_dicom_files, save_ndarray_as_dicom
from image_processing import fill_circle_outside, resize_image, clip_image
from cbct_sort import copy_and_rename_dicom_files
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import gridspec

def dicom_viewer(args, skip):
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
        center = (255.9, 256.22)  # 円の中心座標
        radius = 261.86  # 円の半径
        
        #出力用ディレクトリを作成
        output_folder = dcm_folder + "_fixed"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
            
        j = -1
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
