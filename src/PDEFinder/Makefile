rule UPIMAPI_search:
    input:
        "Data/FASTA/literature_seq/lit_sequences.fasta"
    output:
        "Alignments/BLAST/results/upimapi_results.zip"
    shell:
        "bwa mem {input} | samtools view -Sb - > {output}"


rule UPIMAPI_parse:
	input:
		"Alignments/BLAST/results/upimapi_results/UPIMAPI_results.tsv"
	script:
		"tsv_parser.py"


rule seq_download:
	input:
		
