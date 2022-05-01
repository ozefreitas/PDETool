from tsv_parser import diamond_parser, iter_per_sim, above_60, devide_by_query, UPIMAPI_parser, UPIMAPI_iter_per_sim
from uniprot_retriever import fasta_retriever
from txt_parser import read_clstr_file, cdhit_parser


# df = diamond_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/Diamond/diamond_out.tsv")

# enzymes = iter_per_sim(df)
# print(enzymes)

# enzyme_search = above_60(df)
# print(enzyme_search)
# fasta_retriever(enzyme_search, filename="Diamond_target_enzymes")
# 
# enzymes = devide_by_query(df)
# print(enzymes)
# fasta_retriever(enzymes, dic=True, filename="Diamond_target_enzymes_byquery", query=True)

# upi = UPIMAPI_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/BLAST/results/upimapi_results/UPIMAPI_results.tsv")
# print(upi)
# 
# upi_enzymes = UPIMAPI_iter_per_sim(upi)
# print(upi_enzymes.keys())
# print(upi_enzymes)
# 
# fasta_retriever(upi_enzymes, dic=True)


### Processamento dos cd-hit depois do upimapi

sequencias = cdhit_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/UPIMAPI/cd-hit90_after_diamond_60-65.fasta.clstr")
print(sequencias)

