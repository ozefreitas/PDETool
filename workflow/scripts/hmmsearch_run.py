from docker_run import run_command

def run_hmmsearch(sequences_file: str, hmm_file: str, output_file: str, out_type = "out"):
    if out_type == "out":
        run_command(f"hmmsearch {hmm_file} {sequences_file} > {output_file}")
    elif out_type == "tsv":
        run_command(f"hmmsearch --tblout {output_file} {hmm_file} {sequences_file}")
    elif out_type == "pfam":
        run_command(f"hmmsearch --pfamtblout {output_file} {hmm_file} {sequences_file}")