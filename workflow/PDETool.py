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
parser.add_argument("-o", "--output", type=str, help="path for output directory")
parser.add_argument("-db", "--database", type=str, help="path to a user defined database")
parser.add_argument("-hm", "--hmm_models", type=str, help="path to a directory containing HMM models previously created by the user")
parser.add_argument("--concat_hmm_models", action="store_true", default=False, help="concatenate HMM models into a single file")
parser.add_argument("-s", "--snakefile", type=str, help="user defined snakemake worflow Snakefile. Defaults to {}".format(snakefile_path),
                    default=snakefile_path)
parser.add_argument("-c", "--config_file", type=str, help="user defined config file.Defaults to {}".format(config_path), default=config_path)
parser.add_argument("-v", "--version", action="version", version="PDETool {}".format(version))
args = parser.parse_args()

