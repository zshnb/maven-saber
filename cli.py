from parser import Parser
import argparse

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='maven dependence toolkit')
    args_parser.add_argument('-artifact', metavar='artifactId', required=False,
                             dest='artifactId', action='store',
                             help='text maven dependence artifactId to search for')
    args_parser.add_argument('-a', dest='is_accurate', action='store_true',
                             help='whether pattern artifactId accurately')

    args = args_parser.parse_args()

    dependence_parser = Parser()
    dependencies = dependence_parser.parse(keyword=args.artifactId, accurate=args.is_accurate)
    for item in dependencies:
        item.to_string()
