#这里尝试读取txt文件夹来做词性标注
import os
import chardet

root = '/Users/fafaya/Desktop/Paris Olympics/Paris Olympics/奥林匹克英文推文'

folderlist = os.listdir(root)

en_data = {}

folderlist_temp = []

for folder in folderlist:
    if '.DS_Store' not in folder:
        folderlist_temp.append(folder)

folderlist = folderlist_temp

def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']

    with open(file_path, 'r', encoding=encoding) as f:
        return f.read().strip()


for folder in folderlist:
    papers = {}  # 这是用来记录文件名和里面的内容的字典

    folder_path = os.path.join(root, folder)
    filelist = os.listdir(folder_path)

    filelist_temp = []
    for file in filelist:
        if '.DS_Store' not in file:
            filelist_temp.append(file)

    filelist = filelist_temp

    for file in filelist:
        file_path = os.path.join(folder_path, file)
        content = read_file_with_chardet(file_path)  # 使用chardet自动检测编码
        content = content.replace('\n', '').replace(' ', '').replace(' ', '')
        papers[file] = content

    en_data[folder] = papers
