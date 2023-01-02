#package to build a CLI
import argparse

data = []

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