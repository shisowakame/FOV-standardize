import os
import shutil
import pydicom
import argparse

def sort_dicom_files(dicom_files):
    """
    DICOMファイルをスライス位置に基づいてソートする。
    """
    dicom_files.sort(key=lambda x: pydicom.dcmread(x, force=True).ImagePositionPatient[2])
    return dicom_files

def copy_and_rename_dicom_files(src_folder):
    """
    指定されたDICOMファイル群をスライス位置に基づいてソートし、
    1.dcm のように番号を付けて同じ階層に新しいディレクトリにコピーする。
    """
    # 目的ディレクトリのパスを生成
    dest_folder = os.path.join(os.path.dirname(src_folder), os.path.basename(src_folder) + "_fixed")
    
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # DICOMファイルのリストを取得
    dicom_files = [os.path.join(src_folder, f) for f in os.listdir(src_folder) if f.endswith('.dcm')]
    sorted_dicom_files = sort_dicom_files(dicom_files)
    
    # ソートされたファイルをコピー
    for i, file_path in enumerate(sorted_dicom_files, start=1):
        with open("file_number.txt", "r") as file:
            number = int(file.read())
        new_file_name = f"p{number}_{i}_out.dcm"
        #new_file_name = f"{i}.dcm"
        new_file_path = os.path.join(dest_folder, new_file_name)
        shutil.copyfile(file_path, new_file_path)
        #print(f"{file_path} を {new_file_path} にコピーしました。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DICOMファイル群をソートしてコピーする')
    parser.add_argument('src_folder', type=str, help='ソースディレクトリのパス')
    args = parser.parse_args()

    copy_and_rename_dicom_files(args.src_folder)
