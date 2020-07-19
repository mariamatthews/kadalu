"""
'install' subcommand for kubectl-kadalu CLI tool
"""
#To prevent Py2 to interpreting print(val) as a tuple.
from __future__ import print_function

import utils

def set_args(name, subparsers):
    """ add arguments to argparser """
    parser = subparsers.add_parser(name)
    arg = parser.add_argument

    arg(
        "--version",
        help="Kadalu Version to Install [default: latest]",
        choices=["0.7.0", "master", "latest"],
        default="latest"
    )
    arg(
        "--type",
        help="Type of installation - k8s/openshift [default: kubernetes]",
        choices=["openshift", "kubernetes", "microk8s", "rke"],
        default="kubernetes"
    )
    arg(
        "--local-yaml",
        help="local operator yaml file path"
    )
    utils.add_global_flags(parser)


def validate(_args):
    """No validation available"""
    return


def run(args):
    """ perform install subcommand """
    operator_file = args.local_yaml
    if not operator_file:
        file_url = "https://raw.githubusercontent.com/kadalu/kadalu/master/manifests"
        version = ""
        insttype = ""

        if args.version and args.version != "latest":
            version = "-%s" % args.version

            if args.type and args.type == "openshift":
                insttype = "-openshift"

        operator_file = "%s/kadalu-operator%s%s.yaml" % (file_url, insttype, version)

    try:
        cmd = [utils.KUBECTL_CMD, "apply", "-f", operator_file]
        print("Executing '%s'" % cmd)
        resp = utils.execute(cmd)
        print("Kadalu operator create request sent successfully")
        print(resp.stdout)
        print()
    #noqa #pylint : disable=R0801
    except utils.CommandError as err:
        utils.command_error(cmd, err.stderr)
