import praw
from IPython import embed

def get_reddit_data():

    # Configurer les clés d'API
    reddit = praw.Reddit(
        client_id='jR67A-aIdnhKhTxSXvqulA',
        client_secret='Ag-fP_rt4JihyRT_x_B34kfPK7tLiA',
        user_agent='Educational-Will8448'
    )

    # Fonction pour récupérer les posts d'un subreddit
    def get_reddit_posts(subreddit_name, limit=100):
        subreddit = reddit.subreddit(subreddit_name)
        posts_all_infos = [[post.title, post.selftext, post.created_utc, post.author.name] for post in subreddit.hot(limit=limit)]
        posts_only = [[post.selftext] for post in subreddit.hot(limit=limit)]
        return posts_only

    # Exemple d'utilisation
    posts = get_reddit_posts('bitcoin', 100)
    for post in posts:
        print(post)

    return posts
