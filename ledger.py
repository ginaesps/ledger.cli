#package to build a CLI
import argparse

#to get to target directory
from pathlib import Path

transactions = [];


def LGregister(): #accounts, options
    #print(getTransactions(options.F))
    print("reg funct")

def LGbalance(): #accounts, options
    #print(getTransactions(options.F))
    print("bal funct")
    print(parser.parse_args())

def LGprint():
    #print(getTransactions(options.F))
    print("print func")


def getTransactions():
    with open(filename) as file:
        while (line := file.readline().rstrip()):
            print(line)
    # cada que se acabe una transaction        
    transactions.push(file)        


#program description
arg_desc = '''\
        Let's keep track of your finance!
        --------------------------------
            This program is a simple recreation
            of a Ledger CLI with Python argparse!
        '''

#ArgumentParser adds arguments and parse them
#parser will be set with parse_args()
    #this method will be wraped with vars() to avoid errors
parser = argparse.ArgumentParser(prog = 'ledger',
                                formatter_class = argparse.RawDescriptionHelpFormatter,
                                description= arg_desc)

#positional argument
###############################check how to indicate or run the name of the file
parser.add_argument('filename')

#register command
parser.add_argument('-reg', '--register', 
                    help='prints all the transactions and the running total',
                    action=LGregister())      # option that takes a value

#balance command
parser.add_argument('-bal', '--balance', 
                    help='prints the balances of your journal accounts',
                    action=LGbalance())      # option that takes a value

#print command
parser.add_argument('-p', '--print', 
                    help='prints transactions in a textual format parsed by ledger',
                    action=LGprint())      # option that takes a value

#path command
parser.add_argument("--path", type=Path, default=Path(__file__).absolute().parent, help="Path to the target directory")
 
args = vars(parser.parse_args())
print(args)
print("hasdofaisdf")

#if args["-bal"]:
#    print(args)

#options
parser.add_argument('--price-db',
                    help='The fiel for the prices database')
parser.add_argument('--file', '-f <string....>',
                    help='The fiel for the prices database')
parser.add_argument('-s', '--sort',
                    help='Sort a report')