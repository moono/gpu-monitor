import subprocess


def query_command(command_str_list):
    output = subprocess.Popen(command_str_list, stdout=subprocess.PIPE).communicate()[0]
    decoded = output.decode('utf-8')
    decoded = decoded.splitlines()
    return decoded
