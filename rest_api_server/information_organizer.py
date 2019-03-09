from docker_parser import get_docker_container_id_n_name


def reorganize_and_merge_info(gpu_info, parse_docker=False):
    # reorganize gpu informations
    data_points_memory = list()
    data_points_util = list()
    data_points_processes = list()
    total_free_memory = 0

    for gpu_index, gpu in enumerate(gpu_info):
        gpu_label = 'gpu_{:d}'.format(gpu_index)

        total_memory = gpu['memory']['total']
        total_memory_used = gpu['memory']['used']
        utilization = gpu['gpu_util']

        memory_usage_percentage = int((float(total_memory_used) / float(total_memory)) * 100.0)
        data_points_memory.append({'label': gpu_label, 'y': memory_usage_percentage})
        data_points_util.append({'label': gpu_label, 'y': utilization})

        for process in gpu['processes']:
            pname = process['name']
            pid = process['pid']
            pmem_used = process['mem_used']

            # check to use docker command to find python related docker container name
            if parse_docker and 'python' in pname:
                docker_container_id, docker_container_name = get_docker_container_id_n_name(pid, False)
            else:
                docker_container_id, docker_container_name = None, None

            if docker_container_name is not None:
                process_label = '{:s}/{:s}'.format(gpu_label, docker_container_name)
            else:
                process_label = '{:s}/{:s}'.format(gpu_label, pname)

            # add to datapoints
            data_points_processes.append({'name': process_label, 'y': pmem_used})

        # add free memory
        free_memory = total_memory - total_memory_used
        total_free_memory += free_memory

    # add total free memory
    data_points_processes.append({'name': 'free', 'y': total_free_memory})

    # merge as single dictionary
    ret = {
        'dp_memory': data_points_memory,
        'dp_utilization': data_points_util,
        'dp_processes': data_points_processes
    }
    return ret