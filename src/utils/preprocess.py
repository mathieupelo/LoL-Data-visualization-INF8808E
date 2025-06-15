'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd

def round_decimals(my_df):
    '''
        Rounds all the numbers in the dataframe to two decimal points

        args:
            my_df: The dataframe to preprocess
        returns:
            The dataframe with rounded numbers
    '''
    # TODO : Round the dataframe
    return None


def get_range(col, df1, df2):
    '''
        An array containing the minimum and maximum values for the given
        column in the two dataframes.

        args:
            col: The name of the column for which we want the range
            df1: The first dataframe containing a column with the given name
            df2: The first dataframe containing a column with the given name
        returns:
            The minimum and maximum values across the two dataframes
    '''
    # TODO : Get the range from the dataframes
    return []


def combine_dfs(df1, df2):
    '''
        Combines the two dataframes, adding a column 'Year' with the
        value 2000 for the rows from the first dataframe and the value
        2015 for the rows from the second dataframe

        args:
            df1: The first dataframe to combine
            df2: The second dataframe, to be appended to the first
        returns:
            The dataframe containing both dataframes provided as arg.
            Each row of the resulting dataframe has a column 'Year'
            containing the value 2000 or 2015, depending on its
            original dataframe.
    '''
    # TODO : Combine the two dataframes
    return None


def sort_dy_by_yr_continent(my_df):
    '''
        Sorts the dataframe by year and then by continent.

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    # TODO : Sort the dataframe
    return None

def preprocess_lollipop(df: pd.DataFrame, top_k =5)->pd.DataFrame:
    """
    Preprocess the data for the lollipop chart.

    args:
        - df: the dataframe to process
        - top_k: The number of top pair duos to considere and group others pairs to other category
    return:
        processed dataframe
    """
    # Filter for bot and support roles
    bot_sup_df = df[df['position'].isin(['bot', 'sup'])]

    # Group by game and team to find pairings
    pairings = (
        bot_sup_df.groupby(['gameid', 'teamname'])
        .apply(lambda x: tuple(sorted(x['champion'])))
        .reset_index(name='pair')
    )

    # Count frequency of each unique pairing
    pair_counts = pairings['pair'].value_counts().reset_index()
    pair_counts.columns = ['pair', 'count']

    # Get top k pairings for the pie chart
    top_pairs = pair_counts.head(top_k)
    other_count = pair_counts['count'].iloc[top_k:].sum()

    top_pairs.insert(0,['pair','count'],['Others',other_count])
    return top_pairs

