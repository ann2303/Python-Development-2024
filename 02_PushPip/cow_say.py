import argparse
import cowsay
import sys
import os

argmap = {
    "e": "eyes",
    "T": "tongue",
    "W": "width",
    "n": "wrap_text",
    "f": "cow",
}
preset_options = ["b", "d", "g", "p", "s", "t", "w", "y"]

parser = argparse.ArgumentParser(description="Cowsay on Python")
parser.add_argument(
    "-l", help="List all cowfiles on the current COWPATH", action="store_true"
)
parser.add_argument("-e", help="A custom eye string")
parser.add_argument("-T", help="A custom tonque string")
parser.add_argument(
    "-f",
    help="A particular cow picture file (''cowfile'') to use. If the cowfile spec contains '/' then it will be interpreted as a path relative to the current directory. Otherwise, cowsay will search the path specified in the COWPATH environment variable.",
)
parser.add_argument("-W", help="Width", type=int)
parser.add_argument(
    "-n",
    help="If it is specified, the given message will not be word-wrapped.",
    action="store_true",
)
parser.add_argument("-b", help="Borg mode", action="store_true")
parser.add_argument(
    "-d", help="Causes the cow to appear dead", action="store_true"
)
parser.add_argument("-g", help="greedy mode", action="store_true")
parser.add_argument(
    "-p",
    help="Causes a state of paranoia to come over the cow",
    action="store_true",
)
parser.add_argument(
    "-s", help="Makes the cow appear thoroughly stoned", action="store_true"
)
parser.add_argument("-t", help="Yields a tired cow", action="store_true")
parser.add_argument("-w", help="Wired mode", action="store_true")
parser.add_argument(
    "-y", help="Brings on the cow's youthful appearance", action="store_true"
)

args = parser.parse_args()
if args.l:
    cowpath = os.getenv("COWPATH")
    if cowpath:
        print(cowsay.list_cows(cowpath))
    else:
        print(cowsay.list_cows())
    exit(0)

message = sys.stdin.read()
preset = "".join([i for i in preset_options if args.__getattribute__(i)])
func_args = {}
for arg in argmap:
    if args.__getattribute__(arg):
        func_args[argmap[arg]] = args.__getattribute__(arg)

print(cowsay.cowsay(message=message, preset=preset, **func_args))
