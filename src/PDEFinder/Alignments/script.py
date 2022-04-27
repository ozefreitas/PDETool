from tsv_parser import diamond_parser, iter_per_sim, above_60, devide_by_query
from uniprot_retriever import fasta_retriever

df = diamond_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/Diamond/diamond_out.tsv")

# enzymes = iter_per_sim(df)
# print(enzymes)

enzyme_search = above_60(df)
print(enzyme_search)
fasta_retriever(enzyme_search, filename="Diamond_target_enzymes")

enzymes = devide_by_query(df)
print(enzymes)
fasta_retriever(enzymes, dic=True, filename="Diamond_target_enzymes_byquery", query=True)