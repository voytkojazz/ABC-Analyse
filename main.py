from abc_argparser import parser, Args
from typing import List
from data_parser import parse_csv, Product
import pandas as pd
from abc_table import ABCAnalizer

def main(abc_groups: Args): 
    print(abc_groups)
    
    print(f'Group A: {abc_groups.group_a_min} - {abc_groups.group_a_max}')
    print(f'Group B: {abc_groups.group_b_min} - {abc_groups.group_b_max}')
    print(f'Group C: {abc_groups.group_c_min} - {abc_groups.group_c_max}')
    
    products: List[Product] = parse_csv('data/products_2.csv')
    df = pd.DataFrame.from_records(data=products, columns=Product._fields)
    analyzer = ABCAnalizer(df, abc_groups)
    result = analyzer.analyze()
    print(result)
    


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)