import smtplib, ssl, datetime, argparse
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

def run():

    content_dict = read_stdin()

    #Check if user don't use any option
    if content_dict == None:
        raise Exception('Options aren\'t used')

    #Checks if more than one option is used
    ctr = 0
    for e in content_dict:
        if content_dict[e] != None:
            ctr += 1

    if ctr != 1:
        raise Exception('Too many options are used use only 1')

    if 'mail' in content_dict.keys() and content_dict['mail'] != None:
        # Format the text and remove curly braces
        message_txt = str(content_dict['mail'])[2:-2]
        send_mail(message_txt)





    try:
        if 'cat_facts' in content_dict.keys() and content_dict['cat_facts'] != None:
            cat_facts(int(content_dict['cat_facts'][0]))

        if 'teachers' in content_dict.keys() and content_dict['teachers'] != None:
            display_teachers(content_dict['teachers'][0])
    except IndexError as ie:
        print('bla bla')
        print(ie.__cause__)




def read_stdin():

    parser = argparse.ArgumentParser()
    parser.add_argument('--mail', help='Send a mail to the teacher',
                        action='store', required=False, nargs=1)
    parser.add_argument('--cat-facts', help='Shows an interesting fact about cats choose between 1 and 5',
                        action='store', required=False, nargs=1)
    parser.add_argument('--teachers', help='Display a list of teacher starting with a given letter',
                        action='store', required=False, nargs=1)

    args = parser.parse_args()


    if vars(args).get('mail') != None:
        return vars(args)

    if vars(args).get('cat_facts') != None:
        return vars(args)

    if vars(args).get('teachers') != None:
        return vars(args)


def send_mail(message_txt):

    try:
        secret = ""
        with open('secret.txt', 'r') as file:
            secret = file.read()
    except FileNotFoundError as fnf:
        print(fnf)

    sender_email = secret.split(" ")[0]
    password = secret.split(" ")[1]
    port = 465
    receiver_email = "bogumila.hnatkowska@pwr.edu.pl"

    message = MIMEMultipart("alternative")
    message["Subject"] = str(datetime.datetime.now())
    message["From"] = sender_email
    message["To"] = receiver_email

    text = message_txt

    textObject = MIMEText(text, "plain")
    message.attach(textObject)

    # Create a secure ssl Context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


def cat_facts(fact_num):

    if fact_num < 1 or fact_num > 5:
        raise IndexError('Please enter a number between 1 and 5')

    r = requests.get('https://cat-fact.herokuapp.com/facts/')
    text = r.json()[fact_num - 1]['text']
    print(text)


def display_teachers(letter):

    if len(letter) != 1:
        raise Exception('Please enter just one character')

    if letter.isnumeric():
        raise Exception('Please enter a character not an int')

    url = 'https://wiz.pwr.edu.pl/pracownicy?letter=' + letter.upper()
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    cards = soup.findAll('div', {'class': 'col-text text-content'})

    nameList = []
    mailList = []

    for e in cards:
        nameList.append(e.findChildren('a', recursive=False)[0].text)
        mailList.append(e.findChildren('p', recursive=False)[0].text)

    for idx, e in enumerate(nameList):
        print(e + " -> " + mailList[idx][7:])

    if len(nameList) == 0:
        print(f'Sorry we couldn\'t find anyone starting with letter {letter}')


run()
