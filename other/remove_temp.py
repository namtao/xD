import os
import re
import shutil
from pathlib import Path


# xóa file rác và thư mục trống
def remove_temp(path):
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if (len(dir) > 10 or ('Temp' in dir)):
                print(os.path.join(root, dir))
                shutil.rmtree(os.path.join(root, dir))

    for root, dirs, files in os.walk(path):
        for file in files:
            if (('_' in file) or os.path.getsize(os.path.join(root, file)) == 0 or ('jpg' in file)):
                print(os.path.join(root, file))
                os.remove(os.path.join(root, file))

    def removeEmptyFolders(path, removeRoot=True):
        if not os.path.isdir(path):
            return

        # remove empty subfolders
        files = os.listdir(path)
        if len(files):
            for f in files:
                fullpath = os.path.join(path, f)
                if os.path.isdir(fullpath):
                    removeEmptyFolders(fullpath)

        # if folder empty, delete it
        files = os.listdir(path)
        if len(files) == 0 and removeRoot:
            print("Removing empty folder:", path)
            os.rmdir(path)

    removeEmptyFolders(path)


# kiểm tra file chưa nén và file nén xem đã đầy đủ chưa
def copy_nen(dir1, dir2, pathTarget):
    def get_files(folderPath, fileFormat):
        lst = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                pattern = re.compile(".*"+fileFormat+"$")

                if pattern.match(file):
                    # lst.append(os.path.join(root, file))
                    lst.append(os.path.join(file))
                    # lst.append(os.path.splitext(file)[0])
        return lst

    lstPdf1 = get_files(dir1, 'pdf')
    lstPdf2 = get_files(dir2, 'pdf')
    # lstPdf3 = get_files(dir3, 'pdf')

    # lstDuplicate = list(set(lstPdf1) & set(lstPdf2))
    lstNotDuplicate = list(set(lstPdf1) - set(lstPdf2))

    # print(len(lstDuplicate))

    # count = 0
    for root, dirs, files in os.walk(dir1):
        for file in files:
            if (file in lstNotDuplicate):
                print(os.path.join(root, file))
                shutil.copy(os.path.join(root, file),
                            os.path.join(pathTarget, file))


def remove_nen(dir1, dir2):
    def get_files(folderPath, fileFormat):
        lst = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                pattern = re.compile(".*"+fileFormat+"$")

                if pattern.match(file):
                    # lst.append(os.path.join(root, file))
                    lst.append(os.path.join(file))
                    # lst.append(os.path.splitext(file)[0])
        return lst

    # dir3 = r'E:\Chua nen'

    lstPdf1 = get_files(dir1, 'pdf')
    lstPdf2 = get_files(dir2, 'pdf')
    # lstPdf3 = get_files(dir3, 'pdf')

    lstDuplicate = list(set(lstPdf1) & set(lstPdf2))
    # lstNotDuplicate = list(set(lstPdf1) - set(lstPdf2) - set(lstPdf3))

    # print(len(lstDuplicate))

    for root, dirs, files in os.walk(dir1):
        for file in files:
            if (file in lstDuplicate):
                print(os.path.join(root, file))
                os.remove(os.path.join(root, file))


def create_struct(pathRoot, pathTarget):
    count = 0
    for root, dirs, files in os.walk(pathRoot):
        for fileName in files:
            try:
                head, tail = (os.path.split(
                    Path(os.path.join(root, fileName))))
                if (len(tail.split('.')) > 6):
                    newPath = os.path.join(pathTarget, tail.split('.')[0], tail.split('.')[
                                           1], tail.split('.')[2], tail.split('.')[3])
                    Path(newPath).mkdir(parents=True, exist_ok=True)
                    # os.path.splitext(tail)[0]
                    # os.path.splitext(tail)[1]
                    if not os.path.exists(os.path.join(newPath, tail.replace(' ', ''))):
                        shutil.move(os.path.join(root, fileName), os.path.join(
                            newPath, tail.replace(' ', '')))
                        count += 1
                    else:
                        pass
                        # print(os.path.join(root, fileName))
                        # with open('error.txt', 'a', encoding='utf8') as f:
                        # print(os.path.join(root, fileName))
                        # f.write(os.path.join(root, fileName) + '\n')
            except:
                # with open('error.txt', 'a', encoding='utf8') as f:
                # print(os.path.join(root, fileName))
                # f.write(os.path.join(root, fileName) + '\n')
                pass
    print(count)


# xóa temp
remove_temp(r'E:\OCR NEN\CHUA NEN')

# copy nén vị thanh
copy_nen(r'D:\HoTich\HOTICH_HG\source - haugiang\Files',
         r'D:\HoTich\HOTICH_HG\source - haugiang\FilesNen', r'E:\OCR NEN\CHUA NEN\VI THANH')

# copy nén vị thủy
copy_nen(r'D:\HoTich\HOTICH_HG\source - vithuy\Files',
         r'D:\HoTich\HOTICH_HG\source - vithuy\FilesNen', r'E:\OCR NEN\CHUA NEN\VI THUY')

# copy nén long mỹ
copy_nen(r'D:\HoTich\HOTICH_HG\soucre - hlongmy\Files',
         r'D:\HoTich\HOTICH_HG\soucre - hlongmy\FilesNen', r'E:\OCR NEN\CHUA NEN\LONG MY')

# xóa file đã nén
remove_nen(r'E:\OCR NEN\CHUA NEN', r'E:\OCR NEN\NEN')

# tạo cấu trúc thư mục
create_struct(r'E:\OCR NEN\CHUA NEN\VI THANH', r'E:\OCR NEN\CHUA NEN\VI THANH')
create_struct(r'E:\OCR NEN\CHUA NEN\VI THUY', r'E:\OCR NEN\CHUA NEN\VI THUY')
create_struct(r'E:\OCR NEN\CHUA NEN\LONG MY', r'E:\OCR NEN\CHUA NEN\LONG MY')

