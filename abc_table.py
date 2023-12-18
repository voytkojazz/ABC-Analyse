import pandas as pd
from functools import reduce
from abc_argparser import Args
import numpy as np

round_to_two_decimals = lambda x: round(x, 2)

def get_percentage_lambda(row_name: str, total_amount: int):
    return lambda row: row[row_name] * 100 / total_amount

def get_reduced_lambda(lambdas: list):
    return lambda row: reduce(lambda x, f: f(x), lambdas, row)

def add_total_price(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['total_price'] = dataframe['amount'] * dataframe['unitprice']

def add_rank(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['rank'] = dataframe['total_price'].rank(method='min', ascending=False)

def add_percent_from_total_amount(total_amount: int, sorted_df_by_rank: pd.DataFrame): 
    lambdas = [get_percentage_lambda("amount", total_amount), round_to_two_decimals]
    sorted_df_by_rank["percent_from_total_amount"] = sorted_df_by_rank.apply(
        get_reduced_lambda(lambdas), axis=1)
    
    
def add_percent_from_total_price(total_price_value: float, sorted_df_by_rank: pd.DataFrame):
    lambdas = [get_percentage_lambda('total_price', total_price_value), round_to_two_decimals]
    sorted_df_by_rank["percent_from_total_price"] = sorted_df_by_rank.apply(
        get_reduced_lambda(lambdas), axis=1)
    
def assign_abc_groups(dataframe: pd.DataFrame, abc_groups: Args) -> pd.DataFrame:
    conditions = [
        (dataframe['cumulative_price_percent'] <= abc_groups.group_a_max),
        (dataframe['cumulative_price_percent'] > abc_groups.group_a_max) & (dataframe['cumulative_price_percent'] <= (abc_groups.group_a_max + abc_groups.group_b_max)),
        (dataframe['cumulative_price_percent'] > (abc_groups.group_a_max + abc_groups.group_b_max))
    ]

    choices = ['A', 'B', 'C']

    dataframe['abc_group'] = np.select(conditions, choices, default='C')

    return dataframe