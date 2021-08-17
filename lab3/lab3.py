import sys
import logging
import math

logging.basicConfig(level=logging.DEBUG)

list1 = []
list2 = []
list3 = []

def run():
    temp = read_log()
    print("Call # 1")
    print(successfull_reads(temp))
    print()
    print("Call #2")
    print(failed_reads(temp))
    print()
    print("Call #3")
    print_html_entries(temp)



def read_log():
    lineNumCount = 0
    for line in sys.stdin:
        list1.append(line)
        lineNumCount += 1

    logging.debug('The number of lines in log.txt -> ' + str(lineNumCount))

    for ele in list1:
        if '\n' in ele:
            list2.append(ele[:-1])
        else:
            list2.append(ele)

    temp0 = []
    temp1 = []
    temp2 = []

    for ele in list2:
        ele = ele.split()
        temp0.append(ele[0])
        temp1.append(int(ele[1]))
        temp2.append(int(ele[2]))

    list3.append(tuple(temp0))
    list3.append(tuple(temp1))
    list3.append(tuple(temp2))

    return list3
    logging.debug('The number of entries in the list is -> ' + str(len(list2)))


def successfull_reads(list):
    tempList = []
    for idx,ele in enumerate(list[1]):
        if math.floor(ele/100) == 2:
            tempList.append(list[0][idx])

    return tempList

def failed_reads(list):
    temp4 = []
    temp5 = []
    for idx,ele in enumerate(list[1]):
        if math.floor(ele/100) == 4:
            temp4.append(list[0][idx])
        elif math.floor(ele/100) == 5:
            temp5.append(list[0][idx])

    logging.info('Number of entries for 4xx -> ' + str(len(temp4)))
    logging.info('Number of entries for 5xx -> ' + str(len(temp5)))

    return temp4 + temp5


def html_entries(list):
    temp = []

    for ele in list[0]:
        if ele[-5:] == '.html':
            temp.append(ele)

    return temp


def print_html_entries(list):
    temp = []

    for ele in list[0]:
        if ele[-5:] == '.html':
            temp.append(ele)

    print(temp)

run()

print_html_entries(list3)


# successful_reads, failed_reads, html_entries can be called multiple times
# run() and read_log() are just to be called 1 time in the beginning
