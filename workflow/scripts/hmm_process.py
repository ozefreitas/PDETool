import pandas as pd
import sys 


hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])+"/Data/HMMs/HMMsearch_results/"

def read_hmmsearch_table(path: str, format:str = "tblout", save_as_csv: bool = False) -> pd.DataFrame:
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
    dados.pop()
    lst = []
    for char in first_header[0].strip().split(" "):
        if char != "#" and char != "":
            lst.append(char)
    first_header.clear()
    for char in " ".join(lst).split("-"):
        if char != "" and char != " ":
            first_header.append(char.strip())
    first_header.insert(0, "identifier")
    first_header.append("descriptions")
    for entry in range(len(dados)):
        dados[entry] = dados[entry][:index] + [" ".join(dados[entry][index:])]
    second_header = [["target_name", "target_accession_number", "query_name", "query_accession_number"], 
                    ["E-value", "bit_score", "bias"], 
                    ["E-value", "bit_score", "bias"],
                    ["exp", "reg", "clu", "ov", "env", "dom", "rep", "inc"],
                    ["description of target"]]
    colunas = []
    for i in range(len(first_header)):
        mapa = column_generator(first_header[i], second_header[i])
        colunas += mapa
    df = pd.DataFrame(dados)
    df.columns = pd.MultiIndex.from_tuples(colunas)
    return df, colunas


def column_generator(column_name: str, list_columns: list) -> list:
    mapa = list(map(lambda field: (column_name, field), list_columns))
    return mapa


def get_bit_scores(dataframe: pd.DataFrame) -> pd.Series:
    scores = dataframe["full sequence"]["bit_score"]
    return scores


def get_e_values(dataframe: pd.DataFrame) -> pd.Series:
    e_value = dataframe["full sequence"]["E-value"]
    return e_value


def get_match_IDS(dataframe: pd.DataFrame) -> pd.Series:
    matches = dataframe["identifier"]["target_name"]
    return matches


def relevant_info_df():
    pass


s, d = read_hmmsearch_table(hmmsearch_out_folder + "test_multprofiles.tsv")
print(s["full sequence"]["E-value"])