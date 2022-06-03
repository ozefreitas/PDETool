import pandas as pd
import urllib.request


def fasta_retriever_from_cdhit(tsv_file, out_folder):
    """Given a .tsv file for each similarity threshold with UniProt ID's as data, first column as number of the cluster, 
    write a fasta file with all fasta sequences of the corresponding ID's, by cluster.

    Args:
        tsv_file (string): String containing the name of the .tsv file to be processed.
        threshold (string): interval of the similarity threshold.
    """
    df = pd.read_csv(tsv_file, sep="\t", index_col=0)
    cluster = out_folder.split("/")[-2]
    threshold = out_folder.split("/")[-1].split(".f")[0]
    print(cluster)
    print(threshold)
    for index, content in df.iterrows():
        if index == cluster:
            # abre o ficheiro no modo write
            file = open("c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/CDHIT" + threshold + "/" + str(index) + ".fasta", mode="w")
            for seq in list(content):
                try:
                    # faz o download da sequencia em formato fasta
                    data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + seq + ".fasta")
                except:
                    continue
                dados = data.read()
                # urllib.request.urlopen retorna os dados em forma de bytes, tem que ser convertido em string
                encoding = 'utf-8'
                fasta = dados.decode(encoding)
                fasta = fasta.split("\n")
                # para cada elemento da lista gerado pelo split
                for line in fasta:
                    # vai adicionar uma linha ao ficheiro, juntamente com o \n no final, para fazer uma nova linha
                    file.write(line)
                    file.write("\n")
            file.close()


# fasta_retriever_from_cdhit(snakemake.input[0], threshold)
# fasta_retriever_from_cdhit("C:/Users/Ze/Desktop/Mestrado/3ºSemestre/TESE/PDETool/workflow/Data/Tables/cdhit_clusters_60-65_afterUPIMAPI.tsv", "C:/Users/Ze/Desktop/Mestrado/3ºSemestre/TESE/PDETool/workflow/Data/FASTA/CDHIT/60-65/1.fasta")