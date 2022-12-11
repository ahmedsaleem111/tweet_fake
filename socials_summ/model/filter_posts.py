import re
from typing import Optional

import pandas as pd

from socials_summ.model.preprocessing import Corpus


TWEET_PREFIX = "Tweet:"


def preprocess_tweet_text(text: str) -> Optional[str]:
    new_text = re.sub(r"https://t.co/\w+", "", text).strip()
    if len(new_text) < 20:
        # take away small tweets as those are probably mostly image
        return None
    return new_text


def read_tweets(corpus: Corpus) -> pd.DataFrame:
    """
    Takes a corpus and returns a dataframe with 2 columns: (caption, likes)
    """
    captions = []
    likes = []
    for post in corpus.posts:
        captions.append(post.caption)
        likes.append(post.likes)

    return pd.DataFrame({"caption": captions, "likes": likes})


def print_post_prompt(caption: str) -> str:
    return f"{TWEET_PREFIX} {caption}"


def get_prompt_text(captions: pd.Series) -> str:
    return "\n".join(captions.apply(print_post_prompt)) + f"\n{TWEET_PREFIX}"


def get_new_prompt(df: pd.DataFrame, topn: int = 30) -> str:
    # filter out retweets, preprocess the remaining tweets, and keep the
    # most popular `topn`
    df_no_nulls = df[~df.caption.isnull()]
    df_no_retweets = df_no_nulls[~df_no_nulls.caption.str.startswith("RT @")]
    df_preproc = df_no_retweets.assign(
        caption=df_no_retweets.caption.apply(preprocess_tweet_text)
    ).sort_values("likes").tail(topn)

    # output prompt for the model
    return get_prompt_text(df_preproc.caption)


def get_prompt(corpus: Corpus, topn: int = 30) -> str:
    df = read_tweets(corpus)
    return get_new_prompt(df, topn)
