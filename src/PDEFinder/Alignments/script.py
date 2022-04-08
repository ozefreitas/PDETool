from tsv_parser import diamond_parser, iter_per_sim
from uniprot_retriever import fasta_retriever

df = diamond_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/Diamond/diamond_out.tsv")

enzymes = iter_per_sim(df)
print(enzymes)

# fasta_retriever(enzymes, "/PDETool/src/PDEFinder/Alignments/test.fasta")

fasta_retriever(enzymes)