import sys
import re

rawData = []
param = {}
dictiRequestNum = {}

def run():
    out = read_log()
    ip_requests_number()
    ip_find()
    longest_request()
    print(non_existent(out))


# Reads from stdin and returns a categorized dictionary
def read_log():

    # Reading raw data from standard input
    for line in sys.stdin:
        rawData.append(line)

    # Find necessary part of the data using regex
    wholeRegex = re.compile(r'((\d|\d\d|\d\d\d).(\d|\d\d|\d\d\d).(\d|\d\d|\d\d\d).(\d|\d\d|\d\d\d)\s\-.*?\s(\d+)\s(\d+|-))')
    rawWhole = wholeRegex.findall(str(rawData))

    # Removing data with unacceptable standards and make a clean list: correctRequests
    correctRequests = []
    for e in rawWhole:
        if('HTTP/1.1' in e[0]):
            correctRequests.append(e[0])

    # Find Ip addresses inside correctRequests and make a list of them : ipList
    ipRegex = re.compile(r'(\d+)\.(\d+)\.(\d+)\.(\d+)\s\-')
    ipTuple = ipRegex.findall(str(correctRequests))
    ipListBeforeConcat = []
    ipList = []
    for e in ipTuple:
        ipListBeforeConcat.append(list(e))

    for e in ipListBeforeConcat:
        str1 = ""
        for e1 in e:
            str1 += e1 + "."
        ipList.append(str1[:-1])


    # For all the otherdata which are requests, https, sizes I make a list called otherData
    otherRegex = re.compile(r'("\w\w\w+\s.+?1"\s\d+?\s(\d+|-))')
    otherDataBeforeConcat = otherRegex.findall(str(correctRequests))
    otherData = []

    for e in otherDataBeforeConcat:
        otherData.append(str(e[0]))

    # For the request part I made a requestList
    requestRegex = re.compile(r'".+?"')
    requestData = requestRegex.findall(str(otherData))
    requestList = []

    for e in requestData:
        temp = e.replace('"', '')
        requestList.append(temp)

    # For the http codes I made httpList
    # For the byte size I made sizeList
    httpRequest = re.compile(r'("\s(\d+)\s(\d+|-))')
    httpData = httpRequest.findall(str(otherData))
    httpList = []
    sizeList = []


    for e in httpData:
        httpList.append(e[1])
        sizeList.append(e[2])


    # creating dictionary

    for idx, e in enumerate(ipList):
        if (e not in param.keys()):
            param[e] = [requestList[idx], httpList[idx], sizeList[idx]]
        elif (e in param.keys()):
            param[e] = param[e] + [requestList[idx], httpList[idx], sizeList[idx]]


    return param


# For a given ip address, create a data structure that keeps the number of for the given ip return this structure
def ip_requests_number():
    keys = param.keys()

    for e in keys:
        dictiRequestNum[e] = len(param[e]) / 3

    return dictiRequestNum



# if called ip_find(most_active=True) return the biggest number of requests
# if called ip_find(most_active=False) return the smallest number of request
# there could be many IP addresses with the same number of requests.
def ip_find(most_active=True):
    if most_active:
        temp = 0
        for e in param.keys():
            if temp < dictiRequestNum[e]:
                temp = dictiRequestNum[e]
        return temp
    else:
        temp = 10
        for e in param.keys():
            if temp > dictiRequestNum[e]:
                temp = dictiRequestNum[e]
        return temp


# Request longest request string for exp GET /index.html along with its ip address.
# If there are many choose the arbitrarly / as you wish
def longest_request():
    ip = ""
    temp = ""

    for e in param.keys():
        if len(param[e]) == 3:
            if len(temp) < len(param[e][0]):
                temp = param[e][0]
                ip = e
        else:
            steps = len(param[e]) / 3
            counter = 0

            while(counter < steps):
                if len(temp) < len(param[e][counter * 3]):
                    temp = param[e][counter * 3]
                    ip = e
                counter += 1

    return [ip, temp]

# Returns all request strings with HTTP result code Page not found.
# Each request string should appear just once
def non_existent(param):

    result = set()
    for e in param.keys():
        if len(param[e]) == 3:
            if param[e][1] == '404':
                result.add(param[e][0])

        else:
            steps = len(param[e]) / 3
            counter = 0
            while counter < steps:
                if param[e][counter * 3] == '404':
                    result.add(param[e][counter * 3])
                counter += 1

    return list(result)




run()