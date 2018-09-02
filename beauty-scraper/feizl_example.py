# -*- coding: utf-8 -*-
'''Example for scrape https://www.feizl.com/'''
from beauty_scraper import BeautyScraper

class FeizlScraper(BeautyScraper):
    def get_category_urls(self):
        return {"https://www.feizl.com/meinv/xinggan/": "xinggan",
                "https://www.feizl.com/meinv/siwameitui/":"siwameitui",
                "https://www.feizl.com/meinv/weimei/": "weimei",
                "https://www.feizl.com/meinv/wangluo/": "wangluo",
                "https://www.feizl.com/meinv/mote/": "mote",
                "https://www.feizl.com/meinv/dongman/": "dongman",}

    def get_page_url(self, index, first_url):
        if index == 0:
            cur_url = first_url
        else:
            cur_url = first_url + "defaultp" + str(index+1) + ".htm"
        return cur_url

    def get_download_folder_path(self):
        return "downloads"

    def get_downloaded_list_name(self, category):
        return "feizl_" + category + ".txt"

    def get_image_tags_on_page(self, soup):
        return soup.find_all("h5")

    def get_image_page_url(self, index, first_url):
        if index == 0:
            return "https://www.feizl.com" + first_url
        return "https://www.feizl.com" + first_url[0:-4] + "_" + str(index) + ".htm"

    def get_image_info(self, soup):
        parent = soup.find("div", class_="tupian")
        if parent is not None:
            img_url = parent.a.img['src']
            print(img_url)
            file_name = parent.a.img['alt']
            print(file_name)
        return img_url, file_name

if __name__ ==  "__main__":
    scraper = FeizlScraper()
    scraper.download_images(multi_thread=False)
