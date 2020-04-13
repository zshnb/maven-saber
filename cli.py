from parser import Parser
import argparse

if __name__ == '__main__':
    args_parser = argparse.ArgumentParser(description='maven dependence toolkit')
    args_parser.add_argument('-artifact', metavar='artifactId', required=True,
                             dest='artifact_id', action='store',
                             help='text maven dependence artifactId to search for')
    args_parser.add_argument('-group', metavar='groupId', required=False,
                             dest='group_id', action='store',
                             help='dependence group')
    args_parser.add_argument('-ac', dest='is_accurate', action='store_true',
                             help='whether pattern artifactId accurately')
    args_parser.add_argument('-asc', dest='is_asc', action='store_true',
                             help='sort dependence by version asc')
    args_parser.add_argument('-limit', metavar='show dependencies size', dest='limit',
                             help='show how many dependencies you want copy')

    args = args_parser.parse_args()

    dependence_parser = Parser()
    dependencies = dependence_parser.parse(artifactId=args.artifact_id,
                                           groupId=args.group_id,
                                           accurate=args.is_accurate,
                                           is_asc=args.is_asc,
                                           limit=args.limit)
    for item in dependencies:
        item.to_string()
