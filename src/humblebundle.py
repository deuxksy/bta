import requests
import scrapy

# response = requests.get(url)
# html = Selector(text=response.text)
# rating_list = html.xpath('//tr[contains(@id, "ctl00_ContentHolder_rptGradeDoc_ctl")]')
# page_list = html.xpath('//tr[contains(@id, "ctl00_ContentHolder_pgrBoardPager_PagerList_ct")]')
# page_next = html.xpath('//a[@style="font-weight:bold;color:#353959;font-size:12px;border-color:#353959;background:#f8f9fb;"]/following-sibling::a[1]')

if __name__ == '__main__':
    url_games = 'http://www.humblebundle.com'
    url_books =  'http://www.humblebundle.com/books'
    response = requests.get(url_books)
    html = scrapy.Selector(text=response.text)
    next_urls = html.xpath('//div[@id="subtab-container"]/a[not(contains(@href, "#"))]/@href').extract()
    print (next_urls)