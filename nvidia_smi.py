import subprocess
import pprint


class MemoryUsage(object):
    def __init__(self, mtotal, mused, mfree):
        if not (isinstance(mtotal, int) or isinstance(mused, int) or isinstance(mfree, int)):
            raise ValueError('Inputs must be numeric ints')
        self.total = mtotal
        self.used = mused
        self.free = mfree
        self.percentage = float(mused) / float(mtotal) * 100.0
        return


class Process(object):
    def __init__(self, pid, ptype, pname, pused):
        if not (isinstance(pid, int) or isinstance(pused, int)):
            raise ValueError('Inputs must be numeric ints')
        if not (isinstance(ptype, str) or isinstance(pname, str)):
            raise ValueError('Inputs must be numeric strings')

        self.pid = pid
        self.type = ptype
        self.name = pname
        self.used = pused
        return


class GPUInfo(object):
    def __init__(self, index, name, uuid, utilization, memory_info, process_info):
        if not isinstance(memory_info, MemoryUsage):
            raise ValueError('memory_info must be MemoryUsage class!!')
        if not isinstance(process_info, Process):
            raise ValueError('process_info must be Process class!!')

        self.index = index
        self.name = name
        self.uuid = uuid
        self.utilization = utilization
        self.memory_info = memory_info
        self.process_info = process_info

        return


def query_command(command_str_list):
    output = subprocess.Popen(command_str_list, stdout=subprocess.PIPE).communicate()[0]
    decoded = output.decode('utf-8')
    decoded = decoded.splitlines()
    return decoded


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
    return MemoryUsage(mem_total_val, mem_used_val, mem_free_val)


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
        p_obj = Process(pid_val, ptype_val, pname_val, pmem_val)
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
    # query nvidia-smi once
    display_string = ','.join(['MEMORY', 'UTILIZATION', 'PIDS'])
    decoded = query_command(['nvidia-smi', '-q', '--display={:s}'.format(display_string)])

    # parse header to get number of gpus
    n_gpus, decoded = parse_header(decoded)

    current_item = None
    useful_info = list()
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
                useful_info.append(current_item)

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
            else:
                decoded_index += 1
        else:
            decoded_index += 1

    # insert last item if any
    if current_item:
        useful_info.append(current_item)
    return useful_info


def main():
    useful_info = run_nvidia_smi()
    pprint.pprint(useful_info)
    return


if __name__ == '__main__':
    main()


# def get_list_of_gpus():
#     decoded = query_command(['nvidia-smi', '-L'])
#
#     list_of_gpus = dict()
#     for decoded_str in decoded:
#         gpu_index, gpu_type_uuid = decoded_str.split(':', 1)
#
#         gpu_index = int(gpu_index.split(' ', 1)[1])
#
#         gpu_type, gpu_uuid = gpu_type_uuid.split('(', 1)
#         gpu_type = gpu_type.rstrip()
#
#         gpu_uuid, _ = gpu_uuid.split(')', 1)
#         _, gpu_uuid = gpu_uuid.split(':', 1)
#         gpu_uuid = gpu_uuid.lstrip()
#
#         list_of_gpus[gpu_index] = {
#             'gpu_type': gpu_type,
#             'gpu_uuid': gpu_uuid,
#         }
#     return list_of_gpus
