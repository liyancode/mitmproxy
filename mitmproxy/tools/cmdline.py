import argparse
import os

from mitmproxy import options
from mitmproxy import version


CONFIG_PATH = os.path.join(options.CA_DIR, "config.yaml")


def common_options(parser, opts):
    parser.add_argument(
        '--version',
        action='store_true',
        dest='version',
    )
    parser.add_argument(
        '--shortversion',
        action='version',
        help="show program's short version number and exit",
        version=version.VERSION
    )
    parser.add_argument(
        '--options',
        action='store_true',
        help="Dump all options",
    )
    parser.add_argument(
        "--conf",
        type=str, dest="conf", default=CONFIG_PATH,
        metavar="PATH",
        help="Read options from a configuration file"
    )
    parser.add_argument(
        "--set",
        type=str, dest="setoptions", default=[],
        action="append",
        metavar="option[=value]",
        help="""
            Set an option. When the value is omitted, booleans are set to true,
            strings and integers are set to None (if permitted), and sequences
            are emptied.
        """
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true", dest="quiet",
        help="Quiet."
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_const", dest="verbose", const=3,
        help="Increase log verbosity."
    )

    # Basic options
    opts.make_parser(parser, "mode", short="m")
    opts.make_parser(parser, "anticache")
    opts.make_parser(parser, "showhost")
    opts.make_parser(parser, "rfile", metavar="PATH", short="r")
    opts.make_parser(parser, "scripts", metavar="SCRIPT", short="s")
    opts.make_parser(parser, "stickycookie", metavar="FILTER")
    opts.make_parser(parser, "stickyauth", metavar="FILTER")
    opts.make_parser(parser, "streamfile", metavar="PATH", short="w")
    opts.make_parser(parser, "anticomp")

    # Proxy options
    group = parser.add_argument_group("Proxy Options")
    opts.make_parser(group, "listen_host", metavar="HOST")
    opts.make_parser(group, "listen_port", metavar="PORT", short="p")
    opts.make_parser(group, "server", short="n")
    opts.make_parser(group, "ignore_hosts", metavar="HOST")
    opts.make_parser(group, "tcp_hosts", metavar="HOST")
    opts.make_parser(group, "upstream_auth", metavar="USER:PASS")
    opts.make_parser(group, "proxyauth", metavar="SPEC")
    opts.make_parser(group, "rawtcp")

    # Proxy SSL options
    group = parser.add_argument_group("SSL")
    opts.make_parser(group, "certs", metavar="SPEC")
    opts.make_parser(group, "ssl_insecure", short="k")

    # Client replay
    group = parser.add_argument_group("Client Replay")
    opts.make_parser(group, "client_replay", metavar="PATH", short="C")

    # Server replay
    group = parser.add_argument_group("Server Replay")
    opts.make_parser(group, "server_replay", metavar="PATH", short="S")
    opts.make_parser(group, "replay_kill_extra")
    opts.make_parser(group, "server_replay_nopop")

    # Replacements
    group = parser.add_argument_group("Replacements")
    opts.make_parser(group, "replacements", metavar="PATTERN", short="R")
    opts.make_parser(group, "replacement_files", metavar="PATTERN")

    # Set headers
    group = parser.add_argument_group("Set Headers")
    opts.make_parser(group, "setheaders", metavar="PATTERN", short="H")


def mitmproxy(opts):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    common_options(parser, opts)

    opts.make_parser(parser, "console_eventlog")
    group = parser.add_argument_group(
        "Filters",
        "See help in mitmproxy for filter expression syntax."
    )
    opts.make_parser(group, "intercept", metavar="FILTER")
    opts.make_parser(group, "filter", metavar="FILTER")
    return parser


def mitmdump(opts):
    parser = argparse.ArgumentParser(usage="%(prog)s [options] [filter]")

    common_options(parser, opts)
    opts.make_parser(parser, "flow_detail", metavar = "LEVEL")
    parser.add_argument(
        'filter_args',
        nargs="...",
        help="""
            Filter view expression, used to only show flows that match a certain
            filter. See help in mitmproxy for filter expression syntax.
        """
    )
    return parser


def mitmweb(opts):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    group = parser.add_argument_group("Mitmweb")
    opts.make_parser(group, "web_open_browser")
    opts.make_parser(group, "web_port", metavar="PORT")
    opts.make_parser(group, "web_iface", metavar="INTERFACE")

    common_options(parser, opts)
    group = parser.add_argument_group(
        "Filters",
        "See help in mitmproxy for filter expression syntax."
    )
    opts.make_parser(group, "intercept", metavar="FILTER")
    return parser
