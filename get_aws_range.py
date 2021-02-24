import argparse
import json
import requests


def parse_filters():
    class ParseFilterString(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            filters = values.split(',')
            filters_dict = {}
            for input_filter in filters:
                filters_dict.setdefault(input_filter.split('=')[0])
                filters_dict[input_filter.split('=')[0]] = input_filter.split('=')[1]
            values = filters_dict
            setattr(args, self.dest, values)

    return ParseFilterString


def cli_parser():
    my_parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    my_parser.add_argument('-f', '--filters',
                           type=str,
                           help='Define Custom filters. To get the list of possible keys, use the '
                                '--get_available_filters option. Use this format for the filter: --filters '
                                'service=S3,region=eu-central-1. Mind the spaces in the input string, use quotes when '
                                'applicable',
                           action=parse_filters(),
                           default={})
    my_parser.add_argument('--get_available_keys_for_filter',
                           help='List all available AWS services from which you can filter',
                           default=None)
    my_parser.add_argument('--get_available_filters',
                           help='List all available AWS possible keys per filter, that you can choose from',
                           action="store_true")
    my_parser.add_argument('-p', '--print_selected_range',
                           help='Print the selected IP range in stdout, instead of writing it to a file(default)',
                           action="store_true")
    my_parser.add_argument('--file',
                           type=str,
                           help='The file you want the result to be writen to. By default, it will use the current '
                                'directory',
                           default=None)
    args = my_parser.parse_args()
    return args


class AWSRanges:
    def __init__(self,
                 cli_filters: dict = None,
                 url: str = "https://ip-ranges.amazonaws.com/ip-ranges.json"
                 ):
        self.url = url
        self.cli_filters = cli_filters

    def get_range(self):
        data = requests.get(url=self.url)
        return data.json()['prefixes']

    def get_available_keys_per_filter(self, filter_key):
        service_set = set()
        for key in self.get_range():
            service_set.add(key[filter_key])
        return list(service_set)

    def get_available_filters(self):
        filters_set = []
        for prefix in self.get_range():
            for key in prefix:
                filters_set.append(key)
            break
        return filters_set

    def filter_range(self):
        for aws_range in self.get_range():
            include_range = True
            for filter_key, value in self.cli_filters.items():
                if not aws_range[filter_key] == value:
                    include_range = False
            if include_range is True:
                yield aws_range

    def range_to_ip_prefix(self):
        return (key['ip_prefix'] for key in self.filter_range())

    def write_to_file(self, object_to_write=None, file: str = None):
        if object_to_write is None:
            object_to_write = self.range_to_ip_prefix()
        if file is None:
            name_string = ""
            for key, value in self.cli_filters.items():
                name_string = f"{name_string}_{key}_{value}"
            file = f"aws_range{name_string}"
        with open(file, 'w') as f:
            for entry in object_to_write:
                f.write(entry)
                f.write('\n')


if __name__ == "__main__":
    cli_args = cli_parser()
    aws_range_to_route = AWSRanges(cli_filters=cli_args.filters)
    if cli_args.get_available_keys_for_filter is not None:
        print(json.dumps(
            aws_range_to_route.get_available_keys_per_filter(filter_key=cli_args.get_available_keys_for_filter),
            indent=4))
        exit(0)
    if cli_args.print_selected_range is True:
        for i in aws_range_to_route.range_to_ip_prefix():
            print(i)
        exit(0)
    if cli_args.get_available_filters is True:
        print(json.dumps(aws_range_to_route.get_available_filters(), indent=4))
    aws_range_to_route.write_to_file(file=cli_args.file)
