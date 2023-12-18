from abc_argparser import parser, Args
from typing import List
from data_parser import parse_csv, Product
import pandas as pd
from abc_table import add_total_price, add_rank, add_percent_from_total_amount, add_percent_from_total_price, assign_abc_groups

def main(abc_groups: Args): 
    print(abc_groups)
    
    print(f'Group A: {abc_groups.group_a_min} - {abc_groups.group_a_max}')
    print(f'Group B: {abc_groups.group_b_min} - {abc_groups.group_b_max}')
    print(f'Group C: {abc_groups.group_c_min} - {abc_groups.group_c_max}')
    
    products: List[Product] = parse_csv('data/products_2.csv')
    
    initial_df = pd.DataFrame.from_records(data=products, columns=Product._fields)
    
    add_total_price(initial_df)
    add_rank(initial_df)

    sorted_df_by_rank = initial_df.sort_values(by=['rank'])
    
    total_amount = initial_df['amount'].sum()
    total_price_value = initial_df['total_price'].sum()
    
    add_percent_from_total_amount(total_amount, sorted_df_by_rank)
    sorted_df_by_rank['cumulative_amount_percent'] = sorted_df_by_rank['percent_from_total_amount'].cumsum()
    
    add_percent_from_total_price(total_price_value, sorted_df_by_rank)
    sorted_df_by_rank['cumulative_price_percent'] = sorted_df_by_rank['percent_from_total_price'].cumsum()    
        
    abc_analyse = assign_abc_groups(sorted_df_by_rank, abc_groups)
    print(abc_analyse)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)