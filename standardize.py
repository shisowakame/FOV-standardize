import subprocess

def read_paths(file_path):
    paths = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            # コメント行または空行を無視
            if not stripped_line or stripped_line.startswith('#'):
                continue
            paths.append(stripped_line)
    return paths


#def main():
"""
paths = read_paths(paths_file)
main_path = paths[0]
main_circle_path = paths[1]
PlanCT_dir = paths[2]
CBCT_dir = paths[3]
CBCT_sort = paths[4]
"""
print("")
print("---------------------------------------------------------------")
print("defaultの円の半径は261.86 、円の中心は(255.9, 256.22)です:")
print("")
print("1) 半径と円の中心を測りなおす")
print("2) defaultの半径と円の中心を使う")
print("")
choice = input()
for number in range(15, 17):
    
    
    main_path = '/home/research/preprocessing_test/main.py'
    main_circle_path = '/home/research/preprocessing_test/main-circle.py'
    PlanCT_dir = f'/home/research/data/HirosakiUniv-small/trainB/RT-CT_{number}'
    CBCT_dir = f'/home/research/data/HirosakiUniv-small/trainA/preCBCT_{number}'
    CBCT_sort = '/home/research/preprocessing_test/cbct_sort.py'

    

    if choice == '1':

        subprocess.run(['python3', main_circle_path, PlanCT_dir, CBCT_dir])

    elif choice == '2':
        subprocess.run(['python3', main_path, PlanCT_dir, CBCT_dir])

    else:
        print("無効な選択です。")

    subprocess.run(['python3', CBCT_sort, CBCT_dir])

"""
print("")
print("---------------------------------------------------------------")
print("出力結果に不要なスライドは含まれていましたか？：")
print("")
print("1) はい")
print("2) いいえ")
print("")
choice2 = input()
#if choice2 == '1':

#elif choice2 == '2':
"""

"""
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("使用法: python3 main.py paths.txt")
    else:
        main(sys.argv[1])
"""
