import os

work_dir = '../VOC_MASK/Annotations/'
new_dir= '../VOC_MASK/Annotations/'
print(1)
# masks/VOC_MASK/JPEGImages/1_Handshaking_Handshaking_1_341.jpg

for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            file = open(file_path,"r+",encoding='UTF-8')
            newFile = open(new_dir+filename,"w",encoding='UTF-8')
            for line in file.readlines():
                if("FIRC" in line):
                    line = line.replace("FIRC","Unknown")
                if("person" in line):
                    line = line.replace("person","not_standard")
                newFile.writelines(line)
            print (filename)
            newFile.close()
            file.close()