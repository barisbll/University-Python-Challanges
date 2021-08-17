import re
import pyinputplus as pyip
from datetime import datetime
import json
from json import JSONDecoder
from json import JSONEncoder




def main():
    config_json()
    read_config_raise_err()
    #list = print_all_index()
    #print_requests_in_the_config(list)



# 1 ask for config parameters and store them in data.json file
def config_json():

    # Ask for values and put them in variables

    dict_config = {}

    dict_config["name_webserver_log"] = pyip.inputStr(prompt="Name of the webserver log -> ", blank=True)
    if dict_config["name_webserver_log"] == '': dict_config["name_webserver_log"] = '152.32.65.99'

    dict_config["name_http_request_method"] = pyip.inputChoice(["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT" "PATCH"], blank=True)
    if dict_config["name_http_request_method"] == '': dict_config["name_http_request_method"] = 'GET'

    dict_config["log_level"] = pyip.inputChoice(["Access-Log", "Error-Log"],default="Access-Log", blank=True)
    if dict_config["log_level"] == '': dict_config["log_level"]='Access-Log'

    dict_config["num_log_lines_to_display"] = pyip.inputNum(prompt="Write number of lines to display: ",min=1, blank=True)
    if dict_config["num_log_lines_to_display"] == '': dict_config["num_log_lines_to_display"] = '5'

    dict_config["http_response_code"] = pyip.inputNum(prompt="Enter http response code: ", min=100, max=599, blank=True)
    if dict_config["http_response_code"] == '': dict_config["http_response_code"] = '301'

    dict_config["response_byte_size"] = pyip.inputNum(prompt="Enter the response's byte size: ", max=5000, default=200, blank=True)
    if dict_config["response_byte_size"] == '' : dict_config["response_byte_size"] = '234'

    dict_config["date"] = datetime.now()


    # Encode values to the json
    encode(dict_config, 'data.json')


def encode(dicti, file_name):
    with open(file_name , 'w') as write_file:
        json.dump(dicti, write_file, cls=DateTimeEncoder, indent=4)


def decode(file):
    data = json.load(file)
    return data


class DateTimeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kargs):
        JSONDecoder.__init__(self, object_hook=self.dict_to_object,
                             *args, **kargs)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        type = d.pop('__type__')
        try:
            dateobj = datetime(**d)
            return dateobj
        except:
            d['__type__'] = type
            return d


class DateTimeEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'year': obj.year,
                'month': obj.month,
                'day': obj.day,
                'hour': obj.hour,
                'minute': obj.minute,
                'second': obj.second,
                'microsecond': obj.microsecond,
            }
        else:
            return JSONEncoder.default(self, obj)


# 2 read the config file raise 4 errors if needed
# 3 is inside
def read_config_raise_err():

    # Create the string to hold log file's value
    al_str = ''

    # Open the log file and put the values to al_str
    try:
       with open('access-log.txt', 'r') as read_file:
              al_str = read_file.read()

    except FileNotFoundError as err:
        print(err)


    # Decode the data.json file and put its values to data
    try:
        data = decode(open('data.json', 'r'))

    except FileNotFoundError as err:
        print(err)
    except json.JSONDecodeError as err:
        print(err)

    # Take the values of the keys for data 1 by 1
    # Set the loging level according to the configuration
    try:
        webserver_log = data['name_webserver_log']
        log_level = data['log_level']
        if log_level == 'Access-Log':
            log_level = '- -'

        else:
            log_level = '[error]'

        http_request_method = data['name_http_request_method']
        http_response_code = str(data['http_response_code'])
        response_byte_size = str(data['response_byte_size'])
        num_log_lines_to_display = str(data['num_log_lines_to_display'])

    except KeyError as err:
        print(err)

    # Find places in log file specified by the settings of json file
    idx = al_str.index(webserver_log)
    idx2 = al_str.index(response_byte_size)
    match = al_str[idx:idx2]

    # Create a list to hold the values each time we match
    matched_results = []

    # Find match objects as much as num_log_lines_to_display variable
    for i in range(1,int(num_log_lines_to_display)):
        if (log_level in match and http_request_method in match and http_response_code in match):
            matched_results.append(match)

        al_str = al_str.replace(match, 'foo')


    print(matched_results)


# 4 write a func to print all requests containing index.html
def print_all_index():
    al_str = ''
    try:
        with open('access-log.txt', 'r') as read_file:
            al_str = read_file.read()

    except FileNotFoundError as err:
        print(err)


    regex = re.compile(r'\]\s\"(\w+\s?)(\/index.+HTTP/1.1?)')
    matchList = regex.findall(al_str)

    print(matchList[:5])
    print()


    print()
    print("------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------")
    print()

    return matchList


# 5 Pring all requests with the method defined in config.json
def print_requests_in_the_config(list):
    json_dict = decode(open('data.json','r'))
    counter = 0
    for e in list:
        if e[0] == json_dict['name_http_request_method'] + ' ':
            counter += 1
            print(e)

    # What would you do if the number was less or equal to zero?
    if counter == 0:
        print()
        print('Number is less than or equal to zero')

# 6 is already done as # 1
# 7 is : Nowhere I already have try and catch blocks.
main()


