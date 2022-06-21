import argparse
import sys
import os
from pathlib import Path, PureWindowsPath
from time import time
import yaml
import re


version = "0.1.0"

snakefile_path = sys.path[0].replace("\\", "/")+"/Snakefile"
# config_path = "/".join(sys.path[0].split("\\")[:-1])+"/config/config.yaml"  # Para WINDOWS
config_path = "/".join(sys.path[0].split("/")[:-1])+"/config/config.yaml"  # Para Linux
hmm_database_path = sys.path[0].replace("\\", "/")+"/Data/HMMs/After_tcoffee_UPI/"

parser = argparse.ArgumentParser(description="PDETool's main script")
parser.add_argument("-i", "--input", help = "input FASTA file containing\
                    a list of protein sequences to be analysed")
parser.add_argument("-o", "--output", help = "path for output directory")
parser.add_argument("-db", "--database", help = "path to a user defined database. Default use of in-built database")
parser.add_argument("-s", "--snakefile", help = f"user defined snakemake worflow Snakefile. Defaults to {snakefile_path}",
                    default = snakefile_path)
parser.add_argument("-t", "--threads", type = int, help = "number of threads for Snakemake to use. Defaults to 1",
                    default = 1)
parser.add_argument("-hm", "--hmm_models", type=str, help = f"path to a directory containing HMM models previously created by the user. By default\
                    PDETool uses the built-in HMMs from database in {hmm_database_path}")
parser.add_argument("--concat_hmm_models", action = "store_true", default = False, help = "concatenate HMM models into a single file")
parser.add_argument("--unlock", action = "store_true", default = False, help = "could be required after forced workflow termination")
parser.add_argument("-w", "--workflow", default = "annotation", help = 'defines the workflow to follow, \
                    between "annotation" and "database_construction". Defaults to "annotation"')
parser.add_argument("-c", "--config_file", help = f"user defined config file. Only recommended for\
                    advanced users. Defaults to {config_path}. If given, overrides config file construction\
                    from input", default = config_path)
parser.add_argument("-v", "--version", action = "version", version = "PDETool {}".format(version))
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
    """Given a FASTA file, returns the IDs from all sequences in that file.

    Args:
        filename (str): Name of FASTA file

    Returns:
        list: A list containing IDs from all sequences
    """
    unip_IDS = []
    with open(filename, "r") as f:
        try:
            Lines = f.readlines()
            for line in Lines:
                if line.startswith(">"):
                    identi = re.findall("\|.*\|", line)
                    identi = re.sub("\|", "", identi[0])
                    unip_IDS.append(identi)
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
    """Given a input file, output directory, and a name to assign to the new config file, write that same config file
    accordingly to the given arguments

    Args:
        input_file (str): Name for the input FASTA file
        out_dir (str): Name for the output directory where result shall be directed
        config_filename (str): Name to be given to the new config file

    Returns:
        yaml: Returns a .yaml format config file, with the given arguments though the CLI
    """
    seq_IDS = parse_fasta(input_file)
    results_dir = get_results_directory()
    results_dir += "/" + out_dir
    results_dir = results_dir.replace("\\", "/")
    dict_file = {"seqids": seq_IDS,
                "output_directory": results_dir,
                "threads": args.threads,
                "workflow": args.workflow}
    caminho = "/".join(config_path.split("/")[:-1]) + "/" + config_filename
    with open(caminho, "w") as file:
        document = yaml.dump(dict_file, file)
    return document


def file_generator(path: str) -> str:
    """Function that yield the name of all and only files inside a directory in the given path, for iteration purposes
    Args:
        path (str): Path for the folder to be analyzed

    Yields:
        str: Yield the name of each file inside the given directory
    """

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


hmm_database_path = sys.path[0].replace("\\", "/")+"/Data/HMMs/After_tcoffee_UPI/"


from scripts.hmmsearch_run import run_hmmsearch


if args.workflow == "annotation":
    print("GREAT SUCESS!!!")
    for file in file_generator(hmm_database_path):
        run_hmmsearch(args.input, file, "search" + args.input + "_" + file + ".out")

elif args.workflow == "database_construction":
    print("VERY NISEEEE!")


doc = write_config(args.input, args.output, "test.yaml")
