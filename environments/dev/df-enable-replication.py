import getopt
import json
import os
import requests
import sys

def print_help():
    print("""
Usage: cloudability_setup.py [options]

cloudability_setup -- Register new account with Cloudability

Options:
  -h, --help            Show this help message and exit
  -a <acct #>, --acctnum=<acct #>
                        Required argument: IaaS Account Number
  -t <type>, --type=<type>
                        Required argument: IaaS Account Type
""")


def enable_replication_data_fusion(project_name, location, instance_name, access_token):

    url = 'https://datafusion.googleapis.com/v1/projects/' + project_name + '/locations/' + location + '/instances/' + instance_name
    headers = {'Authorization': 'Bearer ' + access_token}
    data = '{ "accelerators":[{"accelerator_type":"CDC", "state":"ENABLED"}]}'

    response = requests.patch(url, headers=headers, data=data)

    if response.status_code == requests.codes.ok:
      sys.exit()

    else:
      print("Bad response from Cloudability API while updating account.")
      print("HTTP: " + str(response.status_code))
      sys.exit(3)


def main(argv=None):
    '''
    Main function: work with command line options and send an HTTPS request to the Google API.
    '''

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:l:i:t:',
                                   ['help', 'proj=', 'loc=', 'instance=', 'token='])
    except getopt.GetoptError as err:
        # Print help information and exit:
        print(str(err))
        print_help()
        sys.exit(2)

    # Initialize parameters
    project_name = None
    location = None
    instance_name = None
    access_token = None

    # Parse command line options
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            sys.exit()
        elif opt in ('-p', '--proj'):
            project_name = arg
        elif opt in ('-l', '--loc'):
            location = arg
        elif opt in ('-i', '--instance'):
            instance_name = arg
        elif opt in ('-t', '--token'):
            access_token = arg

    print(f">>> project_name={project_name}")
    print(f">>> location={location}")
    print(f">>> instance_name={instance_name}")
    print(f">>> access_token={access_token}")

    # Enforce required arguments
    if not project_name or not location or not instance_name or not access_token:
      print_help()
      sys.exit(4)

    enable_replication_data_fusion(project_name, location, instance_name, access_token)


if __name__ == '__main__':
    sys.exit(main())