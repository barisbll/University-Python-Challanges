import re


# Main function tha calls other functions
def run():
    configList = read_config()
    logList = read_log()
    tupleList = analyze_log(logList)
    # print_reqs(configList, tupleList)
    print_total_bytes(configList, tupleList)


# Read From .config File and Return Structured Data
def read_config():

    try:

        with open('lab6.config', 'r') as read_file:
            conf = read_file.readlines()

        # Removing \n's
        for e in conf:
            if (e == '\n'):
                conf.remove(e)

        for idx, e in enumerate(conf):
            conf[idx] = e[:-1]

        # Making list of the content string seperated by ','
        # and added '&' to easier regex match
        seperator = ","
        conf_Str = seperator.join(conf) + '&'

        # raise exception and add default values if lab6.config is corrupted
        try:

            # Adding default values
            log_file = 'access log-20201025'
            config = 'INFO'
            display = {
                'lines': '6',
                'seperator': '|',
                'filter': 'GET'
            }

            # Filter values into 3 variables log_file, config, display

            regex = re.compile(r'(\[.+?,.+?,([^\[].+?,.+?\&)?)')
            match_list = regex.findall(conf_Str)

            log_file_mo = re.search('name=.+?,', str(match_list[0]))
            log_file = str(log_file_mo.group())[5:-1]

            config_mo = re.search('debug=.+?,', str(match_list[1]))
            config = str(config_mo.group())[6:-1]

            # display = dict()
            display_mo = re.search(',(.+?),(.+?),(.+?&)', str(match_list[2]))

            display['lines'] = str(display_mo.group(1))[-1]
            display['seperator'] = str(display_mo.group(2))[-1]
            display['filter'] = str(display_mo.group(3))[7:-1]

        except Exception:

            print('Error')

        return [log_file, config, display]

    except FileNotFoundError as fnf:
        print(fnf)


# Reads from access-log and returns log-lines as a list
def read_log():
    try:
        list = []
        with open('access-log.txt', 'r') as read_file:
            list = read_file.readlines()

        return list

    except FileNotFoundError as fnf:
        print(fnf)


# Analyze input list and seperate its content into tuple elements in a list
def analyze_log(list):

    regex = re.compile(r'(\d+?\.\d+?\.\d+?\.\d+?)\s-\s-\s'
                       r'(\[.+?\])\s"(.+?)"\s(\d+?)\s(\d+?)\s')
    match = regex.findall(str(list))
    return match


def print_reqs(configList, tupleList):

    ip_addr = '152.32.65.99'
    mask = (253976 % 16) + 8
    lines = int(configList[2]['lines'])

    ip_list = []
    for e in tupleList:
        ip_list.append(e[0])

    match_list = find_ip_matches(ip_addr, mask, ip_list)

    # Present the matched ip addresses as pressed enter
    ctr = 0
    while ctr < lines and ctr < len(match_list):

        tmp_inp = input('Press Enter to See Matched '
                        'IP Addresses and  Write "exit" to Exit\n')
        if tmp_inp == 'exit':
            break

        print(match_list[ctr])
        ctr += 1


# Helpful function for print_reqs
def find_ip_matches(ip_addr, mask_length, ip_list):

    # Convert all ip addresses to binary lists
    binary_list = []

    for e in ip_list:
        tmp = e.split('.')
        bin_tmp = []

        for e in tmp:
            bin_tmp.append(bin(int(e)))

        binary_list.append(bin_tmp)

    # convert main ip address to binary list
    tmp_bin_ip_addr_list = ip_addr.split('.')
    bin_ip_addr_list = []

    for e in tmp_bin_ip_addr_list:
        bin_ip_addr_list.append(bin(int(e)))

    # Find steps for conditional operation
    steps = int(mask_length / 8)
    steps_plus = int(mask_length % 8)

    bin_result_list = []

    # Hardest part find ip addresses for defined ip addr and mask
    # Check if each digit of the ip addr equal to log ip addresses
    for sub_list in binary_list:

        ctr = 0
        for step in range(steps):
            if sub_list[step] == bin_ip_addr_list[step]:
                ctr += 1
            else:
                break

            if step + 1 == steps:
                tmp_ctr = 0

                for e in range(steps_plus):
                    if steps_plus != 0 and \
                            sub_list[step][e] == bin_ip_addr_list[step][e]:

                        tmp_ctr += 1

                    else:
                        break

                if steps_plus != 0 and tmp_ctr == steps_plus:
                    bin_result_list.append(sub_list)

        if steps_plus == 0 and ctr == steps:
            bin_result_list.append(sub_list)

    # Convert bin_result_list to ip address list and return

    result_list = []
    for sub_list in bin_result_list:

        tmp_list = []
        seperator = '.'

        for e in sub_list:
            tmp_list.append(str(int(e, 2)))
        result_list.append(seperator.join(tmp_list))

    return result_list


def print_total_bytes(config_list, tuple_list):

    filter = config_list[2]['filter']
    seperator = config_list[2]['seperator']

    total_sum = 0

    for e in tuple_list:
        if '"GET ' in e[2]:
            total_sum += int(e[4])

    print(f'Type of the request is : {filter} \t '
          f'{seperator} \t Sum of total bytes is {total_sum}')


run()
