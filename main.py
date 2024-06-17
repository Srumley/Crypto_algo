
from IPython import embed
from google_trends import get_GT_data
from twitter import get_twitter_data


# Google Trends
data_GT = get_GT_data()
print('Data GT', data_GT)

# Twitter
data_Twitter = get_twitter_data