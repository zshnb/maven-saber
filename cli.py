from parser import Parser
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='search maven dependence')
    parser.add_argument('-artifact', metavar='pattern', required=True,
                        dest='patterns', action='append',
                        help='text pattern to search for')

    args = parser.parse_args()
    print(args)


    # parser = Parser()
    # dependencies = parser.parse('fastjson')
    # for item in dependencies:
    #     item.to_string()
