# FOV-standardizer

不揃いなFOVを持つCBCT画像とPlanCT画像を深層学習のためにリサイズ、クリッピングおよび円形にマスクして統一する。  
特に画像の四角形からはみ出すように円形をとっていて、楕円等の不完全な円ですらないCT画像を想定

実行コマンドは以下： 
```
python3 get_circle.py
python3 standardize.py PlanCT_DirName CBCT_DirName
```
