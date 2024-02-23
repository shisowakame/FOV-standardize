import pydicom as dicom
import numpy as np
import os
from pydicom.dataset import Dataset

def dicom2ndarray(dicom_file):
    # DICOMファイルを読み込み、NumPy配列に変換する
    try:
        ref = dicom.read_file(dicom_file, force=True)
        img = ref.pixel_array
        return img, ref
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return None, None

def sort_dicom_files(dicom_files): #DICOMファイルをスライス位置に基づいてソートする。
    dicom_files.sort(key=lambda x: dicom.read_file(x, force=True).ImagePositionPatient[2])
    return dicom_files

def save_ndarray_as_dicom(img, ref, j, output_folder):
    img_processed = img

    # 新しいDatasetオブジェクトを作成
    ds = Dataset()

    # 処理後の画像データをDICOMファイルとして保存
    img_processed = (img_processed * 65535).astype(np.uint16)  # 画像データの正規化と型変換
                    
    ds.file_meta = ref.file_meta  # メタデータのコピー
    ds.update(ref)  # その他の必要なDICOM属性のコピー
    ds.Rows, ds.Columns = img_processed.shape
                    
    ds.PixelData = img_processed.tobytes()

    # ファイルパスの生成を修正
    filename = f"{j}_out.dcm"  # ファイル名のフォーマットを修正
    path = os.path.join(output_folder, filename)
    #ds.save_as(path, write_like_original=False)
    dicom.dcmwrite(path, ds)