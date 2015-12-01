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

import sb

def ensurelist(listorother):
  if type(listorother).__name__ == 'list':
    return listorother
  else:
    return [listorother]


# initialize class to read options
options = sb.oneliner()
options.helpmsg = ('usage: \n       > python baroc.py <options-list>\n'+
    'example:'+
    '\noptions:\n') 
options.addopt('seed',                   -1,'seed for random number generator','int')
options.addopt('inFname',      'infile.dat','input filename for matrix','str')
options.addopt('outFname',    'outfile.dat','output filename for matrix','str')
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
    print('Line: ',line)
    name_email[k] = line.split()
    k = k+1
print(name_email)

# randomly choose assingnments  
satisfied = 0
full_list = range(k)
count = 0
while not satisfied and count<100:
    print('trial %d' % count)
    receiver  = {} 
    remainder = list(full_list)
    
    for i in range(k):
        receiver[i] = remainder.pop(random.randint(0,len(remainder)))
    
    # check
    satisfied = 1 
    for i in range(k):
        if receiver[i] == i: #giving to themself
            satisfied = 0
        if receiver[receiver[i]] == i: #giving to the giver
            satisfied = 0
        if name_email[receiver[i]][-1] == name_email[i][-1]: #giving to SigOther
            satisfied = 0

    count += 1
if count>=100:
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
for i in range(k):
  f2.write(bar)
  f2.write('\nTo:\n\n'+name_email[i][1]+'\n\n')
  f2.write('Dear '+name_email[i][0]+',\n')
  f2.write('     You are invited to participate in the holiday gift exchange.    Your assignment is to give a gift to '+name_email[receiver[i]][0]+'.\n\n')
  f2.write('              Sincerely,\n')
  f2.write('              The Gift-Exchange-O-Matic, version 0.2014.0\n')



f.close()
f2.close()



