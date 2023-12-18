from abc_argparser import parser, Args
from typing import List
from data_parser import parse_csv, Product
import pandas as pd
from abc_table import add_total_price, add_rank, add_percent_from_total_amount, add_percent_from_total_price, assign_abc_groups, sort_by_rank, add_cumulative_amount_percent, add_cumulative_price_percent

def main(abc_groups: Args): 
    print(abc_groups)
    
    print(f'Group A: {abc_groups.group_a_min} - {abc_groups.group_a_max}')
    print(f'Group B: {abc_groups.group_b_min} - {abc_groups.group_b_max}')
    print(f'Group C: {abc_groups.group_c_min} - {abc_groups.group_c_max}')
    
    products: List[Product] = parse_csv('data/products_2.csv')
    
    df = pd.DataFrame.from_records(data=products, columns=Product._fields)
    
    add_total_price(df)
    add_rank(df)
    df = sort_by_rank(df)
    
    total_amount = df['amount'].sum()
    total_price_value = df['total_price'].sum()
    
    add_percent_from_total_amount(total_amount, df)
    add_cumulative_amount_percent(df)
    
    add_percent_from_total_price(total_price_value, df)
    add_cumulative_price_percent(df)
        
    abc_analyse = assign_abc_groups(df, abc_groups)
    print(abc_analyse)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)