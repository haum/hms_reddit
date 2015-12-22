import praw

import settings


def get_submissions():
    r = praw.Reddit(user_agent=settings.USER_AGENT)
    submissions = r.get_subreddit('haum').get_hot(limit=5)
    return filter(lambda x: not already_posted(x), submissions)

def already_posted(sub):
    with open('posted') as f:
        posted = f.read().splitlines()
        return sub.id in posted

def mark_posted(sub):
    with open('posted', 'a') as f:
        f.write(sub.id + '\n')

def init_file():
    with open('posted', 'w') as f:
        f.flush()


if __name__ == "__main__":
    init_file()
