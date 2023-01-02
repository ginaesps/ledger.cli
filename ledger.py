#Imports
import argparse 
import datetime 
import numpy as np

data = []
transactions = []

"""
----------- Transaction class() -----------
The constructor includes date, comment, account1, amount1, account2 and amount2.
"""
class Transaction():
    def __init()__(self, date, comment, account1, amount1, account2, amount2=None):
        self.date = date
        self.comment = comment
        self.account1 = account1
        self.account2 = account2

        #if amount2=None, amount1 is acommodity or amount depending if it has a space.
        #either case, the amounts are lists with symbol/currency and value.
        if not amount2:
            if (' ' in amount1): #commodity
                amount = amount1.split(' ')
                self.amount1 = [amount[1], float(amount[0])]
                self.amount2 = [amount[1], float(amount[0])* -1 ]
            else: #amount
                if ('-' in amount1):
                    amount1 = amount1.replace('-','')
                    self.amount1 = [amount1[0], float(amount1[1:])* -1]
                    self.amount2 = [amount1[0], float(amount1[1:])]
                else:
                    self.amount1 = [amount1[0], float(amount1[1:])]    
                    self.amount2 = [amount1[0], float(amount1[1:])* -1]

        else:
            if ('-' in amount1):
                amount1 = amount1.replace('-', '')
                self.amount1 = [amount1[0], float(amount1[1:])* -1]
            else:
                self.amount1 = [amount1[0], float(amount1[1:])]

        if (' ' in amount2):
            amount = amount2.split(' ')
            self.amount2 = [amount[1], float(amount[0])]
        else: #Am2 amount
            if('-' in amount2):
                amount2 = amount2.replace('-','')
                self.amount2 = [amount2[0], float(amount2[1:])* -1]
            else:
                self.amount2 = [amount2[0], float(amount2[1:])]


class Main():
    pass


"""
----------- Node class() -----------
Each one is a building block for a tree data structure. The constructor includes 
children, balance and name.
"""
class Node():
    def __init__(self, name):
        self.children = []
        self.balance = collections.defaultdic(float)
        self.name = name


"""
----------- parse function() -----------
It iterates every 3 lines. For each iteration, it takes the 1st element, data[i], which
should contain the date, a comment and a newline char. It is split by space into date and 
comment. The date is converted to a datetime.date obj. 
datetime format: year, month, day
data[i+1] shoudl contain the name account and amount for account1. It splits and remove empty
elements from the resulting list.
data[i+2] should contain name account and amount for account2. If the list has only one element, 
it is assigned to account2 and sets amount2 = None
The result is a Transaction object with the extracted data
"""
def parse(data):
    for i in range(0, len(data), 3):
        data[i] = data[i].replace('/', '-').strip('\n')
        firstline = data[i].split(' ', 1)
        date = np.array(firstline[0].split('-')).astype(int)
        date = datetime.date(date[0], date[1], date[2])
        comment = firstline[1]

        secondline = data[i+1].strip('\n').split('\t')
        for item in secondline:
            if item == '':
                secondline.remove(item)
        account1 = secondline[0].strip()
        amount1 = secondline[1]

        thirdline = data[i+2].strip('\n').split('\t')
        for item in thirdline:
            if item == '':
                thirdline.remove(item)
        account2 = thirdline[0].strip()
        if len(thirdline) > 1:
            amount2 = thirdline[1]
        else
            amount2 = None

        transactions.append(Transaction(date, comment, account1, 
                            amount1, account2, amount2))


"""
----------- readFile function() -----------
reads a file and stores its lines in the data list.
the with statement opens the file and reads it line by line with for and readlines()
If the line starts with ! there's recursion with the filename after the ! and with 
the continue statement, skips to the next iteration.
If it doesn't start with ! or ; then the line appends()
"""
def readFile(filename):
        #with is for exception handling to simplify...
        #management of files
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith(';'):
                    continue
                if line.startswith('!include'):
                    readFile(line.split()[1]) #recursive
                    continue
                data.append(line)


#program description
arg_desc = '''\
        Let's keep track of your finance!
        --------------------------------
            This program is a simple recreation
            of a Ledger CLI with Python argparse!
        '''

#ArgumentParser adds arguments and parses them
parser = argparse.ArgumentParser(prog = 'ledger',
                                formatter_class = argparse.RawDescriptionHelpFormatter,
                                description= arg_desc)

#positional argument (needed to obtain information to work on)
parser.add_argument('-f', '--file', 
                    help='Input a file to read'
                    required=True)

#sort command
parser.add_argument('-s', '--sort',
                    help='Sort by amount, comment or date')

#prices database command
parser.add_argument('--price-db', nargs=2,
                    help='Load a prices database for your brokerage account')

#optional commands
parser.add_argument("command",
                    choices=['balance', 'bal', 'register', 'reg', 'print'],
                    help='Select a command to execute')

#Parse the arguments given as inputs 
args = parser.parse_args()

#calling function defined above depending on the input of commands and flags

if args.file:
    readFile(args.file)

else:
    readFile('index.ledger')

parse(data)

if args.sort == 'd' or args.sort == 'date':
    sort = 'date'
elif args.sort == 'a' or args.sort == 'amount':
    sort = 'amount'

#if args.price_db:

#if args.command == 'print':

#if args.command in ['balance', 'bal']:

#if args.command in ['register', 'reg']: