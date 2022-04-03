import pandas as pd

diamond_outfile = pd.read_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/diamond_out.tsv", sep="\t")
print(diamond_outfile)

# selecionar colunas com perc. id. e bit scores


# juntar com os IDs das queries e dos alinhamentos


# passar a csv
diamond_outfile.to_csv("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/best_matches.csv")