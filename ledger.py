#Imports
import argparse 
import datetime 
import collections
import numpy as np
from tabulate import tabulate
from colored import fg

data = []
transactions = []
bal = []
balance = collections.defaultdic(float)
colorbal = collections.defaultdic(str)
red = fg('red')
blue = fg('blue')
black = fg('black')

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
----------- readFile function() -----------
reads a file and stores its lines in the data list.
the with statement opens the file and reads it line by line with for and readlines()
If the line starts with ! there's recursion with the filename after the ! and with 
the continue statement, skips to the next iteration.
If it doesn't start with ! or ; then the line appends()
"""
def readFile(filename):
        #with is for exception handling to simplify management of files
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith(';'):
                    continue
                if line.startswith('!include'):
                    readFile(line.split()[1]) #recursive
                    continue
                data.append(line)

                
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
----------- colorbalance function() -----------
Takes in a dictionary of balances and returns a copy with formatted values to display 
the currency symbol and two decimal places. If -value, red output.
Formatting done with str.format() and ANSI escape codes for text color
"""
def colorbalance(balance):
    colored = balance.copy()
    for key in colored:
        if colored[key] < 0:
            colored[key] = red + key + ' ' + '{:.2f}'.format(colored[key]) + black
        else:
            colored[key] = key + ' ' + '{:.2f}'.format(colored[key])
    return colored


"""
----------- print_node function() -----------
Takes in a node object and prints the name and balance, as well as from the children
recursively. First, a copy of colorbal is created (node's bal dict) and formats balance values
with colorbalance(). If node has only one child, it appends a list with the balance and concatenation
of info to bal list. Otherwise, it apends same as before plus print_node() on each child
"""
def print_node(node):
    colorbal = colorbalance(node.balance)
    
    if len(node.children) == 1:
        bal.append([''.join('%s\n'% (val) for (key, val) in colorbal.items()),
            blue + node.name + ':' + node.children[0].name + black])
    else:
        bal.append([''.join('%s\n'% (val) for (key, val) in colorbal.items()),
            blue + node.name + black])
        for childnode in node.children:
            print_node(childnode)


"""
----------- balance_ledger function() -----------
Takes a list of transactions and optional filters as input, prints the balance of accounts.
It creates a tr list with tr account1, amount1, account2 and amount2. For each element, the 
balance is updated for the main tree and current node by adding amount(1 or 2).
For each subaccount obtained from the account's name, the function checks if it exist as a
child of the current node so that it can set the current node as that child or creates a new one
and adds it as a child of the current node and updates the balance of current node.
When all transactions have been processed, the function sorts the children of root by name and
print_node on each child. Finally, it prints the balance of the root node and all its children with tabulate()
"""
def balance_ledger(transactions, *filters):
    tree = Main()
    currentnode = Node('root')
    tree.root = currentnode

    for t in transactions:
        tr = [[t.account1, t.amount1], [t.account2, t.amount2]]

        for i in tr: #update main tree balance
            currentnode.balance[i[1][0]] += i[1][1]

            for account in i[0].split(':'):
                account = account.strip()
                nextnode = None

                for child in currentnode.children:
                    if child.name == account:
                        nextnode = child
                        break
                if nextnode:
                    currentnode = nextnode
                else:
                    newnode = Node(account)
                    currentnode.children.append(newnode)
                    currentnode = newnode
                
                #update currentnode balance
                currentnode.balance[i[1][0] += i[1][1]]
            
            currentnode = tree.root
        
        tree.root.children.sort(key=lambda x: x.name)
        headers = ['Balance', 'Account']

        for x in tree.root.children:
            print_node(x)

        bal.append(['----------------', ' ']) #append root balance
        colorbal = colorbalance(tree.root.balance)
        bal.append([''.join('%s\n'% val for (key, val) in colorbal.items()),
                    ' '])
        print(tabulate(bal, headers))


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