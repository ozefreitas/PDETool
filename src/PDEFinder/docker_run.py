from subprocess import run
import sys


def run_command(bashCommand, output='', mode='w', sep=' ', print_message=True, verbose=True):
    if print_message:
        print(f"{bashCommand.replace(sep, ' ')}{' > ' + output if output != '' else ''}")
    if output == '':
        run(bashCommand.split(sep), stdout=sys.stdout if verbose else None, check=True)
    else:
        with open(output, mode) as output_file:
            run(bashCommand.split(sep), stdout=output_file)

def docker_run_tcoffee(volume, input_dir, input_file, output_type, output_name):
    run_command(f'docker run --rm -v {volume} pegi3s/tcoffee t_coffee /data/{input_dir}/{input_file} -run_name /data/{output_name} -output {output_type}')