from hashlib import new
from msilib.schema import Directory
from operator import ne
import urllib.request
import re
import os


def fasta_retriever(seq_ids, dic=False, filename=None, query=False, seq_proc=False):
    """Given a dictionary with UniProt ID's, write a fasta file with all fasta sequences of the corresponding ID's

    Args:
        seq_ids (dictionary): A dictionary where the keys are intervals of sequence similarity, and values are lists of UniProtKB queries
        dic (bool, optional): _description_. Defaults to False.
        filename (string, optional): A name to asign to the fasta file containing all sequences. Defaults to None.
        query (bool, optional): Set to True if dictionary keys are query names. Defaults to False.
        seq_proc (bool, optional): Decides if is necessary to process UniProt ID's. Defaults to False.
    """

    # iterar pelos values do dicionário, que são listas
    if dic:
        for ident, seqs in seq_ids.items():
            if query:
                ident = re.findall("\|.*\|", ident)
                ident = re.sub("\|", "", ident[0])
            # abre o ficheiro no modo write
            file = open(file="c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/UPIMAPI/" + ident + ".fasta", mode="w")
            for seq in seqs:
                # muda a seq para o codigo que o uniprot aceite como ID
                if seq_proc:
                    code = re.findall("\|.*\|", seq)
                    clean = re.sub("\|", "", code[0])
                else:
                    clean = seq
                try:
                    # faz o download da sequencia em formato fasta
                    data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + clean + ".fasta")
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
    else:
        file = open(file="c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/Diamond/" + filename + ".fasta", mode="w")
        for seq in seq_ids:
            # muda a seq para o codigo que o uniprot aceite como ID
            code = re.findall("\|.*\|", seq)
            clean = re.sub("\|", "", code[0])
            try:
                # faz o download da sequencia em formato fasta
                data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + clean + ".fasta")
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

# seq = fasta_retriever()
# print(seq)

def test_retriever():
    code = "Q7Z7W5"
    data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + code + ".fasta")
    dados = data.read()
    encoding = 'utf-8'
    dados = dados.decode(encoding)
    teste = dados.split("\n")
    return teste 

# seq = url_retriever()
# print(seq)

def fasta_retriever_from_cdhit(seq_ids, threshold):
    parent_dir = "c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/CD-HIT/"
    newpath = os.path.join(parent_dir, threshold)
    if not os.path.exists(newpath):
        os.mkdir(newpath)
    for clstr, seqs in seq_ids.items():
        # abre o ficheiro no modo write
        file = open(file=newpath + "/" + str(clstr) + ".fasta", mode="w")
        for seq in seqs[0]:
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