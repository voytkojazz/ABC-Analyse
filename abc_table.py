import pandas as pd
from functools import reduce
from abc_argparser import Args
import numpy as np

round_to_two_decimals = lambda x: round(x, 2)

def get_percentage_lambda(row_name: str, total_amount: int):
    return lambda row: row[row_name] * 100 / total_amount


def get_reduced_lambda(lambdas: list):
    return lambda row: reduce(lambda x, f: f(x), lambdas, row)


class ABCAnalizer: 
    
    """Class for ABC Analysis"""

    def __init__(self, dataframe: pd.DataFrame, abs_groups: Args) -> None:
        '''Constructor for this class.'''
        self.df = dataframe
        self.abc_groups = abs_groups
        self.total_amount = self.df['amount'].sum()

    def analyze(self):
        return self._add_total_price()._add_rank()._sort_by_rank()._add_percent_from_total_amount()._add_cumulative_amount_percent()._add_percent_from_total_price()._add_cumulative_price_percent()._assign_abc_groups().df
        
    def _add_total_price(self):
        '''Adds total price for every product to dataframe.'''
        self.df['total_price'] = self.df['amount'] * self.df['unitprice']
        self.total_price_value = self.df['total_price'].sum()
        return self
    
    def _add_rank(self):
        '''ranks products by total price.'''
        self.df['rank'] = self.df['total_price'].rank(method='min', ascending=False)
        return self
    
    def _sort_by_rank(self):
        '''Sorts dataframe by rank.'''
        self.df = self.df.sort_values(by=['rank'])
        return self
    
    def _add_percent_from_total_amount(self):
        '''Adds percent from total amount for every product to dataframe.'''
        lambdas = [get_percentage_lambda("amount", self.total_amount), round_to_two_decimals]
        self.df["percent_from_total_amount"] = self.df.apply(
            get_reduced_lambda(lambdas), axis=1)
        return self
    
    def _add_cumulative_amount_percent(self):
        '''Adds cumulative amount percent for every product to dataframe.'''
        self.df['cumulative_amount_percent'] = self.df['percent_from_total_amount'].cumsum()
        return self
    
    def _add_percent_from_total_price(self):
        lambdas = [get_percentage_lambda('total_price', self.total_price_value), round_to_two_decimals]
        self.df["percent_from_total_price"] = self.df.apply(
            get_reduced_lambda(lambdas), axis=1)
        return self
    
    def _add_cumulative_price_percent(self):
        self.df['cumulative_price_percent'] = self.df['percent_from_total_price'].cumsum()
        return self
    
    def _assign_abc_groups(self):
        conditions = [
            (self.df['cumulative_price_percent'] <= self.abc_groups.group_a_max),
            (self.df['cumulative_price_percent'] > self.abc_groups.group_a_max) 
            & (self.df['cumulative_price_percent'] <= (self.abc_groups.group_a_max + self.abc_groups.group_b_max)),
            (self.df['cumulative_price_percent'] > (self.abc_groups.group_a_max + self.abc_groups.group_b_max))
        ]

        choices = ['A', 'B', 'C']

        self.df['abc_group'] = np.select(conditions, choices, default='C')
        return self
    
    