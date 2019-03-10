from docker_parser import get_docker_container_name


def reorganize_and_merge_info_chartjs(gpu_info, parse_docker=False):
    # reorganize gpu informations
    bar_labels = list()
    bar_memory_data = list()
    bar_utilization_data = list()
    pie_labels = list()
    pie_process_data = list()
    total_free_memory = 0

    for gpu_index, gpu in enumerate(gpu_info):
        gpu_label = 'gpu_{:d}'.format(gpu_index)

        total_memory = gpu['memory']['total']
        total_memory_used = gpu['memory']['used']
        utilization = gpu['gpu_util']
        memory_usage_percentage = int((float(total_memory_used) / float(total_memory)) * 100.0)

        # add labels data
        bar_labels.append(gpu_label)

        # add memory data
        bar_memory_data.append(memory_usage_percentage)

        # add utilization data
        bar_utilization_data.append(utilization)

        for process in gpu['processes']:
            pname = process['name']
            pid = process['pid']
            pmem_used = process['mem_used']

            # check to use docker command to find python related docker container name
            if parse_docker and 'python' in pname:
                docker_container_name = get_docker_container_name(pid)
            else:
                docker_container_name = None

            if docker_container_name is not None:
                process_label = '{:s}/{:s}'.format(gpu_label, docker_container_name)
            else:
                process_label = '{:s}/{:s}'.format(gpu_label, pname)

            # add to datapoints
            pie_labels.append(process_label)
            pie_process_data.append(pmem_used)

        # add free memory
        free_memory = total_memory - total_memory_used
        total_free_memory += free_memory

    # add total free memory
    pie_labels.append('free')
    pie_process_data.append(total_free_memory)

    # merge as single dictionary
    ret = {
        'bar_chart': {
            'labels': bar_labels,
            'memory_data': bar_memory_data,
            'utilization_data': bar_utilization_data,
        },
        'pie_chart': {
            'labels': pie_labels,
            'processes_data': pie_process_data
        }
    }
    return ret
