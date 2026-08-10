import logging
import shutil
import os

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
public_exists = os.path.exists(PUBLIC_PATH)
if public_exists is False:
    os.mkdir(PUBLIC_PATH)

def remove_all(path:str):
    children = os.listdir(path)

    for item in children:
        item_path = os.path.join(path, item)
        Is_File, Is_Dir = os.path.isfile(item_path), os.path.isdir(item_path)
        
        if Is_File is True:
            os.remove(item_path)
        elif Is_Dir is True:
            remove_all(item_path)
            os.remove(item_path)

def copy_and_move_all(src_path:str, dst_path:str):
    children = os.listdir(src_path)

    for item in children:
        item_path = os.path.join(src_path, item)
        new_dst_path = os.path.join(dst_path, item)
        Is_File, Is_Dir = os.path.isfile(item_path), os.path.isdir(item_path)

        if Is_Dir is True:
            os.mkdir(new_dst_pathh)
            copy_and_move_all(item_path, new_dst_path)
        elif Is_File is True:
            shutil.copy(item_path, new_dst_path)



def main():
    remove_all(PUBLIC_PATH)
    copy_and_move_all(STATIC_PATH, PUBLIC_PATH)
    

if __name__ == '__main__':
    main()