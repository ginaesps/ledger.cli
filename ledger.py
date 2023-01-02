#package to build a CLI
import argparse

transactions = [];

#function to read the file
def readFile(fileName):
    #try tests a block of code for errors 
    try:
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
    except FileNotFoundError:
        print('File not found, please check the file name')
        exit()


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