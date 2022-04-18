import urllib.request
import re


def fasta_retriever(seq_ids, dic=False, filename=None):
    """Given a dictionary with UniProt ID's, write a fasta file with all fasta sequences of the corresponding ID's

    Args:
        seq_ids (dictionary): A dictionary where the keys are intervals of sequence similarity, and values are lists of UniProtKB queries 
        filename (string, optional): A name to asign to the fasta file containing all sequences
    """

    # iterar pelos values do dicionário, que são listas
    if dic:
        for ident, seqs in seq_ids.items():
            # abre o ficheiro no modo write
            file = open(file="c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/Diamond" + ident + ".fasta", mode="w")
            for seq in seqs:
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
    else:
        file = open(file="c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/Diamond_target_enzymes.fasta", mode="w")
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