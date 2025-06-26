from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import random


def login_weibo():
    """
    用 selenium 打开微博并手动扫码登录
    """
    driver = webdriver.Chrome()
    driver.get("https://weibo.com/login.php")
    print("请在弹出的浏览器窗口中扫码登录微博，登录后按回车继续...")
    input()
    return driver


def search_weibo_by_user(driver, username, max_count=10):
    """
    真实爬取指定用户的微博（driver为已登录的浏览器）
    """
    user_url = "https://weibo.com/u/6741964788?tabtype=home"  # 请确保这个URL是周也yeah的真实UID或通过搜索获取
    driver.get(user_url)
    time.sleep(random.uniform(3, 6))

    if "外星人绑架了" in driver.page_source or "验证码" in driver.page_source:
        print(f"警告：访问用户 {username} 主页时遇到反爬或验证码。请手动处理或等待。")
        return []

    posts = []
    soup = BeautifulSoup(driver.page_source, "lxml")
    cards = soup.find_all("div", {"node-type": "feed_list_item"})
    for card in cards[:max_count]:
        content_elem = card.find("p", {"node-type": "feed_list_content"})
        if content_elem:
            posts.append({
                "user": username,
                "content": content_elem.text.strip(),
                "post_id": card.get("mid", "")
            })
            post_id = card.get("mid", "")
            print(f"Extracted post_id: {post_id}")
    return posts


def search_weibo_by_topic(driver, topic, max_count=10):
    """
    真实爬取指定主题的微博（driver为已登录的浏览器）
    """
    driver.get("https://s.weibo.com/weibo?q=" + topic)
    time.sleep(random.uniform(3, 6))

    if "外星人绑架了" in driver.page_source or "验证码" in driver.page_source:
        print(f"警告：访问主题 {topic} 搜索页时遇到反爬或验证码。请手动处理或等待。")
        return []

    posts = []
    soup = BeautifulSoup(driver.page_source, "lxml")
    cards = soup.find_all("div", class_="card-wrap")
    for card in cards[:max_count]:
        content_elem = card.find("p", class_="txt")
        if content_elem:
            user_elem = card.find("a", class_="name")

            post_id = card.get("mid", "")
            if not post_id:
                post_id_div = card.find("div", class_="card-feed")
                if post_id_div:
                    post_id = post_id_div.get("mid", "")

            posts.append({
                "user": user_elem.text.strip() if user_elem else "",
                "content": content_elem.text.strip(),
                "post_id": post_id
            })
            post_id = card.get("mid", "")
            print(f"Extracted post_id: {post_id}")
    return posts

def get_uid_by_post_id(post_id, driver):
    """
    根据 post_id 打开微博详情页，模拟刷新后从URL中提取 uid
    """
    detail_url = f"https://weibo.com/detail/{post_id}"
    driver.get(detail_url)
    
    time.sleep(3)  # 等待页面加载
    
    # 模拟刷新页面
    driver.refresh()
    
    time.sleep(3)  # 等待刷新后加载
    
    current_url = driver.current_url
    print(f"当前页面URL：{current_url}")
    
    # 使用正则从URL中提取 uid
    import re
    match = re.search(r'https?://weibo\.com/(\d+)/', current_url)
    if match:
        return match.group(1)
    else:
        print("警告：无法从刷新后的URL中提取uid")
        return None
def get_comments_for_post(post_id, driver, uid):
    """
    爬取某条微博的所有评论和回复（通过调用Ajax接口）
    返回结构化数据：[{user, content}]
    
    参数说明：
    - post_id: 微博帖子ID (字符串)
    - driver: 已登录的 Selenium WebDriver 实例
    - uid: 帖子作者的 uid (字符串)
    """
    if not post_id or not uid:
        print("警告：post_id 或 uid 为空，无法获取评论。")
        return []

    # 构造评论请求 URL
    comment_url = (
        f"https://weibo.com/ajax/statuses/buildComments?"
        f"is_reload=1&id={post_id}&is_show_bulletin=2&is_mix=0"
        f"&count=20&uid={uid}&fetch_level=0&locale=zh-CN"
    )

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'https://weibo.com/detail/{post_id}'
    }

    # 使用 Selenium 获取 Cookie 并注入到 requests 中
    cookies = {cookie['name']: cookie['value'] for cookie in driver.get_cookies()}

    import requests
    response = requests.get(comment_url, headers=headers, cookies=cookies)

    if response.status_code == 200:
        try:
            data = response.json()
            comments = []
            for item in data.get("data", []):
                if isinstance(item, dict):
                    user = item.get("user", {}).get("screen_name", "未知用户")
                    content = item.get("text", "").strip()
                    if content:
                        print(f"用户：{user} | 内容：{content}")
                        comments.append({
                            "user": user,
                            "content": content
                        })
            return comments
        except Exception as e:
            print("解析评论失败:", e)
    else:
        print(f"请求评论失败，状态码: {response.status_code}")
    return []