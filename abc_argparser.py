from argparse import ArgumentParser
from typing import TypedDict

class Args(TypedDict):
    group_a_min: int
    group_a_max: int
    group_b_min: int
    group_b_max: int
    group_c_min: int
    group_c_max: int

parser = ArgumentParser(description='Makes an ABC Analysis')
    
parser.add_argument('--group_a_min', type=int, default=75, help='Group A Min Percentage')
parser.add_argument('--group_a_max', type=int, default=80, help='Group A Max Percentage')
    
parser.add_argument('--group_b_min', type=int, default=10, help='Group B Min Percentage')
parser.add_argument('--group_b_max', type=int, default=15, help='Group B Max Percentage')
    
parser.add_argument('--group_c_min', type=int, default=5, help='Group C Min Percentage')
parser.add_argument('--group_c_max', type=int, default=10, help='Group C Max Percentage')