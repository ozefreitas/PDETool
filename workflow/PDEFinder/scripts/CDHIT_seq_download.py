import pandas as pd
import urllib.request


def fasta_retriever_from_cdhit(tsv_file, threshold):
    """_summary_

    Args:
        tsv_file (string): String containing the name of the .tsv file to be processed.
        threshold (string): interval of the similarity threshold.
    """
    df = pd.read_csv(tsv_file, sep="\t", index_col=0)
    for index, content in df.iterrows():
        # abre o ficheiro no modo write
        file = open(file=newpath + "/" + str(index) + ".fasta", mode="w")
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


# fasta_retriever_from_cdhit(snakemake.input[0])