# FOV-standardizer

不揃いなFOVを持つCBCT画像とPlanCT画像を深層学習のためにリサイズ、クリッピングおよび円形にマスクして統一する。  
特に画像の四角形からはみ出すように円形をとっていて、楕円等の不完全な円ですらないCT画像を想定  
path.txtに処理したいディレクトリのパス等を記入してコマンドを実行  

実行コマンドは以下： 
```
python3 standardize.py path.txt
```
最後に不要なファイルを確認して削除  
```
python3 single_dicom_viewer.py preCBCT_41_fixed
```
