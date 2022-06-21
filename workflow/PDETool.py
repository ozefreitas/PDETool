import numpy as np
import argparse
import sys
import os
from time import time
import yaml


version = "0.1.0"
snakefile_path = sys.path[0].replace("\\", "/")+"/Snakefile"
config_path = "/".join(sys.path[0].split("\\")[:-1])+"/config/config.yaml"

parser = argparse.ArgumentParser(description="PDETool's main script")
parser.add_argument("-i", "--input", help="input FASTA file containing\
                    a list of protein sequences to be analysed")
parser.add_argument("-o", "--output", help="path for output directory")
parser.add_argument("-db", "--database", help="path to a user defined database. Default use of in-built database")
parser.add_argument("-s", "--snakefile", help=f"user defined snakemake worflow Snakefile. Defaults to {snakefile_path}",
                    default=snakefile_path)
parser.add_argument("-c", "--config_file", help=f"user defined config file. Only recommended for\
                    advanced users. Defaults to {config_path}", default=config_path)
parser.add_argument("-v", "--version", action="version", version="PDETool {}".format(version))
args = parser.parse_args()
# print(vars(args))


