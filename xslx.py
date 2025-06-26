import pandas as pd
import os

def save_posts(posts):
    # 检查文件是否存在，如果存在则加载，否则创建新的DataFrame
    if os.path.exists("weibo_posts.xlsx"):
        df_existing = pd.read_excel("weibo_posts.xlsx")
        df_new = pd.DataFrame(posts)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = pd.DataFrame(posts)

    # 保存到Excel文件，移除 encoding 参数
    df_combined.to_excel("weibo_posts.xlsx", index=False)
    print("帖子已保存到 weibo_posts.xlsx")

def save_comments(comments):
    # 检查文件是否存在，如果存在则加载，否则创建新的DataFrame
    if os.path.exists("weibo_comments.xlsx"):
        df_existing = pd.read_excel("weibo_comments.xlsx")
        df_new = pd.DataFrame(comments)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = pd.DataFrame(comments)

    # 保存到Excel文件，移除 encoding 参数
    df_combined.to_excel("weibo_comments.xlsx", index=False)
    print("评论已保存到 weibo_comments.xlsx")

# init_db 函数不再需要，因为我们不再使用SQLite
# def init_db():
#     pass