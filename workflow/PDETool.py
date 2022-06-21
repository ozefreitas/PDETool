import argparse
import sys
import os
from pathlib import Path, PureWindowsPath
from time import time
import yaml
import re


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
parser.add_argument("-w", "--worflow", default = "annotation", help='defines the workflow to follow, \
                    between "annotation" and "database construction". Defaults to "annotation"')
parser.add_argument("-c", "--config_file", help=f"user defined config file. Only recommended for\
                    advanced users. Defaults to {config_path}. If given, overrides config file construction\
                    from input", default=config_path)
parser.add_argument("-v", "--version", action="version", version="PDETool {}".format(version))
args = parser.parse_args()
print(vars(args))


def read_config_yaml(filename: str) -> tuple:
    config_type = filename.split(".")[-1]
    if config_type == "yaml":
        with open(filename) as stream:
            try:
                config_file = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        quit("Config file must be in .yaml format.")
    return config_file, config_type


def parse_fasta(filename: str) -> list:
    unip_IDS = []
    with open(filename, "r") as f:
        try:
            Lines = f.readlines()
            for line in Lines:
                if line.startswith(">"):
                    identi = re.findall("\|.*\|", line)
                    IDS = re.sub("\|", "", identi[0])
                    unip_IDS.append(IDS)
        except:
            quit("File must be in FASTA format.")
    return unip_IDS


def get_results_directory() -> str:
    """Automatically return the path where output should appear. It must climb up one folder till PDETool folder, 
    and go back to results

    Returns:
        str: Path for the output folder
    """
    p = Path(sys.path[0])
    return str(p.parents[0] / "results")


def write_config(input_file: str, out_dir: str, config_filename: str) -> yaml:
    seq_IDS = parse_fasta(input_file)
    results_dir = get_results_directory()
    results_dir += "/" + out_dir
    results_dir = results_dir.replace("\\", "/")
    dict_file = {"seqids": seq_IDS,
                "output_directory": results_dir}
    with open(config_filename, "w") as file:
        document = yaml.dump(dict_file, file)
    return document


# file ,form = read_config_yaml(args.config_file)
# print(file, form)
# identificadores_FASTA = parse_fasta(args.input)
# print(identificadores_FASTA)
doc = write_config(args.input, args.output, "test.yaml")