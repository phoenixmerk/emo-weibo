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


def get_comments_for_post(post_id, driver):
    """
    爬取某条微博的所有评论和回复，并保留回复关系
    返回结构化数据：[{comment_id, user, content, reply_to, is_reply}]
    """
    if not post_id:
        print("警告：post_id为空，无法获取评论。")
        return []

    # 微博详情页链接（根据实际情况调整）
    url = f"https://weibo.com/detail/{post_id}"
    driver.get(url)
    time.sleep(5)  # 等待页面加载

    # 自动下拉加载更多评论
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    comments_data = []
    # 假设评论区每条评论在 <div class="list_con"> 里
    comment_blocks = soup.find_all("div", class_="list_con")
    for block in comment_blocks:
        try:
            user_elem = block.find("a", class_="name")
            content_elem = block.find("span", class_="txt")
            user = user_elem.text.strip() if user_elem else ""
            content = content_elem.text.strip() if content_elem else ""
            if not content:
                continue
            comments_data.append({
                "post_id": post_id,
                "user": user,
                "content": content,
                "reply_to": "",  # 可扩展为回复关系
                "is_reply": False
            })
        except Exception as e:
            continue
    return comments_data