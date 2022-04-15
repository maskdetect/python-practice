work_dir = "VOC_MASK/Annotations"  # self_xml文件所在的目录
new_dir = 'VOC_MASK/Annotations/old'  # dst_xml 文件所在的目录

for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
    for filename in filenames:
        file_path = os.path.join(parent, filename)
        file = open(file_path, "r+", encoding='UTF-8')
        newFile = open(new_dir+filename, "w", encoding='UTF-8') # filename
        print(new_dir+filename)
        for line in file.readlines():    # 读取文件的每一行
             #! 修改标签为我们自己设定的然后再copy过去
            if("FIRC" in line):
                line = line.replace("FIRC", "Unknown")
            if("person" in line): # 直接把 person 改了
                line = line.replace("person", "not_standard")
            newFile.writelines(line)
        print(filename)
        newFile.close()
        file.close()
