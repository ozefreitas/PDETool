from tsv_parser import diamond_parser, iter_per_sim, above_60, devide_by_query, UPIMAPI_parser, UPIMAPI_iter_per_sim
from uniprot_retriever import fasta_retriever, fasta_retriever_from_cdhit
from txt_parser import cdhit_parser, counter
from docker_run import docker_run_tcoffee


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


### Processamento dos cd-hit depois do upimapi e criacao dos ficheiros fasta com cada cluster

# for perc in range(60, 86, 5):
#     chave = str(perc)+"-"+str(perc+5)
#     sequencias = cdhit_parser("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/UPIMAPI/cd-hit90_after_diamond_" + chave + ".fasta.clstr")
#     numb_seq = counter(sequencias, remove_single=True)
#     print(numb_seq)
#     fasta_retriever_from_cdhit(numb_seq, chave)


### Correr t_coffee para todos os ficheiros gerados em cima

docker_run_tcoffee("~/FASTA/CD-HIT/:/data/", "60-65", "1.fasta", "clustalw_aln", "1.clustal_aln")