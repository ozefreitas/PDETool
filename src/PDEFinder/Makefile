rule UPIMAPI_search:
    input:
        sequence = "Data/FASTA/literature_seq/lit_sequences.fasta",
		database = "path to DB"
    output:
        "Alignments/BLAST/results"
	threads: 8
    shell:
        "upimapi.py -i {input.sequence} -o {output} --use-diamond -db {input.database} -t {threads}"


rule UPIMAPI_parse:
	input:
		"Alignments/BLAST/results/upimapi_results/UPIMAPI_results.tsv"
	output:
		# é apenas um dataframe
	script:
		"tsv_parser.py"


rule seq_download:
	input:
		# o que sai da de cima
	output:
		"Data/FASTA/UPIMAPI/{thresholds}.fasta"
	script:
		"uniprot_retriever.py"


rule cd-hit_per_threshold:
	input:
		"Data/FASTA/UPIMAPI/{thresholds}.fasta"
	output:
		"Data/FASTA/UPIMAPI/cd-hit90_after_diamond_{thresholds}.fasta"
	shell:
		"docker run --rm -v ~/FASTA/UPIMAPI/:/data/ biocontainers/cd-hit:v4.6.8-2-deb_cv1 bash -c "cd-hit -i data/{input} -o {output} -c 0.9 -n 5 -M 16000 -d 0 -T 8"


rule cd-hit_parse:
	input:
		"Data/FASTA/UPIMAPI/cd-hit90_after_diamond_{thresholds}.fasta"
	output:
		# é um dicionario
	script:
		"txt_parser.py"


rule seq_download:
	input:
		o que sair de cima
	output:
		"Data/FASTA/CDHIT/{thresholds}/{clusters}.fasta"  # todos os clusters, por threshold
	script:
		"uniprot_retriever.py" from_cdhit


rule t_coffee:
	input:
	 	"Data/FASTA/CDHIT/{thresholds}/{clusters}.fasta"
	output:
		"Alignments/MultipleSequencesAlign/T_Coffee_UPI/{thresholds}/{clusters}.clustal_aln"
	shell:
		"docker run --rm -v ~/PDEFinder/:/data pegi3s/tcoffee:latest t_coffee data/{input} -run_name data/{output} -output clustalw_aln"


rule hmmbuild:
	input:
		"Alignments/MultipleSequencesAlign/T_Coffee_UPI/{thresholds}/{clusters}.clustal_aln"
	output:
		"Data/HMMs/After_tcoffee_UPI/{thresholds}/{clusters}.hmm"
	shell:
		"docker run --rm -v ~/PDEFinder/:/data biocontainers/hmmer:v3.2.1dfsg-1-deb_cv1 hmmbuild {output} {input}"


rule hmmsearch:
	input:
		"Data/HMMs/After_tcoffee_UPI/{thresholds}/{clusters}.hmm",
		"path to DB"
	output:
		"Data/HMMs/HMMsearch_results/After_UPI/{thresholds}/{clusters}.out"
	shell:
		"docker run --rm -v ~/PDEFinder/:/data biocontainers/hmmer:v3.2.1dfsg-1-deb_cv1 hmmsearch {input} > {output}"