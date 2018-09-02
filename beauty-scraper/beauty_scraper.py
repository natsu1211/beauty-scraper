# -*- coding: utf-8 -*-
import os
import requests
import shutil
import time
import threading
import beauty_scraper_util as bsUtil
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod

DL_FOLDER_NAME = 'downloads'


class BeautyScraper(object):
    '''Inherit this class and overwrite all the abstractmethods'''
    __metaclass__ = ABCMeta
    @abstractmethod
    def get_category_urls(self):
        '''Return category start urls as a dict
        Example:
        return {"http://www.iyi8.com/hot/": "hot",
        "http://www.iyi8.com/photo/mm/":"mm",
        "http://www.iyi8.com/photo/sexy/": "sexy",
        "http://www.iyi8.com/photo/star/": "star",
        "http://www.iyi8.com/photo/event/": "event",
        }
        '''
        pass

    @abstractmethod
    def get_page_url(self, index, first_url):
        '''Return page url with index based on first_url
        Example:
        first_url : "http://www.iyi8.com/star"
        other page url with index 3: "http://www.iyi8.com/star/3.html"
        '''
        pass

    @abstractmethod
    def get_download_folder_path(self):
        '''Return path for download folder name
        beauty_scraper will create a folder located at the returned path for downloaded images.
        The path is relatived to current module path.
        Example:
        return "downloads"
        '''
        pass

    @abstractmethod
    def get_downloaded_list_name(self, category):
        '''Return name for downloaded list file
        Example:
        return "iyi8_" + category + ".txt"
        '''
        pass

    @abstractmethod
    def get_image_tags_on_page(self, soup):
        '''Return image html tag that contain image url'''
        pass

    @abstractmethod
    def get_image_page_url(self, index, first_url):
        '''Return image page url based on first_url and index
        like "http://www.iyi8.com/2017/mm_1225/2928_3.html"
        '''
        pass

    @abstractmethod
    def get_image_info(self, soup):
        '''Retrun image url and image name'''
        pass

    def download_images(self, multi_thread=False):
        '''Download images of all categories'''
        start_urls = self.get_category_urls()
        print(start_urls)
        if multi_thread:
            for url, c in start_urls.items():
                work_thread = threading.Thread(target=self._download_images_category, args=(url, c))
                work_thread.start()
        else:
            for url, c in start_urls.items():
                self._download_images_category(url, c)

    def _download_images_category(self, first_url, category):
        '''Download images of specific category'''
        DIR_NAME = self.get_download_folder_path()
        if not os.path.exists(DIR_NAME):
            os.makedirs(DIR_NAME)
        # download images from every page
        MAX_PAGE = 1000
        for page_index in range(MAX_PAGE):
            page_url = self.get_page_url(page_index, first_url)
            resp = requests.get(page_url)
            if resp.status_code != 200:
                return
            soup = BeautifulSoup(resp.text, "lxml")
            self._download_images_on_page(soup, category)

    def _download_images_on_page(self, soup, category):
        '''Download iamges of specific category of one page'''
        tags = self.get_image_tags_on_page(soup)
        for tag in tags:
            a = tag.a
            if a is not None:
                image_page_first_url = tag.a['href']
                IMAGE_PAGE_COUNT = 100
                for i in range(IMAGE_PAGE_COUNT):
                    image_page_url = self.get_image_page_url(i, image_page_first_url)
                    r = requests.get(image_page_url)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, "lxml")
                        try:
                            self._download_image(soup, i, category)
                        except Exception as e:
                            print(e)
                            continue
                    else:
                        break

    def _download_image(self, soup, index, category):
        '''Find real url and name of image in soup and download it'''
        img_url, file_name = self.get_image_info(soup)
        dir_path = self.get_download_folder_path()
        list_name = self.get_downloaded_list_name(category)
        if bsUtil.check_downloaded(img_url, list_name=dir_path + "/" + list_name):
            return
        with open(dir_path + "/" + list_name, "a+") as f:
            f.write(img_url + "\n")
        path = self.get_download_folder_path()
        category_dir = path + "/" + category + "/"
        bsUtil.download(img_url, file_name, file_name + "_" + str(index) + ".jpg", category_dir)
        time.sleep(10)
