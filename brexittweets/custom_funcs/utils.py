import pandas as pd


def aggregate_sentiment_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group data by five-minute timeslot and count positive and negative tweets,
    and calculate percentage that are positive
    :param df: a pandas DataFrame
    :return: a pandas DataFrame
    """
    grouped_sentiment_times = df.groupby(['datetime_slot', 'sentiment'])['id'].count(). \
        reset_index().rename(columns={'id': 'count'})
    grouped_sentiment_times['index'] = list(range(len(grouped_sentiment_times)))

    grouped_sentiment_times = pd.pivot_table(grouped_sentiment_times,
                                             values='count',
                                             index=['datetime_slot'],
                                             columns=['sentiment']).reset_index()

    grouped_sentiment_times['percentage_positive'] = grouped_sentiment_times['positive'] / (
            grouped_sentiment_times['positive'] +
            grouped_sentiment_times['negative'] +
            grouped_sentiment_times['neutral'])

    grouped_sentiment_times['day'] = grouped_sentiment_times['datetime_slot'].apply(lambda x: x.date().day)
    return grouped_sentiment_times


def positive_negative(num: float) -> str:
    """
    Classify tweets as positive or negative based on polarity value
    """
    if num > 0.1:
        return 'positive'
    elif num < -0.1:
        return 'negative'
    else:
        return 'neutral'


def color_vals(sentiment: float) -> str:
    """
    Colour-code values of sentiment for plotting with matplotlib.pyplot
    """
    if sentiment > 0.1:
        return '#00B050'
    elif sentiment >= -0.1:
        return '#1DA1F2'
    else:
        return '#D53F3B'
