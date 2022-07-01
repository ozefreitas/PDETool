from concurrent.futures import process
import pandas as pd
import sys 


hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/"))+"/Data/HMMs/HMMsearch_results/"
# Para testar em raw python
# hmmsearch_out_folder = "/".join(sys.path[0].replace("\\", "/").split("/")[:-1])+"/Data/HMMs/HMMsearch_results/"

def read_hmmsearch_table(path: str, format: str = "tblout", save_as_csv: bool = False) -> pd.DataFrame:
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
            if line.startswith("#  -") or line.startswith("#-"):
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
    """Maps the main header (column name) with the second headers (list_columns) to be added to a Dataframe as a MultiIndex

    Args:
        column_name (str): Name for the main name for the set of underlying columns
        list_columns (list): Name for the underlying columns

    Returns:
        list: Returns a list of tuples in the form of (first header, second header)
    """
    mapa = list(map(lambda field: (column_name, field), list_columns))
    return mapa


def get_number_hits(dataframe: pd.DataFrame) -> int:
    """Given a Dataframe with data from hmmsearch execution (post processed into a pd.Dataframe), returns the number of hits against the models.

    Args:
        dataframe (pd.DataFrame): A processed txt file resulting from hmmsearch into pandas dataframe.

    Returns:
        int: Number of hits given by hmmsearch.
    """
    return dataframe.shape[0]


def get_bit_scores(dataframe: pd.DataFrame, to_list:bool = False) -> pd.Series:
    """Given a Dataframe with data from hmmsearch execution (post processed into a pd.Dataframe), returns all values of bit scores.

    Args:
        to_list (bool, optional): Coverts Series values to list format. Defaults to False.
        dataframe (pd.DataFrame): A processed txt file resulting from hmmsearch into pandas dataframe.

    Returns:
        pd.Series: The column containg all bit scores.
    """
    if to_list:
        return dataframe["full sequence"]["bit_score"].tolist()
    else:
        return pd.to_numeric(dataframe["full sequence"]["bit_score"])


def get_e_values(dataframe: pd.DataFrame, to_list:bool = False) -> pd.Series:
    """Given a Dataframe with data from hmmsearch execution (post processed into a pd.Dataframe), returns all e-values.

    Args:
        to_list (bool, optional): Coverts Series values to list format. Defaults to False.
        dataframe (pd.DataFrame): A processed txt file resulting from hmmsearch into pandas dataframe.

    Returns:
        pd.Series: The column containg all e-values.
    """
    if to_list:
        return dataframe["full sequence"]["E-value"].tolist()
    else: 
        return pd.to_numeric(dataframe["full sequence"]["E-value"])


def get_match_IDS(dataframe: pd.DataFrame, to_list:bool = False, only_relevant: bool = False) -> pd.Series:
    """Given a Dataframe with data from hmmsearch execution (post processed into a pd.Dataframe), returns all Uniprot IDs from the targuet sequences 
    that gave a hit. Can also be given a dataframe after beeing cut down to only the relevant data.

    Args:
        to_list (bool, optional): Coverts Series values to list format. Defaults to False.
        dataframe (pd.DataFrame): A processed txt file resulting from hmmsearch into pandas dataframe.
        (only_relevant, optional): Set to True if given Dataframe is already in its small format. Defaults to False.

    Returns:
        pd.Series: The column containg all Uniprot IDS.
    """
    if to_list:
        if only_relevant:
            return dataframe["target_name"].tolist()
        else:
            return dataframe["identifier"]["target_name"].tolist()
    else:
        if only_relevant:
            return dataframe["target_name"]
        else:
            return dataframe["identifier"]["target_name"]


def relevant_info_df(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Concatenate all the relevant info (e-values, bit scores and targuet names) to a single Dataframe

    Args:
        dataframe (pd.DataFrame): A pandas Dataframe object with the headers and data from the original file.

    Returns:
        pd.DataFrame: A smaller Dataframe with only relevant information
    """
    scores = get_bit_scores(dataframe)
    evalues = get_e_values(dataframe)
    matches = get_match_IDS(dataframe)
    return pd.concat([scores, evalues, matches], axis = 1)


def concat_df_byrow(*dfs: pd.DataFrame, list_df: list = []) -> pd.DataFrame:
    """Given any number of pandas dataframes, concatenate them by row.

    Args:
        list_df (list): A list of pandas dataframe objects to be merged together.

    Returns:
        pd.DataFrame: A bigger (by number of indexes) Dataframe, with all hits from all given dataframes.
    """
    if list_df == []:
        list_df = [df for df in dfs]
    big_df = pd.concat(list_df, ignore_index = True, sort = False)
    return big_df


def quality_check(dataframe: pd.DataFrame, list_df: list = None, *dfs: pd.DataFrame, bit_threshold: float = 180, eval_threshold: float = 0.00001) -> pd.DataFrame:
    """Reads the full Dataframe from the complete hmmsearch run in all thresholds
    Function concat_df_byrow() can help put all Dataframes together.

    Args:
        dataframe (pd.DataFrame): A bigger (by number of indexes) Dataframe, with all hits from all given dataframes.
        list_df (list, optional): Can give a list of pandas dataframe objects to be merged together, if not done previously.
        *dfs (pd.Dataframe): Can also give any number of Dataframes, that will also be concatenated in the start of the function.

    Returns:
        pd.DataFrame: A Dataframe where it was decided in which hits were good enough to conclude whether that hit
    is going to be in the final report as to be a sequence with potential plastic degradation.
    """
    # get_bit_evalue_thresholds(bit_threshold, eval_threshold)
    if list_df:
        dataframe = concat_df_byrow(list_df = list_df)
    elif dfs:
        dataframe = concat_df_byrow(dfs=dfs)
    process_df = dataframe[(dataframe["bit_score"] >= bit_threshold) & (dataframe["E-value"] <= eval_threshold)]
    return process_df.reset_index()


def get_bit_evalue_thresholds(bit, evalue) -> tuple:
    return (bit, evalue)


# s = read_hmmsearch_table(hmmsearch_out_folder + "search_lit_sequences.fasta_60-65.hmm.tsv")
# s1 = read_hmmsearch_table(hmmsearch_out_folder + "search_lit_sequences.fasta_65-70.hmm.tsv")
# s2 = read_hmmsearch_table(hmmsearch_out_folder + "search_lit_sequences.fasta_70-75.hmm.tsv")
# df = relevant_info_df(s)
# df1 = relevant_info_df(s1)
# df2 = relevant_info_df(s1)
# print(df)
# big = concat_df_byrow(df, df1, df2)
# print(big)