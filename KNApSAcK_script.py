"""
Simple script to perform general searches on the KNApSAcK web database
http://www.knapsackfamily.com/knapsack_core/top.php by metabolite or organism.

It creates a csv file with Name, CAS ID, KNApSAcK ID, and SMILES for each compound
found by the user specified keyword. The file is saved to the current folder.

@author: Dr. Freddy Bernal
"""
# Imports
import argparse
import sys

from knapsack_np import KNApSAcKSearch


#####################
#  Argument parser  #
#####################
def arg_parser():
    script_usage = """{}""".format(sys.argv[0])

    parser = argparse.ArgumentParser(
        usage=script_usage,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('searchtype',
                        choices=['metabolite', 'organism'],
                        help='Type of search ("metabolite" or "organism").')
    parser.add_argument('-k',
                        dest='keyword',
                        help='Term to search for (e.g. "flavones", "Bacillus").')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = arg_parser()
    collector = KNApSAcKSearch(searchtype=args.searchtype, keyword=args.keyword)
    results = collector.search()
    filename = f'results_KNApSAcK_{args.searchtype}_{args.keyword}.csv'
    results.to_csv(filename, index=False)
