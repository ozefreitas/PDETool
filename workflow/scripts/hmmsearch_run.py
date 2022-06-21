from docker_run import run_command

def run_hmmsearch(sequences_file: str, hmm_file: str, output_file: str):
    run_command(f"hmmsearch {hmm_file} {sequences_file} > {output_file}")