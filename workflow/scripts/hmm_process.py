from asyncore import read
import pandas as pd
import sys 


hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])+"/Data/HMMs/HMMsearch_results/"

#handle = pd.read_csv(hmmsearch_out_folder + "test_multprofiles.tsv", header = 1, sep = " ")
# print(handle)

def read_hmmsearch_table(path, format = "tblout"):
    index = {"tblout": 18}[format]
    dados, first_header, second_header = [], [], []
    with open(path, "r") as f:
        for line in f.readlines():
            if line.startswith("#  -"):
                continue
            elif line.startswith("# target name"):
                second_header.append(line)
            elif line.startswith("# "):
                first_header.append(line)
            else:
                line = line.strip().split(" ")
                linha = []
                for char in line:
                    if char != "":
                        linha.append(char)
                dados.append(linha)
    first_header = first_header[0].strip().split(" ")
    lst = []
    for char in first_header:
        if char != "#" and char != "" and "-" not in char:
            lst.append(char)
    first_header = lst
    for entry in range(len(dados)):
        dados[entry] = dados[entry][:index] + [" ".join(dados[entry][index:])]
    
    df = pd.DataFrame(dados)
    return df, columns


def column_generator(column_name, list_columns):
    mapa = list(map(lambda field: (column_name, field), list_columns))
    return mapa


def get_bit_scores(dataframe):
    scores = dataframe.iloc["score"]


s, d = read_hmmsearch_table(hmmsearch_out_folder + "test_multprofiles.tsv")
print(d)