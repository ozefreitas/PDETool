import pandas as pd
import sys 


hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])+"/Data/HMMs/HMMsearch_results/"

def read_hmmsearch_table(path: str, format:str = "tblout", save_as_csv: bool = False) -> pd.DataFrame:
    """Function receives the path for a paseable tabular (space-delimited) file from hmmsearch execution, and processed to its conversion
    to a pandas Dataframe object.

    Args:
        path (str): Full path for the hmmsearch resulting file.
        format (str, optional): Refers to the out format from hmmsearch execution. Defaults to "tblout".
        save_as_csv (bool, optional): User option to save file in a CSV format, for more readable output. Defaults to False.

    Returns:
        pd.DataFrame: Returns a pandas Dataframe object with the headers and data from the original file.
    """
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
    if save_as_csv:
        df.to_csv(path.split(".tsv")[:-1] + ".csv")
    return df


def column_generator(column_name: str, list_columns: list) -> list:
    mapa = list(map(lambda field: (column_name, field), list_columns))
    return mapa


def get_number_hits(dataframe: pd.DataFrame) -> int:
    return dataframe.shape[0]


def get_bit_scores(dataframe: pd.DataFrame) -> pd.Series:
    return dataframe["full sequence"]["bit_score"]


def get_e_values(dataframe: pd.DataFrame) -> pd.Series: 
    return dataframe["full sequence"]["E-value"]


def get_match_IDS(dataframe: pd.DataFrame) -> pd.Series:
    return dataframe["identifier"]["target_name"]


def relevant_info_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    scores = get_bit_scores(dataframe)
    evalues = get_e_values(dataframe)
    matches = get_match_IDS(dataframe)
    return pd.concat([scores, evalues, matches], axis = 1)


def quality_check(dataframe: pd.DataFrame) -> pd.DataFrame:
    
    pass


s = read_hmmsearch_table(hmmsearch_out_folder + "test_multprofiles.tsv")
df = relevant_info_df(s)
