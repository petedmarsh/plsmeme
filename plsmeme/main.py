import argparse
import random
import subprocess
import tempfile
import textwrap
from io import TextIOWrapper
from typing import List, Optional

import dotenv
import praw
import requests
import toml

from plsmeme.settings import (PLSMEME_REDDIT_CLIENT_ID,
                              PLSMEME_REDDIT_CLIENT_SECRET,
                              PLSMEME_REDDIT_USERNAME,
                              PLSMEME_REDDIT_PASSWORD,
                              PLSMEME_REDDIT_USER_AGENT)


def download_image(url: str) -> tempfile.NamedTemporaryFile:
    response = requests.get(url)
    temp_file = tempfile.NamedTemporaryFile()
    temp_file.write(response.content)
    return temp_file


def is_image_submission(submission: praw.models.Submission) -> bool:
    url = submission.url.lower()
    return url.endswith('.jpg') or url.endswith('.jpeg') or url.endswith('.png')


def choose_submission(subreddit: praw.models.Subreddit) -> praw.models.Submission:
    submissions = subreddit.top("month")
    image_submissions = list(filter(is_image_submission, submissions))
    return random.choice(image_submissions)


def print_submission(submission, show_attribution):
    f = download_image(submission.url)

    if show_attribution:
        print(textwrap.fill('"{}"'.format(submission.title)), '\n')

    subprocess.run(['catimg', '-w 120', f.name])

    postscript_parts = []

    if show_attribution:
        postscript_parts.append('/r/{} by /u/{}'.format(submission.subreddit.display_name, submission.author.name))

    if show_attribution:
        postscript_parts.append('https://redd.it/{}'.format(submission.id))

    if postscript_parts:
        print('')
        print('\n'.join(postscript_parts))


DEFAULT_CONFIG = {
    'subreddits': ['catpictures', 'dogpictures'],
    'subbreddit_groups': {
        'sfw': ['catpictures', 'dogpictures']
    }
}


def load_config(config_from_ags: Optional[TextIOWrapper]) -> dict:
    config = config_from_ags

    if not config_from_ags:
        try:
            config = open('/plsmeme/config/.plsmeme.toml', 'r')
        except:
            config = open('/plsmeme/config/default.toml', 'r')

    return toml.load(config)


def subreddit_names_from_args(args, config: dict) -> List[str]:
    if args.subreddit:
        return [args.subreddit]

    if args.subreddits_group:
        return config['subreddit_groups'][args.subreddits_group]

    return config['subreddits']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--subreddit', '-r', type=str)
    group.add_argument('--subreddits-group', '-g', type=str)
    group.add_argument('--submission', '-s', type=str)

    parser.add_argument('--config', '-c', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('--show-attribution', '-a', action='store_true')

    args = parser.parse_args()

    reddit = praw.Reddit(
        client_id=PLSMEME_REDDIT_CLIENT_ID,
        client_secret=PLSMEME_REDDIT_CLIENT_SECRET,
        user_agent=PLSMEME_REDDIT_USER_AGENT,
        username=PLSMEME_REDDIT_USERNAME,
        password=PLSMEME_REDDIT_PASSWORD
    )

    config = load_config(args.config)

    if not args.submission:
        subreddit_name = random.choice(subreddit_names_from_args(args, config))
        subreddit = reddit.subreddit(subreddit_name)
        submission = choose_submission(subreddit)
    else:
        submission = praw.models.Submission(reddit, args.submission)

    print_submission(submission, show_attribution=args.show_attribution)
