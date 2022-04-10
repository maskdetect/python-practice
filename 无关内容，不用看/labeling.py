import os

def get_files(root_path):  # 注意root_path前加上r
    '''
    获得目录root_path下（包括各级子目录）所有文件的路径
    '''
    file_list = []
    for i in os.listdir(root_path):
        path = root_path + r'/' + i
        if os.path.isdir(path):
            files = get_files(path)
            for f in files:
                file_list.append(f)
        else:
            file_list.append(path)
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


src_dir = r'E:\Users\hexiangyu\Downloads\dataset1 2\JPEGImages'  # 源文件目录地址
dst_dir = r'/Users/hexiangyu/Downloads/yolov3 口罩/home/aistudio/masks/VOC_MASK/JPEG1/labeling'  # 目标文件目录地址

def list_all_files(rootdir):
    import os
    _files = []

    # 列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)

    for i in range(0, len(list_file)):

        # 构造路径
        path = os.path.join(rootdir, list_file[i])

        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归

        # if os.path.isdir(path):
        #     _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(list_file[i])
    return _files

if __name__ == '__main__':
    # imagelist=(word_in_files(r'/Users/hexiangyu/Downloads/mask_detect/masks/VOC_MASK/JPEGImages', 'H'))
    #列出本目录下所有文件
    files = list_all_files(src_dir)
    print(files)
    file_handle = open("1.txt", mode='w')
    for image in files:
        # txtsrc=image.split('.')[0]+'.txt'
        file_handle.write(image[:-4]+'\n')
    file_handle.close()
    # for image in files:
    #     txtsrc=image.split('.')[0]+'.txt'
    #     file_handle = open(dst_dir+"/"+txtsrc, mode='w')
    #     file_handle.write("1")
    #     file_handle.close()

    #明天我需要把群里三个图片都用文件夹的形式给txt打标签，然后与box对比，测得准确度