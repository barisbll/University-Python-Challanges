import re
from datetime import datetime
from ipaddress import IPv4Address

def run():

    log_list = read_config()
    lines = read_log()
    tuple_list = analyze_log(lines)

    #datetime_coverter(tuple_list[0][1])

    http_req = Http_Request(log_list)
    #print(http_req)

    log_entry = Log_Entry(tuple_list[0])
    #print(log_entry)

    #print(log_entry_converter(tuple_list[7]))

    log_entry_list = log_entry_list_converter(tuple_list)
    #print(log_entry_list[200])

    between_times_list = display_between_times( log_entry_list[200].date,log_entry_list[0].date, log_entry_list)
    print(between_times_list)


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


# Takes 1 date string and returns 1 date object
def datetime_coverter(date_str):

    # Remove curly braces and other useless data
    date_str = date_str[1:21]

    # Change verbal month definition to integer month definition
    month_dict = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
    }

    for month in month_dict:
        if month in date_str:
            date_str = date_str.replace(month, month_dict[month])

    # Define read format to convert a datetime object
    format_str = "%d/%m/%Y:%H:%M:%S"
    return datetime.strptime(date_str, format_str)


# Stores the config data as an object
class Http_Request:

    def __init__(self, log_list):
        self.name = log_list[0]
        self.debug = log_list[1]
        self.lines = log_list[2]['lines']
        self.seperator = log_list[2]['seperator']
        self.filter = log_list[2]['filter']

    def req_method(self):
        return self.filter

    def req_res(self):
        return self.name

    def __str__(self):
        return(f'Http Request\'s Name -> {self.name} \n'
              f'Http Request\'s Debug Data -> {self.debug} \n'
              f'Http Request\'s Line Number -> {self.lines} \n'
              f'Http Request\'s Seperator Type -> {self.seperator} \n'
              f'Http Request\'s Request Method -> {self.filter} \n')


# Store the log data using IPv4 Module
class Log_Entry:

    def __init__(self, tuple_item):
        self.ip = IPv4Address(tuple_item[0])
        self.date = datetime_coverter(tuple_item[1])
        self.req = tuple_item[2]
        self.req_protocol = tuple_item[3]
        self.byte_size = tuple_item[4]

    def __str__(self):
        return (f'Log Entry\'s IP Address -> {self.ip} \n'
                f'Log Entry\'s Date -> {self.date} \n'
                f'Log Entry\'s Request -> {self.req} \n'
                f'Log Entry\'s Request Protocol -> {self.req_protocol} \n'
                f'Log Entry\'s Byte Size -> {self.byte_size} \n ')


# Takes 1 line from the log file and returns
# An instance of Log_Entry class
def log_entry_converter(log_item):

    try:
        log_obj = Log_Entry(log_item)

        if log_obj.req_protocol == '404':
            raise Malformed_Http_Request(log_obj.req_protocol)
        else :
            return  log_obj

    except Malformed_Http_Request as mhttp:
        return 'error'


# Reads the content of the log file
# Returns a list of Log_Entry instances
def log_entry_list_converter(tuple_list):

    log_entry_list = []
    error_ctr = 0

    for e in tuple_list:

        if log_entry_converter(e) != 'error':
            log_entry_list.append(log_entry_converter(e))
        else:
            error_ctr += 1

    # print(f'{error_ctr} errors found ')
    return log_entry_list


# Make an Exception class choose 1 exception
# You wish as a base class
# Change the log_entry_converters as specified in the doc
class Malformed_Http_Request(Exception):

    def __init__(self, req_protocol, message = '404 Page Not Found'):
        self.protocol = req_protocol
        self.message = message
        super().__init__(self.message)


# Displays all requests between 2 given time
def display_between_times(time_1, time_2, log_entry_list):
    between_times_list = []
    if time_2 > time_1:



        for log_entry in log_entry_list:
            if log_entry.date > time_1 and \
               log_entry.date < time_2:

                between_times_list.append(log_entry)

        return between_times_list

    else:
        print('Second Time Parameter is Earlier Than The First One')
        return between_times_list

run()
