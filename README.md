# AWS Helper

Small helper script to get the AWS IP ranges, and filter with any key. 

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

To get the available filters, use the --get_available_filters option:

    python3 get_aws_range.py --get_available_filters
    [
        "ip_prefix",
        "region",
        "service",
        "network_border_group"
    ]
    
    
To get the avaiable key per filter, use the --get_available_keys_for_filter option:

    python3 get_aws_range.py --get_available_keys_for_filter service
    [
        "KINESIS_VIDEO_STREAMS",
        "CLOUDFRONT",
        "S3",
        "WORKSPACES_GATEWAYS",
        "CODEBUILD",
        "ROUTE53_HEALTHCHECKS_PUBLISHING",
        "AMAZON_CONNECT",
        "AMAZON",
        "GLOBALACCELERATOR",
        "ROUTE53_HEALTHCHECKS",
        "API_GATEWAY",
        "EC2",
        "CHIME_VOICECONNECTOR",
        "EC2_INSTANCE_CONNECT",
        "CLOUD9",
        "ROUTE53",
        "CHIME_MEETINGS",
        "AMAZON_APPFLOW",
        "DYNAMODB"
    ]

Example usage:

    python3 get_aws_range.py --filters service=S3,region=eu-central-1
    
 By default, this will create a file in the run directory ('aws_range_service_S3_region_eu-central-1' in this case). The file path/name can be modified by the -f option.
 
 To print the result to stdout, use the -p option:
 
    python3 get_aws_range.py --filters service=S3,region=eu-central-1 -p
    52.219.168.0/24
    3.5.136.0/22
    52.219.72.0/22
    52.219.44.0/22
    52.219.140.0/24
    54.231.192.0/20
    3.5.134.0/23
