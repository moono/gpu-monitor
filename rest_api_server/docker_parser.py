from helper import query_command


def find_docker_container_id(pid):
    # get information via pid
    try:
        # command_str_list = ['cat', '/proc/{}/cgroup'.format(pid)]
        command_str_list = ['cat', '/host_proc/{}/cgroup'.format(pid)]
        decoded = query_command(command_str_list)
    except ValueError as e:
        print(e)
        return None

    # if selected process is related to docker, then it will contain multiple lines with '/docker/' inside
    pid_line = None
    for decoded_str in decoded:
        if '/docker/' in decoded_str:
            pid_line = decoded_str
            break

    # check if it is related to docker container
    docker_container_id = None
    if pid_line is not None:
        # docker container id is behind '/' (last one)
        splitted = pid_line.split('/')
        docker_container_id = splitted[-1]
    return docker_container_id


def get_docker_container_name(pid):
    docker_container_id = find_docker_container_id(pid)

    # use docker inspect to get container name & parse to get only container name
    if docker_container_id is not None:
        try:
            docker_command_str_list = ['docker', 'inspect', '-f', '{{.Name}}', docker_container_id]
            docker_container_name = query_command(docker_command_str_list)
            docker_container_name = docker_container_name[0]
            docker_container_name = docker_container_name[1:]
            return docker_container_name
        except ValueError as e:
            print(e)
            return None
    else:
        return None
