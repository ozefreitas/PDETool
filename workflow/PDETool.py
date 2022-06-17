from ast import Str
import numpy as np
import argparse
import sys
import os
from time import time

version = "0.1.0"
snakefile_path = sys.path[0].replace("\\", "/")+"/Snakefile"
config_path = "/".join(sys.path[0].split("\\")[:-1])+"/config/config.yaml"

parser = argparse.ArgumentParser(description="PDETool's main script")
parser.add_argument("-i", "--input", type=str, help="input FASTA file containing matagenomic\
                    samples or single sequences")
parser.add_argument("-o", "--output", type=str)
parser.add_argument("-db", "--database")
parser.add_argument("-s", "--snakefile", type=str, help="user defined snakemake worflow Snakefile. Defaults to {}".format(snakefile_path),
                    default=snakefile_path)
parser.add_argument("-c", "--config_file", type=str, help="user defined config file.Defaults to {}".format(config_path))
parser.add_argument("-v", "--version", action="version", version="PDETool {}".format(version))
args = parser.parse_args()
