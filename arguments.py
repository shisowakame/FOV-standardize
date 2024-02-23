import argparse
import os

# コマンドライン引数を解析して、DICOMビューアの設定を取得する
def dicom_viewer_arguments(args_list=None):    
    parser = argparse.ArgumentParser()
    parser.add_argument('img_folders', type=str, nargs=2, help='dcmファイルがまとめられているフォルダを2つ入力')
    parser.add_argument('--image_type', '-it', type=str, default='dcm', help='対象とする画像の拡張子を指定')
    args = parser.parse_args(args_list)
    # ファイル数の商
    folder1_count = get_directory_file_count(args.img_folders[0])
    folder2_count = get_directory_file_count(args.img_folders[1])
    skip = folder1_count // folder2_count
    return args, skip

# 指定ディレクトリ内のファイル数を取得
def get_directory_file_count(directory):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
