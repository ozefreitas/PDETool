import urllib.request

def fasta_retriever(seq_ids = None, filename = None):
    file = open(file=filename, mode="w")
    for seq in seq_ids:
        data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + str(seq) + ".fasta")
        fasta = data.read()
        fasta = fasta.splitlines()
    for line in fasta:
        file.writelines(line)
    file.close()

# seq = fasta_retriever()
# print(seq)

def url_retriever(seq_ids=None):
    code = "Q7Z7W5"
    data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + code + ".fasta")
    dados = data.read()
    encoding = 'utf-8'
    dados = dados.decode(encoding)
    teste = dados.split("\n")
    return teste 

seq = url_retriever()
print(seq)