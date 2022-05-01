import pandas as pd

def read_clstr_file(filepath):
    clusters = pd.read_table(filepath + ".clstr", delimiter="\t")
    # fasta = 
    return clusters

def cdhit_parser(txtfile):
    file = open(txtfile, "r")
    cluster = 0
    seqs_by_cluster = {}
    Lines = file.readlines()
    for line in Lines:
        if line[0] == ">":
            seqs_by_cluster[cluster] = []
            cluster += 1
    return seqs_by_cluster