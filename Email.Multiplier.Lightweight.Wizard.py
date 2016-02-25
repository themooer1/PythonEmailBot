import random
import string
import smtplib
import email
import time
import sys
import imaplib
import getpass
import datetime
listeningInbox= raw_input("Please enter full listening email address.")
listeningInboxPass=raw_input("Please enter listening inbox password.")
listeningMailServer=raw_input("Please enter the email server for the listening mail account (e.g imap.gmail.com:993).")
sendingInbox=raw_input("Please enter sending inbox password.")
sendingInboxPass=raw_input("Please enter sending inbox password.")
sendingMailServer=raw_input("Please enter the email server for the sending mail account (e.g smtp.gmail.com:587).")
print 'Initializing Server!'
users = string.split(open('users.txt','r').read())
print "Authenticated users are...\n"
for user in users:
    print user + '\n'






def getmail(server,login,password):
    mailbox = imaplib.IMAP4_SSL(server)
    mailbox.login(login,password)
    mailbox.select('INBOX')
    return mailbox


def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    emails = []
    subjects = []
    senders = []
    sendersparsed = []
    bodiesparsed = []
    bodies = []
    messages = []
    if rv != 'OK':
        print "No messages found!"
        return
    for num in data[0].split():
        rv, data = M.fetch(num, "(BODY[HEADER.FIELDS (SUBJECT)])",)
        if rv != 'OK':
            print "ERROR getting message", num
            return
        rv,body = M.fetch(num, "(UID BODY[TEXT])")
        if rv != 'OK':
            print "ERROR getting message", num
##            print str(body) + '\n\n\n'
            return
        rv,sender = M.fetch(num, '(BODY[HEADER.FIELDS (FROM)])')
        if rv != 'OK':
            print "ERROR getting message", num
##            print str(sender) + '\n\n\n' 
            return
        M.store(num, '+FLAGS', '\\Deleted')
        M.expunge()
        emails.append(data)
        bodies.append(body)
        senders.append(sender)
    for sub in emails:
        sub = str(sub)
        begin = string.find(sub,":") + 1
        end = sub.find("\\r", begin)
        subject = sub[begin:end]
        subjects.append(subject)
    for body in bodies:
        if body == ')':
            break
        body = str(body[0][1])
        begin = string.find(body,", '") + 1
        end = body.find("\r", begin)
        body = body[begin:end]
        bodiesparsed.append(body)
    for sender in senders:
        sender = str(sender[0][1])
        begin = string.find(sender,"<") + 1
        end = sender.find(">", begin)
        sender = sender[begin:end]
        sendersparsed.append(sender)
    M.logout()
    return (subjects,sendersparsed,bodiesparsed)
def runjobs():
    mailbox = getmail(listeningMailServer,listeningInbox,listeningInboxPass)
    contents = process_mailbox(mailbox)
    bodies = contents[2]
    senders = contents[1]
    contents = contents[0]
    subjects = []
    emails = []
    subjects = []
    amount = []
    if contents == []:
        return

    for content in contents:
        i = contents.index(content)
        content = string.split(content)
        for j in content:
            if "@" in j:
                emails.append(j)
            elif j.isdigit():
                amount.append(j)
            else:
                subjects.append(str(j) + ' ')
        sender = str(chooseword(wordlist)) + '@THeCOWsMUStEAt.com'
        if senders[i] not in users:
            print "Sender {0} not authorized to use this server".format(senders[i])
            pass
        else:
            message = prepare_message(subjects[i],bodies[i],emails[i],amount[i])
            sendmail(int(amount[i]),sender,emails[i],message)
            print "Job Completed!"
    print "All jobs completed successfully!"

def prepare_message(Subject,Message,to,amount):
    wordlist = load_words()
    sender = str(chooseword(wordlist)) + '@THeCOWsMUStEAt.com'
    message = """From: ONE ANGRY COW <{0}>
    To: YOU WHO DISPLEASED THE COWS! <{3}>
    Subject: {1}

    {2}


    """.format(fromemail,Subject,Message,to) + str(chooseword(wordlist)) + str(random.random())
    return message

count = 0

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    return wordlist


def chooseword(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()




def sendmail(HOWMUCH, senders, receivers, message):
    print "Sendmail triggered"
    i = 0
    print "Connected!"
    server = smtplib.SMTP(sendingMailServer)
    server.starttls()
    server.login(sendingInbox,sendingInboxPass)
    print " Login Successful!"
    while i < HOWMUCH:
        try:
            server.sendmail(senders,receivers,message)
            print "Message Sent!"
            senders = 'thecowsmusteat' + str(random.choice(range(1,7)))+'@thecowsmusteat.bugs3.com'
            i = i + 1
        except:
            print "Waiting for reconnect..."
            time.sleep(121)
    server.quit()
    print("Sent " + str(HOWMUCH) + " messages to " + str(receivers))
print 'Server started and listening on port 995.'
while True:
    runjobs()
    time.sleep(300 + random.random() * 15)
