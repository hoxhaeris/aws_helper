# AWS Helper

Small helper script to get the AWS IP ranges, and filter those. 

    optional arguments:
      -h, --help            show this help message and exit
      -f FILTERS, --filters FILTERS
                            Define Custom filters. To get the list of possible keys, use the --get_available_filters option. Use this format for the filter:
                            --filters service=S3,region=eu-central-1. Mind the spaces in the input string, use quotes when applicable
      --get_available_keys_for_filter GET_AVAILABLE_KEYS_FOR_FILTER
                            List all available AWS services from which you can filter
      --get_available_filters
                            List all available AWS possible keys per filter, that you can choose from
      -p, --print_selected_range
                            Print the selected IP range in stdout, instead of writing it to a file(default)
      --file FILE           The file you want the result to be writen to. By default, it will use the current directory
