import os

def get_files(root_path):  # 注意root_path前加上r
    '''
    获得目录root_path下（包括各级子目录）所有文件的路径
    '''
    file_list = []
    for i in os.listdir(root_path):
        path = root_path + r'\\' + i
        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            files = get_files(path)
            for f in files:
                file_list.append(f)
    return file_list


def word_in_files(root_path, word):
    '''
    获得目录root_path下（包括各级子目录）所有包含字符串word的文件的路径
    '''
    file_list = get_files(root_path)
    result = []
    for path in file_list:
        if word in os.path.split(path)[1]:
            result.append(path)
    return result

if __name__ == '__main__':
    print(word_in_files(r'/Users/hexiangyu/Downloads/mask_detect/masks/VOC_MASK/JPEGImages', 'H'))