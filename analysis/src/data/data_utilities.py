import ast
import itertools

import numpy as np
import pandas as pd

from itertools import zip_longest
from collections import OrderedDict


def flatten(list_of_iters):
    """flatten
    Flattens a list of iterables into a single flat list.
    
    Args:
    list_of_iters: list of iterables
    
    Returns:
    flattened: list
    """
    flattened = [item for iter in list_of_iters for item in iter]
    return flattened

def eval_column(df, column):
    """literal_eval_column
    Iterates through a DataFrame column and returns a list of each element,
    literally evaluated.

    Args:
        df: DataFrame
            The dataframe containing the column to be evaluated.
        column: str
            The name of the column to be evaluated.
    Returns:
    l: list
        List of literally evaluated elements.
    """
    l = [ast.literal_eval(i) for i in df[column]]
    return l

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

def dataframe_health_report(df, norm=False, report=False, diagnosis=False):
    """data_frame_health_report
    Runs a bunch of diagnostics against the values of a DataFrame. These include 
    finding min/max values, and missing value counts etc.
    
    Args:
    df (pandas.DataFrame): DataFrame to perform health check on.
    norm (bool): Determines whether to normalise columns which represent a count.
    report (bool): Prints health_report_df if True. Defaults to False.
    diagnosis (bool): Print a semantic diagnosis of your DataFrame's health.
    
    Returns:
    health_report_df (pandas.DataFrame): DataFrame containing results of health check.
        Attributes that are assessed for all columns:
        - dtype: The column's numpy dtype
        - non_null_count: The number of elements that do not satisfy pandas.isnull
        - null_count: The number of elements that satisfy pandas.isnull
        - NaN_count: The number of elements with value np.nan
        - unique_values: The number of unique values
        - modal_value: The modal value
        - modal_value_count: The number of elements with the modal value
        
        Attributes that are assessed for columns with dtype 'float64' of 'int32'
        - +inf: Number of elements with value np.inf 
        - -inf: Number of elements with value -np.inf
        - min: Minimum value
        - max: Maximum value
        - zeros_count: Number of elements with value 0
        - mean: Mean value
        - 25%: 25th percentile value
        - 50%: Median value
        - 75% 75th percentile value
        
        Attributes that are assessed for columns with dtype 'object'
        - string_length_min: The length of the shortest string
        - string_length_max: The length of the longest string
        - string_length_median: The median string length
        - string_empty_count: Number of strings with length 0
    """
    
    health_report = OrderedDict()
    
    n_rows = len(df)
    dtypes = [str(d) for d in df.dtypes.values]
    
    for col, dtype in zip(df.columns, dtypes):
        s = df[col]
        # generic health checks
        col_health = OrderedDict()
        col_health['dtype'] = str(dtype)
        col_health['non_null_count'] = s.count()
        col_health['null_count'] = sum(pd.isnull(s))
        col_health['NaN_count'] = sum(pd.isna(s))
        col_health['unique_values'] = len(s.value_counts())
        mode = s.mode().values[0]
        col_health['modal_value'] = mode
        col_health['modal_value_count'] = len(s[s == mode])
        
        if (dtype == 'float64') | (dtype == 'int32'):
            col_health['+inf_count'] = sum(np.isposinf(s))
            col_health['-inf_count'] = sum(np.isneginf(s))
            col_health['min'] = s.min()
            col_health['max'] = s.max()
            col_health['zeros_count'] = len(s[s == 0])
            col_health['mean'] = s.mean()
            col_health['25%'] = s.quantile(.25)
            col_health['50%'] = s.quantile(.5)
            col_health['75%'] = s.quantile(.75)
        
        if dtype == 'object':
            stringed = s.str
            stringed_len = stringed.len()
            col_health['string_length_min'] = stringed_len.min()
            col_health['string_length_max'] = stringed_len.max()
            col_health['string_length_median'] = stringed_len.median()
            col_health['string_empty_count'] = sum(stringed_len == 0)
        
        health_report[col] = col_health
        
    keys = list(health_report[col].keys())
    health_report_df = pd.DataFrame(health_report).T[keys]
    
    if norm:
        count_columns = [c for c in health_report_df.columns if '_count' in c]
        for col in count_columns:
            health_report_df[col] = health_report_df[col] / n_rows
    
    if report:
        print(health_report_df)
    
    return health_report_df

def print_counter_extremes(counter, n=20, low_pass=5, order_low_counts=False):
    """print_counter_extremes
    Prints the top most common elements and a the least common elements
    from a Counter object.
    
    Args:
    counter (collections.Counter):
    n (int): The number of elements to print. Will print n most common and
        n least common. Defaults to 20.
    low_pass (int): Threshold value that determines the highest possible count
        for elements that fall into the "least common" group. Defaults to 5.
    order_low_counts (bool): If True, will sort the elements with low counts
        and print the 20 most common of those. Defaults to False.
    """
    most_common = counter.most_common(n)
    low_counts = {k: v for k, v in counter.items() if v <= low_pass}
    low_count_keys_n = list(itertools.islice(low_counts, n))
    low_counts_n = [(k, low_counts[k]) for k in low_count_keys_n]
        
    max_len_high = 0
    max_len_low = 0
    for high, low in zip(most_common, low_counts_n):
        if len(high[0]) > max_len_high:
            max_len_high = len(high[0])
        if len(low[0]) > max_len_low:
            max_len_low = len(low[0])
        
    print('{:<{max_len_high}}\t{}\t{:{max_len_low}}\t{}\n'.format('Label (Common)', 'Count', 'Label (Uncommon)', 'Count',
                                                                  max_len_high=max_len_high + 2,
                                                                  max_len_low=max_len_low + 2))
    for high, low in zip(most_common, low_counts_n):
        print('{:<{max_len_high}}\t{}\t{:{max_len_low}}\t{}'.format(high[0], high[1], low[0], low[1],
                                                         max_len_high=max_len_high + 2,
                                                         max_len_low=max_len_low + 2))
    print('\n')
