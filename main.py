from weibo_spider import login_weibo, search_weibo_by_user, search_weibo_by_topic, get_comments_for_post, get_uid_by_post_id
from xslx import save_posts, save_comments
from keywords import get_keywords
from analysis import load_data, find_negative_texts, analyze_and_visualize
import time
import random


def crawl_by_user(driver, username):
    all_posts = []
    all_comments = []

    posts = search_weibo_by_user(driver, username)
    all_posts.extend(posts)

    for post in posts:
        time.sleep(random.uniform(2, 5))
        if 'post_id' in post and post['post_id']:
            uid = get_uid_by_post_id(post['post_id'], driver)
            comments_for_post = get_comments_for_post(post['post_id'], driver, uid)
            all_comments.extend(comments_for_post)  # 直接扩展，因为get_comments_for_post已经处理了结构
        else:
            print(f"警告：跳过没有post_id的帖子: {post}")

    save_posts(all_posts)
    save_comments(all_comments)


def crawl_by_topic(driver, topic):
    all_posts = []
    all_comments = []

    posts = search_weibo_by_topic(driver, topic)
    all_posts.extend(posts)

    for post in posts:
        time.sleep(random.uniform(2, 5))
        if 'post_id' in post and post['post_id']:
            uid = get_uid_by_post_id(post['post_id'], driver)
            comments_for_post = get_comments_for_post(post['post_id'], driver, uid)
            all_comments.extend(comments_for_post)  # 直接扩展
        else:
            print(f"警告：跳过没有post_id的帖子: {post}")

    save_posts(all_posts)
    save_comments(all_comments)


if __name__ == "__main__":
    driver = login_weibo()

    print("开始爬取主题微博...")
    crawl_by_topic(driver, "河北彩花")
    print("主题微博爬取完成。")

    time.sleep(random.uniform(5, 10))

    print("开始爬取用户微博...")
    crawl_by_user(driver, "周也yeah")
    print("用户微博爬取完成。")

    driver.quit()

    print("开始进行负面舆情分析...")
    posts, comments = load_data()
    keywords = get_keywords()
    negative_posts, negative_comments = find_negative_texts(posts, comments, keywords)
    analyze_and_visualize(negative_posts, negative_comments)
    print("分析完成，结果已保存。")