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

> <code> git clone https://github.com/pg42872/PDETool.git <br> 
> #in a command propmt <br>
> cd workdflow/ </code>

We highly recommed users to create an appropriate conda environment with the required dependencies so PlastEDMA executes smoothly, with:

> <code> cd envs/ <br> 
> conda env create -n \<name of env> -f plastedma.yaml <br>
> conda activate \<name of env> <br>
> cd .. </code>

PlastEDMA is also planned to be available as a conda package from bioconda. Simply open an Anaconda prompt:

> <code>conda install plastedma</code> ,

and you will be good to go.
<p>

## Usage
<br>
The main and most basic use for PlastEDMA is:<p>

> <code>python PDETool.pt -i path/to/input_file -o output_folder -rt --output_type excel</code> ,

as the input file must be in FASTA format and contain only (for the time being) aminoacidic sequences, otherwise, program will exit. Output folder can be a pre-existing folder or any name for a fodler that will be created anyways. The `-rt` option flag instructs the tool to include in the output the report in text format, for an easier interpretations of the annotation results and conclusion taking. Also, `--output_type` is recommended to be set to "excel" on these earlier versions, as other output format for the table report will be incrementally coded. <p>
PlastEDMA