from datetime import datetime
from urllib import request
from urllib.parse import urljoin, urlparse, quote
from lxml import html
import logging
import sys
import os
import re
import time
import threading
import codecs

FILE_NAME_PATTERN = "{cate_id}_{site_id}_{post_id}"
CURRENT_DIR = os.getcwd()
DATA_DIR = os.path.join(CURRENT_DIR, "news_data")
LOG_FILE = os.path.join(CURRENT_DIR, "log.txt")

SITE_CONFIGS = [
    {
        "name": "Thanh Nien",
        "id": "TN",
        "url_xpath": "//*[contains(@class, 'zone--timeline') or contains(@class, 'timeline')]//article//h2/a/@href",
        "content_xpath": "//*[contains(@id, 'main_detail')]//div/text()",
        "next_page_pattern": "trang-{}.html",
        "page_regex": r"trang-(\d+)\.html",
        "categories": [
            { "name": "Pháp luật", "id": "PL", "urls": ["https://thanhnien.vn/thoi-su/phap-luat/"] },
            { "name": "Kinh Doanh", "id": "KD", "urls": ["https://thanhnien.vn/tai-chinh-kinh-doanh/"] },
            { "name": "Thể Thao", "id": "TT", "urls": ["http://thethao.thanhnien.vn/bong-da-viet-nam/",
                                                         "http://thethao.thanhnien.vn/bong-da-quoc-te/",
                                                         "http://thethao.thanhnien.vn/binh-luan/",
                                                         "http://thethao.thanhnien.vn/quan-vot/",
                                                         "http://thethao.thanhnien.vn/hau-truong/",
                                                         "http://thethao.thanhnien.vn/toan-canh-the-thao/"] },
            { "name": "Khoa học - Công Nghệ", "id": "KHCN", "urls": ["https://thanhnien.vn/cong-nghe/"] },
            { "name": "Sức Khoẻ", "id": "SK", "urls": ["https://thanhnien.vn/suc-khoe/"] },
            { "name": "Văn Hoá", "id": "VH", "urls": ["https://thanhnien.vn/van-hoa/"] },
            { "name": "Giáo dục", "id": "GD", "urls": ["https://thanhnien.vn/giao-duc/"]},
            { "name": "Chính trị - Xã hội", "id": "CTXH", "urls": ["https://thanhnien.vn/thoi-su/chinh-tri",
                                                                    "https://thanhnien.vn/thoi-su/dan-sinh"]},
            { "name": "Xe cộ", "id": "XC", "urls": ["https://thanhnien.vn/xe/"]},
            { "name": "Đời sống", "id": "DS", "urls": ["https://thanhnien.vn/doi-song/"]},                                                        
        ]
    },
    {
        "name": "Dan Tri",
        "id": "DT",
        "url_xpath": "//*[contains(@id, 'listcheckepl')]/div//h2/a/@href",
        "content_xpath": "//*[contains(@id, 'divNewsContent')]//p/text()",
        "next_page_pattern": "trang-{}.htm",
        "page_regex": r"trang-(\d+)\.htm",
        "categories": [
            { "name": "Pháp luật", "id": "PL", "urls": ["http://dantri.com.vn/phap-luat.htm"] },
            { "name": "Kinh Doanh", "id": "KD", "urls": ["http://dantri.com.vn/kinh-doanh.htm"] },
            { "name": "Thể Thao", "id": "TT", "urls": ["http://dantri.com.vn/the-thao.htm"] },
            { "name": "Khoa học - Công Nghệ", "id": "KHCN", "urls": ["https://dantri.com.vn/suc-manh-so.htm"] },
            { "name": "Sức Khoẻ", "id": "SK", "urls": ["http://dantri.com.vn/suc-khoe.htm"] },
            { "name": "Văn Hoá", "id": "VH", "urls": ["http://dantri.com.vn/van-hoa.htm",
                                                        "https://dantri.com.vn/giai-tri.htm"] },
            { "name": "Giáo dục", "id": "GD", "urls": ["https://dantri.com.vn/giao-duc-khuyen-hoc.htm"]},
            { "name": "Chính trị - Xã hội", "id": "CTXH", "urls": ["https://dantri.com.vn/xa-hoi.htm",
                                                                    "https://dantri.com.vn/xa-hoi/chinh-tri.htm",
                                                                    "https://dantri.com.vn/xa-hoi/phong-su-ky-su.htm",
                                                                    "https://dantri.com.vn/xa-hoi/moi-truong.htm",
                                                                    "https://dantri.com.vn/xa-hoi/giao-thong.htm",
                                                                    "https://dantri.com.vn/xa-hoi/ho-so.htm"]},
            { "name": "Xe cộ", "id": "XC", "urls": ["https://dantri.com.vn/o-to-xe-may.htm"]},
            { "name": "Đời sống", "id": "DS", "urls": ["https://dantri.com.vn/nhip-song-tre.htm",
                                                        "https://dantri.com.vn/tinh-yeu-gioi-tinh.htm"]},
        ]
    },
    {
        "name": "VNExpress",
        "id": "VNE",
        # "url_xpath": "//article[contains(@class, 'list_news')]/h4/a[1]/@href",
        "url_xpath": "//*[contains(@class, 'title-news')]/a/@href",
        # "content_xpath": "//article[contains(@class, 'content_detail')]/p//text()",
        "content_xpath": "//article[contains(@class, 'fck_detail')]/p//text()",
        "next_page_pattern": "p{}",
        "page_regex": r"p(\d+)",
        "categories": [
            { "name": "Pháp luật", "id": "PL", "urls": ["https://vnexpress.net/phap-luat"] },
            { "name": "Kinh Doanh", "id": "KD", "urls": ["https://vnexpress.net/kinh-doanh/"]},
            { "name": "Thể Thao", "id": "TT", "urls": ["https://vnexpress.net/the-thao/"] },
            { "name": "Khoa học - Công Nghệ", "id": "KHCN", "urls": ["https://vnexpress.net/so-hoa/",
                                                                        "https://vnexpress.net/khoa-hoc"]},
            { "name": "Sức Khoẻ", "id": "SK", "urls": ["https://vnexpress.net/suc-khoe/"] },
            { "name": "Văn Hoá", "id": "VH", "urls": ["https://vnexpress.net/giai-tri/"] },
            { "name": "Giáo dục", "id": "GD", "urls": ["https://vnexpress.net/giao-duc/"]},
            { "name": "Chính trị - Xã hội", "id": "CTXH", "urls": ["https://vnexpress.net/thoi-su"]},
            { "name": "Xe cộ", "id": "XC", "urls": ["https://vnexpress.net/oto-xe-may"]},
            { "name": "Đời sống", "id": "DS", "urls": ["https://vnexpress.net/doi-song",
                                                        "https://vnexpress.net/du-lich",
                                                        "https://vnexpress.net/tam-su"]},
        ]
    },
    {
        "name": "Vietnamnet",
        "id": "VNN",
        "url_xpath": "//*[contains(@class, 'd-ib')]/h3/a/@href",
        "content_xpath": "//*[contains(@id, 'ArticleContent')]/p//text()",
        "next_page_pattern": "trang{}/index.html",
        "page_regex": r"trang(\d+)/index\.html",
        "categories": [
            { "name": "Pháp luật", "id": "PL", "urls": ["http://vietnamnet.vn/vn/phap-luat/"] },
            { "name": "Kinh Doanh", "id": "KD", "urls": ["http://vietnamnet.vn/vn/kinh-doanh/"] },
            { "name": "Thể Thao", "id": "TT", "urls": ["http://vietnamnet.vn/vn/the-thao/"] },
            { "name": "Khoa học - Công Nghệ", "id": "KHCN", "urls": ["http://vietnamnet.vn/vn/cong-nghe/"] },
            { "name": "Sức Khoẻ", "id": "SK", "urls": ["http://vietnamnet.vn/vn/suc-khoe/"] },
            { "name": "Văn Hoá", "id": "VH", "urls": ["http://vietnamnet.vn/vn/giai-tri/"] },
            { "name": "Giáo dục", "id": "GD", "urls": ["https://vietnamnet.vn/vn/giao-duc/"]},
            { "name": "Chính trị - Xã hội", "id": "CTXH", "urls": ["https://vietnamnet.vn/vn/thoi-su/chinh-tri/",
                                                                    "https://vietnamnet.vn/vn/thoi-su/"]},
            { "name": "Xe cộ", "id": "XC", "urls": ["https://vietnamnet.vn/vn/oto-xe-may/"]},
            { "name": "Đời sống", "id": "DS", "urls": ["https://vietnamnet.vn/vn/doi-song/"]},
        ]
    }
]

def write_log(content):
    t = str(datetime.now())
    f = open(LOG_FILE, 'a')
    log_content = "{} - {}\n".format(t, content)
    f.write(log_content)
    f.close()


def extract_urls(root_url, doc, url_xpath):
    """
    Arguments:
        :param root_url:
        :param doc: HTML content extracted from page.
        :param url_xpath: Identity of post urls in doc.

        :type root_url: str
        :type doc: lxml.html.HtmlElement
        :type url_xpath: str

    Returns:
        :return: List of extracted urls.
        :rtype: list[str]
    """

    urls = doc.xpath(url_xpath)
    filtered_urls = []

    for url in urls:
        url = "{}{}".format(root_url, urlparse(url).path)
        url = quote(url)
        filtered_urls.append(url)
    return filtered_urls


def init_page_url(page_url, next_page_pattern):

    pattern = re.compile(r".*\.html|.*\.htm")

    if len(pattern.findall(page_url)) > 0:
        if len(page_url.rsplit(".html", 1)) > 1:
            page_url = page_url.rsplit(".html", 1)[0]
        elif len(page_url.rsplit(".htm", 1)) > 1:
            page_url = page_url.rsplit(".htm", 1)[0] + "/"

    if page_url[-1] == "-":
        page_url = page_url + next_page_pattern.format(1)
    else:
        page_url = urljoin(page_url, next_page_pattern.format(1))
    return page_url


def get_next_page_url(current_url, page_regex, next_page_pattern):

    pattern = re.compile(page_regex)
    next_page = None

    if len(pattern.findall(current_url)) > 0:
        next_page = int(pattern.findall(current_url)[0]) + 1
    else:
        next_page = 2

    next_page_url = re.sub(page_regex, next_page_pattern.format(next_page), current_url)

    return next_page_url


def extract_content(doc, content_xpath):
    """
    Arguments:
        :param doc: HTML content from the page.
        :param content_xpath: Identity of content in doc.

        :type doc: lxml.html.HtmlElement
        :type content_xpath: str

    Returns:
        :return: The news content.
        :rtype: str
    """

    content = doc.xpath(content_xpath)
    content = " ".join(content)
    content = re.sub("\s\s+", " ", content).strip()
    return content


def persist_content(site_id, cate_id, post_id, content):
    """
    Arguments:
        :type site_id: str
        :type cate_id: str
        :type post_id: str
        :type content: str

    Return:
        :rtype: bool
    """

    try:
        if not os.path.isdir(DATA_DIR):
            os.makedirs(DATA_DIR)

        cate_dir = os.path.join(DATA_DIR, cate_id)

        if not os.path.isdir(cate_dir):
            os.makedirs(cate_dir)

        file_name = FILE_NAME_PATTERN.format(site_id=site_id, cate_id=cate_id, post_id=post_id)
        file_path = os.path.join(cate_dir, file_name)

        with codecs.open(file_path, 'w', encoding='utf8') as f:
            f.write(content)
        # f = open(file_path, 'w')
        # f.write(content)
        # f.close()

    except OSError as e:
        print("OS error: {}".format(e))
        return False
    except:
        print("Unexpected error: {}".format(sys.exc_info()[0]))
        return False

    return True


def process_post_content(post_url, content_xpath, site_id, cate_id):
    """
    Arguments:
        :type post_url: str
        :type content_xpath: str
        :type site_id: str
        :type cate_id: str

    Returns:
        :rtype: dict
    """

    # print("Processing: {}".format(post_url))

    result = {
        "post_url": post_url,
        "is_success": False,
        "error": None
    }

    try:
        post_id_pattern = re.compile(r"-(.\d+)\.htm")
        post_id = post_id_pattern.findall(post_url)[0]

        page = request.urlopen(post_url, timeout=5)
        doc = html.fromstring(page.read())

        content = extract_content(doc, content_xpath)
        success = persist_content(site_id, cate_id, post_id, content)

        if not success:
            result["is_success"] = False
            result["error"] = "Could not store content."
            process_log(result)
            return result

    except Exception as e:
        print("Error: {}".format(str(e)))
        print("Error from url: {}".format(post_url))
        result["is_success"] = False
        result["error"] = str(e)
        process_log(result)
        return result

    result["is_success"] = True
    process_log(result)
    return result

def process_log(result):
    content = "[INFO]" if result["is_success"] else "[ERROR]"
    if not result["is_success"]:
        content += " - {}".format(result["error"])
    content += " - {}".format(result["post_url"])

    write_log(content)


def process_page(site_id, cate_id, page_url, url_xpath, content_xpath):
    """
    Arguments:
        :type site_id: str
        :type cate_id: str
        :type page_url: str
        :type url_xpath: str
        :type content_xpath: str
        :type page_regex: str
        :type next_page_pattern: str
    """

    try:
        url_elements = urlparse(page_url)
        page = request.urlopen(page_url, timeout=500)
        doc = html.fromstring(page.read())

    except Exception as e:
        print(e)
        return False
    urls = extract_urls(url_elements.netloc, doc, url_xpath)
    for url in urls:
        url = "{}://{}".format(url_elements.scheme, url)
        process_post_content(url, content_xpath, site_id, cate_id)
    return True

def process_data(site_id, url_xpath, content_xpath, page_regex, next_page_pattern, category):

    # for category in categories:
    #     cate_id = category["id"]
    #     for url in category["urls"]:
    #         url = init_page_url(url, next_page_pattern)
    #         count = 0
    #         while count < 500:
    #             count += 1
    #             process_page(site_id, cate_id, url, url_xpath, content_xpath)
    #             url = get_next_page_url(url, page_regex, next_page_pattern)

    cate_id = category["id"]
    for url in category["urls"]:
        url = init_page_url(url, next_page_pattern)
        count = 0
        while count < 200:
            count += 1
            temp = process_page(site_id, cate_id, url, url_xpath, content_xpath)
            if temp == False: break
            url = get_next_page_url(url, page_regex, next_page_pattern)

if __name__ == '__main__':

    for config in [SITE_CONFIGS[2], SITE_CONFIGS[3]]:
        site_id = config["id"]
        url_xpath = config["url_xpath"]
        content_xpath = config["content_xpath"]
        page_regex = config["page_regex"]
        next_page_pattern = config["next_page_pattern"]
        categories = config['categories']
        thread_num = threading.active_count()
        thread_list = []
        for category in categories:
            thread = threading.Thread(target=process_data, args=(site_id, url_xpath, content_xpath, page_regex, next_page_pattern, category))
            thread_list.append(thread)

        for th in thread_list:
            th.start()
            time.sleep(5)

        # count_th = threading.active_count()
        # while(count_th > thread_num):
        #     # count_th = 0
        #     # for th in thread_list:
        #     #     if(th.is_alive()):
        #     #         count_th = count_th + 1
        #     count_th = threading.active_count()

        
        # process_data(site_id, url_xpath, content_xpath, page_regex, next_page_pattern, categories)
        # thread = threading.Thread(target=process_data, args=(site_id, url_xpath, content_xpath, page_regex, next_page_pattern, categories))
        # thread.start()
        # print("Thread {} is running".format(thread.getName()))
        # time.sleep(1)
