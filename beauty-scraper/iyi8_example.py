# -*- coding: utf-8 -*-
'''Example for scrape http://www.iyi8.com/'''
from beauty_scraper import BeautyScraper

class iyi8Scraper(BeautyScraper):
    def get_category_urls(self):
        return {"http://www.iyi8.com/hot/": "hot",
                "http://www.iyi8.com/photo/mm/":"mm",
                "http://www.iyi8.com/photo/sexy/": "sexy",
                "http://www.iyi8.com/photo/star/": "star",
                "http://www.iyi8.com/photo/event/": "event",}

    def get_page_url(self, index, first_url):
        if index == 0:
            cur_url = first_url
        else:
            cur_url = first_url + str(index+1) + "/"
        return cur_url

    def get_download_folder_path(self):
        return "downloads"

    def get_downloaded_list_name(self, category):
        return "iyi8_" + category + ".txt"

    def get_image_tags_on_page(self, soup):
        return soup.find_all("div", class_="item")

    def get_image_page_url(self, index, first_url):
        if index == 0:
            return first_url
        return first_url[0:-5] + "_" + str(index) + ".html"

    def get_image_info(self, soup):
        parent = soup.find(id="Subcon")
        if parent is not None:
            img_url = parent.contents[3].a.img['src']
            print(img_url)
            file_name = parent.contents[3].a['tltie']
            print(file_name)
        return img_url, file_name

if __name__ ==  "__main__":
    scraper = iyi8Scraper()
    scraper.download_images(multi_thread=True)
