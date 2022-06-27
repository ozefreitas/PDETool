from asyncore import read
import pandas as pd
import sys 


hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])+"/Data/HMMs/HMMsearch_results/"

#handle = pd.read_csv(hmmsearch_out_folder + "test_multprofiles.tsv", header = 1, sep = " ")
# print(handle)

def read_hmmsearch_table(path):
    dados, first_header, second_header = [], [], []
    with open(path, "r") as f:
        for line in f.readlines():
            if line.startswith("#  -") or line.startswith("# "):
                continue
            elif line.startswith("# target name"):
                second_header.append(line)
            else:
                line = line.strip().split(" ")
                linha = []
                for char in line:
                    if char != "":
                        linha.append(char)
                dados.append(linha)
    for entry in range(len(dados)):
        dados[entry] = " ".join(dados[entry])
    df = pd.DataFrame(dados)
    return df, first_header, second_header


def get_bit_scores(dataframe):
    scores = dataframe.iloc["score"]


s, d, e = read_hmmsearch_table(hmmsearch_out_folder + "test_multprofiles.tsv")
print(s)