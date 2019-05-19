import praw
import time
from newspaper import Article

# ------OPTIONS------

MAX_CONTENT_LENGTH = 1700  # maximum number of characters in the comment
SUBREDDIT_NAME = "nameofsubreddit"

# URL Blacklist
blacklist = [

    "bloomberg",
    "youtube.com",
    "twitter.com",
    "redandblack",
    "imgur",
    "facebook"
    "gify"

    ]

# -------------------


blacklist_length = len(blacklist)


def main_func():

    # praw.ini file in same folder contains config info
    reddit = praw.Reddit('article_expander')
    subreddit = reddit.subreddit(SUBREDDIT_NAME)

    for submission in subreddit.stream.submissions(skip_existing=True):
        if submission.is_self:
            print("No link. Ignored \n")
        elif is_valid_source(submission.url):
            print(submission.url)
            link = submission.url

            article = Article(link)

            try:
                article.download()
                article.parse()
                article_content = article.text
                if len(article_content) < 400:
                    # This guards against websites that send error messages and false info.
                    # Helps reduce the size of the blacklist
                    print("Content too short. Ignored")
                else:

                    article_short = (article_content[:MAX_CONTENT_LENGTH] + '.......') \
                        if len(article_content) > MAX_CONTENT_LENGTH else article_content
                    article_short = article_short + "\n\nMore: " + link
                    print(article_short)
                    submission.reply(article_short)

            except Exception as e2:
                print(e2)
                print("Error: Can't retrieve or can't post.")

# End of main function


# Check validity of source
def is_valid_source(link_url):
    is_problem = False
    for i in range(blacklist_length):
        if blacklist[i] in link_url:
            print("Source Blacklisted ")
            is_problem = True
    source_valid = not is_problem

    return source_valid


# Initiate code
while True:

    try:
        print("Started Bot")
        main_func()
    except Exception as e:
        # I know catch-all is bad, but it is what it is...
        # if you use it too much, it stops
        # Inform me about the failure of main function
        print(e)
        # and wait because reddit has temp bans and time limits and such
        time.sleep(1000)

# End Init code



