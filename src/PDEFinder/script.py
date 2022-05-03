from tsv_parser import diamond_parser, iter_per_sim, above_60, devide_by_query, UPIMAPI_parser, UPIMAPI_iter_per_sim
from uniprot_retriever import fasta_retriever, fasta_retriever_from_cdhit
from txt_parser import cdhit_parser, counter
from docker_run import docker_run_tcoffee, docker_run_hmmbuild, docker_run_hmmsearch
import os
import re

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


# docker_run_tcoffee("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/CDHIT:/data", "60-65", "1.fasta", "clustalw_aln", "1.clustal_aln")
# docker_run_tcoffee("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder:/data", "Data/FASTA/CDHIT/60-65", "1.fasta", "clustalw_aln", "Alignments/MultipleSequencesAlign/T_Coffee_UPI/1.clustal_aln")

# cdhit_path = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/CDHIT"
# dest_path = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/MultipleSequencesAlign/T_Coffee_UPI"
# 
# for fold in os.listdir(cdhit_path):
#     newpath = os.path.join(dest_path, fold)
#     if not os.path.exists(newpath):
#         os.mkdir(newpath)
#     for file in os.listdir(os.path.join(cdhit_path, fold)):
#         print("Executing T-Coffee for file", file, "in the", fold, "thresold.", "\n")
#         docker_run_tcoffee("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder:/data", "Data/FASTA/CDHIT/" + fold, file, "clustalw_aln", "Alignments/MultipleSequencesAlign/T_Coffee_UPI/" + fold + "/" + file + ".clustal_aln")


### Correr hmmbuild para todos os ficheiros de alinhamento gerados em cima

# tcoffee_path = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Alignments/MultipleSequencesAlign/T_Coffee_UPI"
# dest_path = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/HMMs/After_tcoffee_UPI"
# 
# for fold in os.listdir(tcoffee_path):
#     newpath = os.path.join(dest_path, fold)
#     if not os.path.exists(newpath):
#         os.mkdir(newpath)
#     for file in os.listdir(os.path.join(tcoffee_path, fold)):
#         if file.endswith(".clustalw_aln"):
#             print("Executing hmmbuild for file", file, "in the", fold, "thresold.", "\n")
#             outname = ""
#             for i in file:
#                 if i != ".":
#                     outname += i
#                 else:
#                     outname += ".hmm"
#                     break
#             print("Output name:", outname)
#             docker_run_hmmbuild("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/:/data", "Alignments/MultipleSequencesAlign/T_Coffee_UPI/" + fold + "/" + file, "Data/HMMs/After_tcoffee_UPI/" + fold + "/" + outname)


### Correr hmmsearch para todos os modelos contra a UniProt

hmmpath = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/HMMs/After_tcoffee_UPI"
dest_path = "C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/HMMsearch_results/After_UPI"

for fold in os.listdir(hmmpath):
    newpath = os.path.join(dest_path, fold)
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    for file in os.listdir(os.path.join(hmmpath, fold)):
        print("Executing hmmbuild for file", file, "in the", fold, "thresold.", "\n")
        outname = ""
        for i in file:
            if i != ".":
                outname += i
            else:
                outname += ".out"
                break
        print("Output name:", outname)
        docker_run_hmmsearch("C:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder:/data", "Data/HMMs/After_tcoffee_UPI/" + fold + file, database_file, "Data/HMMsearch_results/After_UPI/" + fold + "/" + outname)