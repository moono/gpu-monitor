from helper import query_command


def get_docker_container_id_n_name(pid, verbose=False):
    # get information via pid
    # command_str_list = ['cat', '/proc/{}/cgroup'.format(pid)]
    command_str_list = ['cat', '/host_proc/{}/cgroup'.format(pid)]
    decoded = query_command(command_str_list)

    # if selected process is related to docker, then it will contain multiple lines with '/docker/' inside
    pid_line = None
    for decoded_str in decoded:
        if '/docker/' in decoded_str:
            pid_line = decoded_str
            break

    # check if it is related to docker container
    if pid_line is not None:
        # docker container id is behind '/' (last one)
        splitted = pid_line.split('/')
        docker_container_id = splitted[-1]

        # use docker inspect to get container name & parse to get only container name
        docker_command_str_list = ['docker', 'inspect', '-f', '{{.Name}}', docker_container_id]
        docker_container_name = query_command(docker_command_str_list)
        docker_container_name = docker_container_name[0]
        docker_container_name = docker_container_name[1:]

        if verbose:
            print('docker image info: {}/{}'.format(docker_container_id[:5], docker_container_name))
        return docker_container_id, docker_container_name
    else:
        return None, None
