
from IPython import embed
from google_trends import get_GT_data
from twitter import get_twitter_data
from chatgpt import use_chatgpt


# Google Trends
data_GT = get_GT_data()
print('Data GT', data_GT)

# ChatGPT
answer = use_chatgpt()
embed()


# Twitter
data_Twitter = get_twitter_data()
print('Data GT', data_GT)
embed()