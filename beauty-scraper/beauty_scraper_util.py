# -*- coding: utf-8 -*-
import os
import shutil
import requests

def load_dl_file(file_path, enc='utf-8'):
    '''Load downloaded image list file'''
    lists = []
    f = open(file_path, 'r', encoding=enc)
    lines = f.readlines()
    for line in lines:
        lists.append(line)
    f.close()
    return lists

def check_downloaded(url, list_name):
    '''Check if image with url has downloaded'''
    if os.path.exists(list_name):
        lists = load_dl_file(list_name)
        if url in lists:
            return True
    return False

def download(image_url, folder_name, file_name, category_name="./"):
    '''Download image located at image_url'''
    r = requests.get(image_url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        f_name = category_name + folder_name
        if not os.path.exists(f_name):
            os.makedirs(f_name)
        with open(f_name + "/" + file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
