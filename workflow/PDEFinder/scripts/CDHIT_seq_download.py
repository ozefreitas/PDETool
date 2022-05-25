import os
import urllib.request


def fasta_retriever_from_cdhit(seq_ids, threshold):
    parent_dir = "c:/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/PDETool/src/PDEFinder/Data/FASTA/CDHIT/"
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

