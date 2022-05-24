import pandas as pd
import re
import urllib.request


def fasta_retriever(tsv_file, out_filename=None, seq_proc=False):
    """Given a .tsv file with UniProt ID's as data, first column as thresholds, write a fasta file with all fasta sequences of the corresponding ID's,
        by similarity thresholds.
    Args:
        tsv_file (bool, optional): _description_. Defaults to False.
        out_filename (string, optional): A name to asign to the fasta file containing all sequences. Defaults to None.
        seq_proc (bool, optional): Decides if is necessary to process UniProt ID's. Defaults to False.
    """
    # abrir tsv como DataFrame
    df = pd.read_csv(tsv_file, sep="\t")
    print(df)
    # iterar pelos values do dicionário, que são listas
#    file = open(file="c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/Diamond/" + out_filename + ".fasta", mode="w")
#    for seq in seq_ids:
#        # muda a seq para o codigo que o uniprot aceite como ID
#        if seq_proc:
#            code = re.findall("\|.*\|", seq)
#            clean = re.sub("\|", "", code[0])
#        else:
#            clean = seq
#        try:
#            # faz o download da sequencia em formato fasta
#            data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + clean + ".fasta")
#        except:
#            continue
#        dados = data.read()
#        # urllib.request.urlopen retorna os dados em forma de bytes, tem que ser convertido em string
#        encoding = 'utf-8'
#        fasta = dados.decode(encoding)
#        fasta = fasta.split("\n")
#        # para cada elemento da lista gerado pelo split
#        for line in fasta:
#            # vai adicionar uma linha ao ficheiro, juntamente com o \n no final, para fazer uma nova linha
#            file.write(line)
#            file.write("\n")
#    file.close()