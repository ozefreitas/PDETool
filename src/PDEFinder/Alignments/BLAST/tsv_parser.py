import pandas as pd

# dar os nomes as colunas
header = ["Query accession", "Target accession", "Sequence identity", 
            "Length", "Mismatches", "Gap openings", "Query start", 
            "Query end", "Target start", "Target end", "E-value", "Bit score"]

# ler file em csv separado por tabs
diamond_outfile = pd.read_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/diamond_out.tsv", sep="\t", names=header)
print(diamond_outfile)

# selecionar colunas com perc. identity juntamente com os IDs das sequencias
print(diamond_outfile.columns)
seq_id = diamond_outfile[["Query accession", "Target accession", "Sequence identity"]]
print(seq_id)

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

print(target_enzymes.keys())
print(target_enzymes.values())

# passar a csv ambos 
diamond_outfile.to_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/best_matches.csv")
seq_id.to_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/sequences_identity.csv")