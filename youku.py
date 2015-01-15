#-*- coding:utf-8 -*-
from __future__ import unicode_literals


def get_youku_stats(url, timeout=30):

    def download():
        from ghost import Ghost
        ghost = Ghost(wait_timeout=timeout, download_images=False, display=False)
        ghost.open(url)
        ghost.click(b'#fn_stat')
        ghost.wait_for_text("本集数据")
        ghost.wait_for_text("总播放数:")
        return ghost.content

    def get_stats(html):
        import re
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html)

        def get_one_stat(key, search_text):
            try:
                return key, int(soup.find(id="videodetailInfo").find(
                    "label", text=re.compile(search_text)).parent.span.string.replace(",", "").strip())
            except Exception as err:
                return key, None

        def get_two_stats(key1, key2, search_text):
            try:
                v1, v2 = soup.find(id="videodetailInfo").find(
                    "label", text=re.compile(search_text)).parent.span.string.replace(",", "").split("/")
                return [(key1, int(v1.replace(",", "").strip())), (key2, int(v2.replace(",", "").strip()))]
            except Exception as err:
                return [(key1, None), (key2, None)]

        return dict([get_one_stat(key, search_text) for key, search_text in
                     [("play", "总播放数:"), ("favorite", "收藏:"), ("comment", "评论:")]] +
                    get_two_stats("up", "down", "顶 / 踩:"))

    return get_stats(download())


print get_youku_stats("http://v.youku.com/v_show/id_XODcxOTQ4MTk2.html")
print get_youku_stats("http://v.youku.com/v_show/id_XODcyMjA1NTky.html")
print get_youku_stats("http://v.youku.com/v_show/id_XNzcyMTExMTcy.html")
print get_youku_stats("http://v.youku.com/v_show/id_XODcxNzYxMTUy.html")
print get_youku_stats("http://v.youku.com/v_show/id_XODI5NzUwODgw.html")

