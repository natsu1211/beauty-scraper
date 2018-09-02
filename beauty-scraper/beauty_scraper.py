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
        '''Provide category start urls and its name
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
        '''Provide page url with index based on first_url.
        e.g.:
        index 0 (first_url): "http://www.iyi8.com/star"
        index 3: "http://www.iyi8.com/star/3.html"
        '''
        pass

    @abstractmethod
    def get_download_folder_path(self):
        '''Provide path for download folder name.
        beauty_scraper will create a folder located at the provided path for downloaded images.
        The path is relatived to current module path.
        e.g.:
        return "downloads"
        '''
        pass

    @abstractmethod
    def get_downloaded_list_name(self, category):
        '''Provide name for downloaded list file.
        This file is used to check whether a image has been downloaded.
        e.g.:
        return "iyi8_" + category + ".txt"
        '''
        pass

    @abstractmethod
    def get_image_tags_on_page(self, soup):
        '''Provide image html tag that contain image url
        e.g.:
        return soup.find_all("div", class_="item")
        '''
        pass

    @abstractmethod
    def get_image_page_url(self, index, first_url):
        '''Provide image page url based on first_url and index
        e.g.:
        index 0 (first_url): "http://www.iyi8.com/2017/mm_1225/2928.html"
        index 3: "http://www.iyi8.com/2017/mm_1225/2928_3.html"
        '''
        pass

    @abstractmethod
    def get_image_info(self, soup):
        '''Find image url and image name in soup
        e.g.:
        (sometimes you can locate the parent element of 'img' tag first)
        parent = soup.find("div", class_="tupian")
        img_url = parent.a.img['src']
        file_name = parent.a.img['alt']
        '''
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
        try:
            if not os.path.exists(DIR_NAME):
                os.makedirs(DIR_NAME)
        except:
            pass
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
        # to avoid IP banned, you can use a better strategy
        time.sleep(10)
