import subprocess


def query_command(command_str_list):
    try:
        output = subprocess.Popen(command_str_list, stdout=subprocess.PIPE).communicate()[0]
        decoded = output.decode('utf-8')
        decoded = decoded.splitlines()
        return decoded
    except OSError as e:
        raise ValueError(e.strerror)


def main():
    try:
        display_string = ','.join(['MEMORY', 'UTILIZATION', 'PIDS'])
        # decoded = query_command(['hhnvidia-smi', '-q', '--display={:s}'.format(display_string)])
        decoded = query_command(['nvidia-smi', '-q', '--display={:s}'.format(display_string)])
        print(decoded)
    except ValueError as e:
        print(e)
    return


if __name__ == '__main__':
    main()

