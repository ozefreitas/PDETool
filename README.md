# PlastEDMA - Plastic Enzymes Degrading for Metagenomic databases Analysis
#### Version 0.1.0 <p>
<br>

## Introduction 
<br>
PlastEDMA is a free to use, open source user friendly CLI implemented workflow and database for the detection of plastic degrading enzymes in metagenomic samples, through structural annotation using Hidden Markov Models, that allows the user to freely interacte with the tool in-built databases and backbone. <p>
PlastEDMA compreends a extensive HMM database, built with state of the art checked enzymatic sequences able to degrade plastic polymers, which is used to carry the structural annotation of given sequences. <p>
First version of PlastEDMA is only available for mining PE (polyethylene), as latter version will compreend a more vast list of plastics to analyse. <p>
Also, PlastEDMA is meant to analyse metagenomic sequences, but version 0.1.0 only accepts single FASTA aminoacidic sequences. Basic steps of PlastEDMA annotation workflow in its frist stages are: 

1. The acceptence of any number of protein sequences in a single FASTA file as query;
2. Execution of hmmsearch from the [HMMER package](https://www.hmmer.org/), using the pre-built HMMs from previously knowns sequences able to have some kind of PE deterioration levels as database; 
3. A quality benchmark to determine good and bad hits from the queries against models;
4. Three output files, consisting in a FASTA file with the protein sequences returned as a hit from the search, a report in text format (if requested by the user) with simply puted information about the inputed and already built (HMMs) data, run and processing parameters and conclusions, and an easy to read report table in xlsx format, with all the important data about the annotation results, in particular:
    - Sequence IDs
    - HMM IDs (Degraded plastic + number)
    - Bit scores
    - E-values

<br>

## Installation
<br>
PlastEDMA is, for know, avaliable for Linux platforms though GitHub repository clonning, using the following line in a git bash terminal inside the desired (empty) folder:<p>

```
git clone https://github.com/pg42872/PDETool.git  
#in a command propmt 
cd workdflow/ 
```

We highly recommed users to create an appropriate conda environment with the required dependencies so PlastEDMA executes smoothly, with:

```
cd envs/ 
conda env create -n \<name of env> -f plastedma.yaml 
conda activate \<name of env> 
cd ..
```

PlastEDMA is also planned to be available as a conda package from bioconda. Simply open an Anaconda prompt:

```
conda install plastedma 
```

and you will be good to go.
<p>

## Usage
<br>
The main and most basic use for PlastEDMA is:<p>

```
python PDETool.pt -i path/to/input_file -o output_folder -rt --output_type excel 
```

as the input file must be in FASTA format and contain only (for the time being) aminoacidic sequences, otherwise, program will exit. Output folder can be a pre-existing folder or any name for a fodler that will be created anyways. The `-rt` option flag instructs the tool to include in the output the report in text format, for an easier interpretations of the annotation results and conclusion taking. Also, `--output_type` is recommended to be set to "excel" on these earlier versions, as other output format for the table report will be incrementally coded. <p>
PlastEDMA

## Aditional arguments

```
optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input FASTA file containing a list of protein
                        sequences to be analysed
  -o OUTPUT, --output OUTPUT
                        name for the output directory. Defaults to
                        'PlastEDMA_results'
  --output_type OUTPUT_TYPE
                        chose report table outpt format from 'tsv', 'csv' or
                        'excel'. Defaults to 'tsv'
  -rt, --report_text    decides wether to produce or not a friendly report in
                        txt format with easy to read information
  --hmms_output_type HMMS_OUTPUT_TYPE
                        chose output type from 'out', 'tsv' ou 'pfam' format.
                        Defaults to 'out'
  -p, --produce_inter_tables
                        call if user wants to save intermediate tables as
                        parseale .csv files (tables from hmmsearch results
                        processing)
  -db DATABASE, --database DATABASE
                        path to a user defined database. Default use of in-
                        built database
  -s SNAKEFILE, --snakefile SNAKEFILE
                        user defined snakemake worflow Snakefile. Defaults to
                        /mnt/c/Users/jpsfr/OneDrive/Ambiente de
                        Trabalho/TOOL/PDETool/workflow/Snakefile
  -t THREADS, --threads THREADS
                        number of threads for Snakemake to use. Defaults to 1
  -hm HMM_MODELS, --hmm_models HMM_MODELS
                        path to a directory containing HMM models previously
                        created by the user. By default PDETool uses the
                        built-in HMMs from database in
                        /mnt/c/Users/jpsfr/OneDrive/Ambiente de Trabalho/TOOL/
                        PDETool/workflow/Data/HMMs/After_tcoffee_UPI/
  --concat_hmm_models   concatenate HMM models into a single file
  --unlock              could be required after forced workflow termination
  -w WORKFLOW, --workflow WORKFLOW
                        defines the workflow to follow, between "annotation",
                        "database_construction" and "both". Latter keyword
                        makes the database construction first and posterior
                        annotation. Defaults to "annotation"
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        user defined config file. Only recommended for
                        advanced users. Defaults to
                        /mnt/c/Users/jpsfr/OneDrive/Ambiente de
                        Trabalho/TOOL/PDETool/config/. If given, overrides
                        config file construction from input
  -v, --version         show program's version number and exit
```