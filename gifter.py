# gifter.py version 0.2014.0
#
# reads a text file of names and emails, builds a directed graph with
# single out degree and single indegree (permutation) and ensures no
# reciporical edges; outputs a textfile be copied into email
#
# NEW THIS VERSION:
#   - everything; idea migrated from matlab code
#
# FOR NEXT VERSION:
#   - couples constraints
#   - automated email
#
# FOR SOME FUTURE VERSION:
#
# usage:
#        > python gifter.py <options-list>
#
# example:
#   > python gifter.py -seed 20141123 -inFname usbank2014.in -outFname usbank2014.out
#
# options:
#
#  -seed       <int>     seed for random number generator
#  -inFname    <str>     input csv file
#  -outFname   <str>     output text file
#  -optsFname  <str>     file for input options
#



#import numpy as np
#import scipy
#import scipy.io
#import matplotlib
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt
import sys

import numpy.random as random
from email.mime.text import MIMEText
import smtplib

import sb

def ensurelist(listorother):
  if type(listorother).__name__ == 'list':
    return listorother
  else:
    return [listorother]

def sendEmail():
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except Exception:
        print('An error occurred: %s' % Exception)

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


# initialize class to read options
options = sb.oneliner()
options.helpmsg = ('usage: \n       > python baroc.py <options-list>\n'+
    'example:'+
    '\noptions:\n')
options.addopt('seed',                   -1,'seed for random number generator','int')
options.addopt('inFname',      'infileKid.in','input filename for matrix','str')
options.addopt('outFname',    'outfileKid.out','output filename for matrix','str')
options.addopt('optsFname',            None,'options file','str')

# read in commandline to get options filename, help
options.parsecmd(sys.argv)

# if help is specified, do the help message
if options.getopt('help'):
  options.printopts()
  sys.exit(0)

# overide default options from file
if options.getopt('optsFname') != None:
  options.parsefile(options.opts['optsFname'][1])

# re-read the commandline to override filename options
options.parsecmd(sys.argv)

# TODO incorporate many of the following standard functionalities into oneliner class
# TODO handle deprecated options in oneliner class

# import options to local variable names
seed       = options.getopt('seed')
inFname    = options.getopt('inFname')
outFname   = options.getopt('outFname')
optsFname  = options.getopt('optsFname')

if seed is -1:
   print('seed is set to -1, or no seed given')
else:
   random.seed(seed)



bar = '\n\n###########################################################################\n\n'

f = open(inFname,'r')

f2 = open(outFname, 'w')

# read names from file
k=0
name_email = {}
for line in f:
#    print('Line: ',line)
    name_email[k] = line.split()
    k = k+1
#print(name_email)

# randomly choose assingnments
satisfied = 0
full_list = range(k)
count = 0
maxTries = 500
while not satisfied and count<maxTries:
#    print('trial %d' % count)
    receiver  = {}
    remainder = list(full_list)

    for i in range(k):
        receiver[i] = remainder.pop(random.randint(0,len(remainder)))

    # check
    satisfied = 1
    for i in range(k):
        print(i, name_email[i][0],name_email[receiver[i]][-1])
        if receiver[i] == i: #giving to themself
            print("Trial {}: Giving to Themself".format(count))
            satisfied = 0
            break
        if receiver[receiver[i]] == i: #giving to the giver
            print("Trial {}: Giving to Giver".format(count))
            satisfied = 0
            break
        if name_email[receiver[i]][0] == name_email[i][2]: #giving to SigOther
            print("Trial {}: Giving to SO, {} to {}".format(count,name_email[receiver[i]][0],name_email[i][0]))
            satisfied = 0
            break
        if name_email[receiver[i]][0] == name_email[i][-1]:#giving to last year
            print("Trial {}: Giving same as Last Year, {} to {}".format(count,name_email[receiver[i]][0],name_email[i][0]))
            satisfied = 0
            break
        if name_email[receiver[i]][0] == name_email[i][-2]:#giving to 2 years ago
            print("Trial {}: Giving same as 2 Years Ago, {} to {}".format(count,name_email[receiver[i]][0],name_email[i][0]))
            satisfied = 0
            break

    count += 1
if count>=maxTries:
    print('Too many attempts')
    sys.exit()
print('Reveiver:',receiver)



# output assignments to file


# first a summary, both to screen and to file
print('Summary:')
f2.write('\nSummary:\n\n')

for i in range(k):

  print(name_email[i][0].ljust(15)+' gives a gift to     '+name_email[receiver[i]][0])
  f2.write(name_email[i][0].ljust(15)+' gives a gift to     '+name_email[receiver[i]][0]+'\n')



# then the text for the individual emails
#for i in range(k):
#  f2.write(bar)
#  message = MIMEText('\nTo:\n\n'+name_email[i][1]+'\n\n'+
#          'Dear '+name_email[i][0]+',\n'+
#          '     You are invited to participate in the holiday gift exchange.    Your assignment is to give a gift to '+name_email[receiver[i]][0]+' with approximately value of $100.\n\n'+
#          '              Sincerely,\n'+
#          '              The Gift-Exchange-O-Matic, version 0.2017.0\n')
#  message['to'] = 'ngreeney@gmail.com'
#  message['from'] = 'ngreeney@gmail.com'
#  message['subject'] = 'Sanders Xmas Exchange'
#  raw = base64.urlsafe_b64encode(message.as_string())



f.close()
f2.close()
