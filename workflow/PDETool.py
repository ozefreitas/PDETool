import argparse
import sys
import os
from pathlib import Path, PureWindowsPath
from time import time
from types import prepare_class
import yaml
import re
import pandas as pd
from collections import Counter
import glob
# import snakemake

from scripts.hmmsearch_run import run_hmmsearch
from scripts.hmm_process import *


version = "0.1.0"

snakefile_path = sys.path[0].replace("\\", "/")+"/Snakefile"
# config_path = "/".join(sys.path[0].split("\\")[:-1])+"/config/config.yaml"  # Para WINDOWS
config_path = "/".join(sys.path[0].split("/")[:-1])+"/config/"  # Para Linux
hmm_database_path = sys.path[0].replace("\\", "/")+"/Data/HMMs/After_tcoffee_UPI/"

parser = argparse.ArgumentParser(description="PlastEDMA's main script")
parser.add_argument("-i", "--input", help = "input FASTA file containing\
                    a list of protein sequences to be analysed")
parser.add_argument("-o", "--output", default = "PlastEDMA_results", help = "name for the output directory. Defaults to 'PlastEDMA_results'")
parser.add_argument("--output_type", default = "tsv", help = "chose report table outpt format from 'tsv', 'csv' or 'excel'. Defaults to 'tsv'")
parser.add_argument("-rt", "--report_text", default = False, action = "store_true", help = "decides wether to produce or not a friendly report in \
                    txt format with easy to read information")
parser.add_argument("--hmms_output_type", default = "out", help = "chose output type from 'out', 'tsv' ou 'pfam' format. Defaults to 'out'")
parser.add_argument("-p", "--produce_inter_tables", default = False, action = "store_true", help = "call if user wants to save intermediate\
                    tables as parseale .csv files (tables from hmmsearch results processing)")
parser.add_argument("-db", "--database", help = "path to a user defined database. Default use of in-built database")
parser.add_argument("-s", "--snakefile", help = f"user defined snakemake worflow Snakefile. Defaults to {snakefile_path}",
                    default = snakefile_path)
parser.add_argument("-t", "--threads", type = int, help = "number of threads for Snakemake to use. Defaults to 1",
                    default = 1)
parser.add_argument("-hm", "--hmm_models", type=str, help = f"path to a directory containing HMM models previously created by the user. By default\
                    PDETool uses the built-in HMMs from database in {hmm_database_path}")
parser.add_argument("--concat_hmm_models", action = "store_true", default = False, help = "concatenate HMM models into a single file")
parser.add_argument("--unlock", action = "store_true", default = False, help = "could be required after forced workflow termination")
parser.add_argument("-w", "--workflow", default = "annotation", help = 'defines the workflow to follow,\
                    between "annotation", "database_construction" and "both". Latter keyword makes the database construction\
                    first and posterior annotation. Defaults to "annotation"')
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
    try:
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
    except TypeError:
        quit("Missing input file! Make sure -i option is filled")
    return unip_IDS


def get_results_directory() -> str:
    """Automatically return the path where output should appear. It must climb up one folder till PDETool folder, 
    and go back to results

    Returns:
        str: Path for the output folder
    """
    p = Path(sys.path[0])
    return str(p.parents[0] / "results/")


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
                "input_file": args.input.split("/")[-1],
                "output_directory": results_dir,
                "out_table_format": args.output_type,
                "hmmsearch_out_type": args.hmms_output_type,
                "threads": args.threads,
                "workflow": args.workflow}
    caminho = "/".join(config_path.split("/")[:-1]) + "/" + config_filename
    with open(caminho, "w") as file:
        document = yaml.dump(dict_file, file)
    return document


def file_generator(path: str, full_path: bool = False) -> str:
    """Function that yield the name of all and only files inside a directory in the given path, for iteration purposes
    Args:
        path (str): Path for the folder to be analyzed

    Yields:
        str: Yield the name of each file inside the given directory
    """

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if full_path:
                yield os.path.join(path, file)
            else:
                yield file


def table_report(dataframe: pd.DataFrame, path: str, type_format: str):
    """Saves a table in a user specified format, with the processed and filtered information from the 
    hmmsearch execution with the HMMs against the query sequences.

    Args:
        dataframe (pd.DataFrame): Dataframe with only the relevant information from hmmsearch execution 
        for all hmm from all threshold ranges.
        path (str): output path.
        type_format (str): Specify the output format.

    Raises:
        TypeError: Raises TypeError error if user gives an unsupported output format.
    """
    pre_plastic = "PE_"
    summary_dic = {
        "querys": get_match_IDS(dataframe, to_list = True, only_relevant = True),
        "models": [pre_plastic + model for model in get_models_names(dataframe, to_list = True, only_relevant = True)],
        "bit_scores": get_bit_scores(dataframe, to_list = True, only_relevant = True),
        "e_values": get_e_values(dataframe, to_list = True, only_relevant = True)
        }
    print(summary_dic)
    df = pd.DataFrame.from_dict(summary_dic)
    table_name = "report_table." + type_format
    if type_format == "tsv":
        df.to_csv(path + table_name, sep = "\t")
    elif type_format == "csv":
        df.to_csv(path + table_name)
    elif type_format == "excel":
        df.to_excel(path + "report_table.xlsx", sheet_name = "Table_Report", index = 0)
    else:
        raise TypeError("Specified table format is not available. Read documentation for --output_type.")


def text_report(dataframe: pd.DataFrame, path: str, hmmpath: str, bit_threshold: float, eval_threshold: float):
    """Write the final report as .txt file, with a summary of the results from the annotation 
    performed with hmmsearch. Starts by calculating the number of in-built HMM profiles, and gives an insight of the 
    filtration thresholds.

    Args:
        dataframe (pd.DataFrame): Dataframe with only the relevant information from hmmsearch execution 
        for all hmm from all threshold ranges.
        path (str): output path.
    """
    number_init_hmms = 0
    for dir in os.listdir(hmmpath):
        if os.path.isdir(os.path.join(hmmpath, dir)):
            for _ in os.listdir(os.path.join(hmmpath, dir)):
                number_init_hmms += 1
    query_names = get_match_IDS(dataframe, to_list = True, only_relevant = True)
    number_hits_perseq = get_number_hits_perseq(query_names)
    unique_seqs = get_unique_hits(query_names)
    inputed_seqs = parse_fasta(args.input)
    with open(path + "test_report.txt", "w") as f:
        f.write(f"PlastEDMA hits report:\n \
                \nFrom a total number of {number_init_hmms} HMM profiles initially considered, only {len(query_names)} where considered"
                "for the final report. \nFiltering process was performed considering the values from bit score and E-value from the HMM search run,"
                f"in which the considered bit score threshold was {bit_threshold} and E-value was {eval_threshold}.\n"
                f"Also, {len(inputed_seqs)} initial query sequences where inputed form {args.input} file, from which {len(unique_seqs)} "
                f"out of these {len(inputed_seqs)} were considered to have a hit against the HMM database.")
        f.close


def get_number_hits_perseq(hit_IDs_list: list) -> dict:
    """Given a list of sequences IDs from the hits against the hmm models from hmmsearch, counts the number of each ID.

    Args:
        hit_IDs_list (list): List of sequence IDs.

    Returns:
        dict: Dictionary containing each ID as key and the respective number of occurrences as value.
    """
    counter = {}
    for i in hit_IDs_list:
        counter[i] = counter.get(i, 0) + 1
    return counter


def get_unique_hits(hit_IDs_list: list) -> list:
    """Given a list of sequence IDs from the hits against the hmm models from hmmsearch, return a new list with only the unique elements.

    Args:
        hit_IDs_list (list): List of sequence IDs.

    Returns:
        list: List with only a single occurrence of each ID.
    """
    unique_IDs_list = []
    for x in hit_IDs_list:
        if x not in unique_IDs_list:
            unique_IDs_list.append(x)
    return unique_IDs_list


def get_hit_sequences(hit_IDs_list: list, path: str, inputed_seqs: str):
    """Wirtes an ouput Fasta file with the sequences from the input files that had a hit in hmmsearch 
    annotation against the hmm models.

    Args:
        hit_IDs_list (list): list of Uniprot IDs that hit.
        path (str): ouput path.
        inputed_seqs (str): name of the initial input file.
    """
    with open(path + "aligned.fasta", "w") as wf:
        uniq_IDS = parse_fasta(inputed_seqs)
        with open(inputed_seqs, "r") as rf:
            for x in hit_IDs_list:
                if x in uniq_IDS:
                    try:
                        Lines = rf.readlines()
                        for line in Lines:
                            if x in line:
                                wf.write(line)
                                wf.write("\n")
                                continue
                            while ">" not in line:
                                wf.write(line)
                                wf.write("\n")
                    except:
                        quit("File must be in Fasta format.")


def generate_output_files(dataframe: pd.DataFrame, hit_IDs_list: list, inputed_seqs: str, bit_threshold: float, eval_threshold: float):
    """Function that initializes the output files creation simultaneously, for now, only two files are generated:
    report and aligned sequences.
    Path will always be the output folder defined by the user when running tool in CLI, so no pat argument is required.

    Args:
        dataframe (pd.DataFrame): Dataframe with only the relevant information from hmmsearch execution.
        hit_IDs_list (list): list of Uniprot IDs that hit.
        inputed_seqs (str): name of the initial input file.
    """
    out_fodler = get_results_directory() + "/" + args.output + "/"
    table_report(dataframe, out_fodler, args.output_type)
    if args.report_text:
        text_report(dataframe, out_fodler, hmm_database_path, bit_threshold, eval_threshold)
    # get_hit_sequences(hit_IDs_list, out_fodler, inputed_seqs)


doc = write_config(args.input, args.output, "test.yaml")
config, config_format = read_config_yaml(config_path + "test.yaml")

hmmsearch_results_path = sys.path[0].replace("\\", "/")+"/Data/HMMs/HMMsearch_results/"


if args.workflow == "annotation":
    print("GREAT SUCESS!!!")
    # for hmm_file in file_generator(hmm_database_path, full_path = True):
    #     run_hmmsearch(args.input, hmm_file, 
    #                 hmmsearch_results_path + "search_" + config["input_file"].split(".")[0] + "_" + hmm_file.split(".")[0] + "." + args.output_type,
    #                 out_type = args.output_type)
    lista_dataframes = []
    for file in file_generator(hmmsearch_results_path):
        print(f'File {file} detected \n')
        lista_dataframes.append(read_hmmsearch_table(hmmsearch_results_path + file))
    final_df = concat_df_byrow(list_df = lista_dataframes)
    rel_df = relevant_info_df(final_df)
    # print(rel_df)
    quality_df, bs_thresh, eval_thresh = quality_check(rel_df, give_params = True)
    hited_seqs = get_match_IDS(quality_df, to_list = True, only_relevant = True)
    # print(hited_seqs)
    generate_output_files(quality_df, hited_seqs, args.input, bs_thresh, eval_thresh)

elif args.workflow == "database_construction":
    print("VERY NISSSEEE!")

elif args.workflow == "both":
    print("DAAAAAAMMMNNN")

else:
    raise ValueError("-w worflow flag only ranges from 'annotation', 'database_construction' or 'both'. Chose one from the list.")