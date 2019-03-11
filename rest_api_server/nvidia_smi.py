from helper import query_command


def compute_leading_space(in_str):
    return len(in_str) - len(in_str.lstrip())


def handle_values(in_str):
    key, val = in_str.split(':', 1)
    key, val = key.strip(), val.strip()
    return key, val


def handle_memory_values(decoded, index):
    mem_total_key, mem_total_val = handle_values(decoded[index + 1])
    mem_used_key, mem_used_val = handle_values(decoded[index + 2])
    mem_free_key, mem_free_val = handle_values(decoded[index + 3])

    mem_total_val = int(mem_total_val.lstrip().split(' ')[0])
    mem_used_val = int(mem_used_val.lstrip().split(' ')[0])
    mem_free_val = int(mem_free_val.lstrip().split(' ')[0])
    memory_info = {
        'total': mem_total_val,
        'used': mem_used_val,
        'free': mem_free_val
    }
    return memory_info


def handle_utilization_values(decoded, index):
    util_gpu_key, util_gpu_val = handle_values(decoded[index + 1])
    util_gpu_val = int(util_gpu_val.lstrip().split(' ')[0])
    return util_gpu_val


def handle_process_values(decoded, index):
    process_list = list()
    p_index = index + 1
    while compute_leading_space(decoded[p_index]) > 0:
        pid_key, pid_val = handle_values(decoded[p_index])
        ptype_key, ptype_val = handle_values(decoded[p_index + 1])
        pname_key, pname_val = handle_values(decoded[p_index + 2])
        pmem_key, pmem_val = handle_values(decoded[p_index + 3])

        pid_val = int(pid_val)
        pmem_val = int(pmem_val.lstrip().split(' ')[0])
        pname_val = (pname_val.split('/')[-1]).split(' ')[0]
        p_obj = {
            'pid': pid_val,
            'type': ptype_val,
            'name': pname_val,
            'mem_used': pmem_val
        }
        process_list.append(p_obj)

        p_index += 4

    return process_list


def parse_header(decoded):
    index = 0
    n_gpus = 0
    for decoded_str in decoded:
        index += 1
        if 'Attached GPUs' in decoded_str:
            key, val = handle_values(decoded_str)
            n_gpus = int(val)
            break

    decoded = decoded[index:]
    return n_gpus, decoded


def run_nvidia_smi():
    # try:
    #     # query nvidia-smi once
    #     display_string = ','.join(['MEMORY', 'UTILIZATION', 'PIDS'])
    #     decoded = query_command(['nvidia-smi', '-q', '--display={:s}'.format(display_string)])
    # except ValueError as e:
    #     print(e)
    #     return list()
    with open('test_out.txt') as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    decoded = [x.rstrip('\n') for x in content]

    # parse header to get number of gpus
    n_gpus, decoded = parse_header(decoded)

    current_item = None
    parsed_gpu_info = list()
    decoded_index = 0
    while decoded_index < len(decoded):
        # get current item
        decoded_str = decoded[decoded_index]

        # check if empty string
        if len(decoded_str) == 0:
            decoded_index += 1
            continue

        # find leading space
        leading_space = compute_leading_space(decoded_str)
        lstriped_str = decoded_str.lstrip()

        # check string leading spaces
        if leading_space == 0:
            if current_item is not None:
                parsed_gpu_info.append(current_item)

            # reset current_item
            current_item = dict()
            decoded_index += 1
        elif leading_space == 4:
            if lstriped_str == 'FB Memory Usage':
                mem_obj = handle_memory_values(decoded, decoded_index)
                current_item['memory'] = mem_obj
                decoded_index += 4
            elif lstriped_str == 'Utilization':
                util_gpu = handle_utilization_values(decoded, decoded_index)
                current_item['gpu_util'] = util_gpu
                decoded_index += 5
            elif lstriped_str == 'Processes':
                p_list = handle_process_values(decoded, decoded_index)
                current_item['processes'] = p_list
                decoded_index += len(p_list) * 4 + 1
            # in case of 'Processes:    None'
            elif 'Processes' in lstriped_str:
                current_item['processes'] = list()
                decoded_index += 1
            else:
                decoded_index += 1
        else:
            decoded_index += 1

    # insert last item if any
    if current_item:
        parsed_gpu_info.append(current_item)
    return parsed_gpu_info


def main():
    import pprint

    try:
        parsed_gpu_info = run_nvidia_smi()
        pprint.pprint(parsed_gpu_info, width=1)
    except ValueError as e:
        print(e)
    return


if __name__ == '__main__':
    main()

