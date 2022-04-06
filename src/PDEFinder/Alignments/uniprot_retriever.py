import urllib.request


def url_retriever(seq_ids=None):
    code = "Q7Z7W5"
    data = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + code + ".fasta")
    dados = data.read()
    dados = dados.splitlines()
    return dados 

seq = url_retriever()
print(seq)