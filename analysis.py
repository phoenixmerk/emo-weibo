import pandas as pd
import matplotlib.pyplot as plt
from keywords import get_keywords
import os


def load_data():
    posts = pd.DataFrame()
    comments = pd.DataFrame()
    if os.path.exists("weibo_posts.xlsx"):
        posts = pd.read_excel("weibo_posts.xlsx")
    if os.path.exists("weibo_comments.xlsx"):
        comments = pd.read_excel("weibo_comments.xlsx")
    return posts, comments

def find_negative_texts(posts, comments, keywords):
    """
    利用关键词表筛选负面文本
    """
    negative_posts = []
    negative_comments = []

    # 确保content列是字符串类型，并将NaN值替换为空字符串
    if not posts.empty and 'content' in posts.columns:
        posts['content'] = posts['content'].fillna('').astype(str)
    if not comments.empty and 'content' in comments.columns:
        comments['content'] = comments['content'].fillna('').astype(str)

    for theme, words in keywords.items():
        if not posts.empty:
            for idx, row in posts.iterrows():
                # 确保row['content']是字符串
                if any(word in row['content'] for word in words):
                    negative_posts.append({"theme": theme, "content": row['content']})
        if not comments.empty:
            for idx, row in comments.iterrows():
                # 确保row['content']是字符串
                if any(word in row['content'] for word in words):
                    negative_comments.append({"theme": theme, "content": row['content']})
    return negative_posts, negative_comments


def analyze_and_visualize(negative_posts, negative_comments):
    """
    统计分析并可视化
    """
    df_posts = pd.DataFrame(negative_posts)
    df_comments = pd.DataFrame(negative_comments)

    if not df_posts.empty:
        post_counts = df_posts['theme'].value_counts()
    else:
        post_counts = pd.Series()

    if not df_comments.empty:
        comment_counts = df_comments['theme'].value_counts()
    else:
        comment_counts = pd.Series()
    
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(10, 5))
    if not post_counts.empty:
        plt.subplot(1, 2, 1)
        post_counts.plot(kind='bar', title='负面帖子主题分布')
    if not comment_counts.empty:
        plt.subplot(1, 2, 2)
        comment_counts.plot(kind='bar', title='负面评论主题分布')
    plt.tight_layout()
    plt.savefig("negative_opinion_analysis.png")
    plt.show()


if __name__ == "__main__":
    posts, comments = load_data()
    keywords = get_keywords()
    negative_posts, negative_comments = find_negative_texts(posts, comments, keywords)
    analyze_and_visualize(negative_posts, negative_comments)
    pd.DataFrame(posts).to_excel("all_posts.xlsx", index=False)
    pd.DataFrame(comments).to_excel("all_comments.xlsx", index=False)
    pd.DataFrame(negative_posts).to_excel("negative_posts.xlsx", index=False)
    pd.DataFrame(negative_comments).to_excel("negative_comments.xlsx", index=False)