import os
import glob
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import gridspec
import pydicom as dicom
import argparse
import numpy as np

def single_dicom_viewer_arguments(args_list=None):
    """
    コマンドライン引数を解析して、DICOMビューアの設定を取得する。
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('img_folders', type=str, nargs='*', help='dcmファイルがまとめられているフォルダを入力')
    parser.add_argument('--image_type', '-it', type=str, default='dcm', help='対象とする画像の拡張子を指定')
    args = parser.parse_args(args_list)
    return args

def dicom2ndarray(dicom_file):
    """
    DICOMファイルを読み込み、NumPy配列に変換する。
    """
    try:
        ref = dicom.read_file(dicom_file, force=True)
        img = ref.pixel_array
        return img
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return None

def sort_dicom_files(dicom_files):
    """
    DICOMファイルをスライス位置に基づいてソートする。
    """
    dicom_files.sort(key=lambda x: dicom.read_file(x, force=True).ImagePositionPatient[2])
    return dicom_files

def single_dicom_viewer(args):
    """
    DICOM画像をビューアで表示する。
    """
    if args.image_type == 'dcm':
        img2ndarray = dicom2ndarray
    else:
        print("サポートされていない画像タイプです。")
        return

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

    min_file_num = min(file_num_list)
    init_slice = min_file_num // 2  # 初期スライスを中間に設定
    all_images = []

    for dcm_paths in dcm_path_list:
        images = [img2ndarray(dcm_path) for dcm_path in dcm_paths[:min_file_num] if img2ndarray(dcm_path) is not None]
        all_images.append(images)

    all_images = np.array(all_images)

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

    ax_slicer = fig.add_subplot(gs[1, :])
    slice_slicer = Slider(ax=ax_slicer, label="position", valinit=init_slice, valmin=0, valmax=min_file_num - 1, valfmt='%d', orientation='horizontal')

    def update(val):
        for images, image_table in zip(all_images, image_tables):
            image_table.set_data(images[int(slice_slicer.val)])
        fig.canvas.draw_idle()

    slice_slicer.on_changed(update)
    plt.show()

if __name__ == '__main__':
    single_dicom_viewer_args = single_dicom_viewer_arguments()
    single_dicom_viewer(single_dicom_viewer_args)
