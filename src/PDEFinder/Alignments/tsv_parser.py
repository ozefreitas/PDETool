import pandas as pd


def diamond_parser(filepath):
    """    Process a .tsv file from diamond tool output

    Args:
        filepath (string): name of the diamond output file in .tsv format

    Returns:
        DataFrame: A pandas dataframe with diamond documented columns names as header
    """

    # dar os nomes as colunas
    header = ["Query accession", "Target accession", "Sequence identity", 
                "Length", "Mismatches", "Gap openings", "Query start", 
                "Query end", "Target start", "Target end", "E-value", "Bit score"]

    # ler file em csv separado por tabs
    diamond_outfile = pd.read_csv(filepath, sep="\t", names=header)
    return diamond_outfile

# passar a csv
# diamond_outfile.to_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/Diamond/best_matches.csv")

def iter_per_sim(dataframe):
    """    Given a pandas DataFrame, return a dictionary with a list of sequences form the iteration of the sequence similarity between queries and database sequences.

    Args:
        dataframe (DataFrame): A pandas dataframe with diamond documented columns names as header

    Returns:
        dictionary: A dictionary where the keys are intervals of sequence similarity, and values are lists of UniProtKB queries
    """

    # selecionar colunas com perc. identity juntamente com os IDs das sequencias
    # print(dataframe.columns)
    seq_id = dataframe[["Query accession", "Target accession", "Sequence identity"]]
    # print(seq_id)

    # retirar os grupos de enzimas com similaridade de 60% a 90% com incrementos de 5%
    target_enzymes = {}
    for perc in range(60, 86, 5):
        chave = str(perc)+"-"+str(perc+5)
        for index, seq in seq_id.iterrows():
            if seq["Sequence identity"] >= perc and seq["Sequence identity"] < perc+5:
                if chave not in target_enzymes.keys():
                    target_enzymes[chave] = [seq["Target accession"]]
                else:
                    target_enzymes[chave].append(seq["Target accession"])
    return target_enzymes

# passar a csv
# seq_id.to_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/Diamond/sequences_identity.csv")
