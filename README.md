# beauty-scraper
template scraper for beauty photography sites    
美女图片网站爬虫模板

## Motivation 动机
After scrapy some beauty photography sites for study purpose, I found there is a common pattern of these kinds of sites.    
We have a homepage, which includes some categories, like star, cosplay, sexy, etc..    
Each category includes several pages, and each single page includes several image sets.
When you clicked into that photograph sets, you can find the photograph sets are also divided into several pages, each page with one beauty photograph.    
These tiny codes aims to extract that pattern, let you to scrape a new photography site easily, by just defining some url extraction rule based on beautifulSoup4.

（基于强烈的求知欲，）最近没事爬了几个美女图网站，我发现这些网站有一个共通的结构。     
主页下有几大分类，每个分类下有多页，每一页又有多套图，每套图点进去又有多页，每页显示一张图片。     
这一小坨代码的目的就是抽出这个结构，用户只需定义少量的基于beautifulSoup4的url查找规则，就能够轻松的爬下该类网站的全部图片。    
## How To Use 如何使用
clone this repository, then   
`pip install beautifulsoup4`    
`pip install requests`    
`python iyi8_example.py`    
you can turn on or turn off multi-thread download by passing `Ture` or `False` to `download_images(multi_thread)`. One thread work for one category.

you can explore `feizl_example.py` and `iyi8_example.py` to find how to write your own scraper, it's really simple.    
Generally, what you need to do is to override the abstractmethod. See comment in `beauty_scraper.py` for details.

Exception process is faulty, you can add as your need.
