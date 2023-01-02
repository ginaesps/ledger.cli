#Imports
from os import read
import re
import argparse 
import datetime 
import collections
import numpy as np
from tabulate import tabulate
from colored import fg

data = []
transactions = []
bal = []
sort = False
balance = collections.defaultdic(float)
colorbal = collections.defaultdic(str)
exchange = collections.defaultdic(float)
red = fg('red')
blue = fg('blue')
black = fg('black')
defaultcurrency = '$'

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
----------- read_pricedb function() -----------
It compiles a regex pattern that matches a number with an optional decimal point and optional
comma separators that will be used to extract exchange rates from the file.
Inside the try block, where the file was found and is being read. 
If the line starts with N, it skips onto the next iteration. If the line starts with D, split
obtains the currency symbol and exchange rate from the line, and uses findall() to extract the
exchange rate, which is stored in the exchange dictionary using the currency symbol as key.
"""
def read_pricedb(filename):
    exchange['$'] = 1.0
    pattern = re.compile(r'\b\d[\d,.]*\b')#only looks up for numbers with optional symbols
    try:
        with open(filename) as f:
            for line in f.readlines():
                if line.startswith('N'):
                    continue

                if line.startswith('D'):
                    defaultcurrency = re.sub(pattern, '', line.split(' ', 1)[1]).strip()
                    #original string takes off the letter because it starts with 2nd position
                    #coincidence of the pattern is taken off
                    #strip allows defaultcurrency to only be the needed char(s)

                if line.startswith('P'):
                    # example: P 2012/11/25 05:04:00 AU $1751.90
                    symbol, exrate = line.split(' ', 3)[3].split(' ')
                    exchange[symbol] = float(re.findall(pattern, exrate)[0])
    except FileNotFoundError:
        print('Price-DB file not found, please check the file name')
        exit()


"""
----------- exchange_values function() -----------
transactions argument is a list of Transaction objects, exchange argument is a dictionary that maps
currency symbols to exchange rates, currency argument is a string representing the target currency to 
which the amounts should be converted.
If the currency of the transaction's amount isn't = as target, first it converts to USD and then to target
"""
def exchange_values(transactions, exchange, currency=defaultcurrency):
    if currency in exchange:
        for tr in transactions:
            if not tr.amount1[0] == currency:
                if not tr.amount1[1] == '$':
                    tr.amount1[1] *= exchange[tr.amount1[0]]
                    tr.amount1[0] = '$'

                tr.amount1[1] /= exchange[currency]
                tr.amount1[0] = currency

            if not tr.amount2[0] == currency:
                if not tr.amount2[1] == '$':
                    tr.amount2[1] *= exchange[tr.amount2[0]]
                    tr.amount2[0] = '$'

                tr.amount2[1] /= exchange[currency]
                tr.amount2[0] = currency
    else:
        print(red + 'Currency not found in Price-DB, please check the currency or update the Price-DB'
                + black + '\nPrinting the Report without exchange rates')


"""
----------- parse data function() -----------
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
----------- print_ledger function() -----------
Prints a list of transactions according to a specified sorting and filtering criteria.
Sort=str, specifies the sort type. Filters is a tuple of str that specifies the filtering.
When the function prints the date, comment, accounts and amounts. 
If abs(amount1) == abs(amount2), only account2 is printed. Otherwise, both are printed.
"""
def print_ledger(transactions, sort=None, *filters):
    if sort == 'date':
        print('Sorting by date...\n')
        transactions.sort(key=lambda x: x.date)
    elif sort == 'amount':
        print('Sorting by amount...\n')
        transactions.sort(key=lambda x: x.amount1)

    for t in transactions:
        if t.amount1[1] < 0:
            amount1 = red + t.amount1[0] + ' ' + '{:.2f}'.format(t.amount1[1]) + black
        else:
            amount1 = t.amount1[0] + ' ' + '{:.2f}'.format(t.amount1[1])
        if t.amount2[1] < 0:
            amount2 = red + t.amount2[0] + ' ' + '{:.2f}'.format(t.amount2[1]) + black
        else:
            amount2 = t.amount2[0] + ' ' + '{:.2f}'.format(t.amount2[1])

        print(str(t.date) + ' ' + '{:<30}'.format(t.comment))
        print('\t\t' + (blue + '{:30}'.format(t.account1) + black + '\t\t\t\t' + amount1))
        if abs(t.amount1[1]) == abs(t.amount2[1]):
            print('\t\t' + (blue + '{:30}'.format(t.account2) + black))
        else:
            print('\t\t' + (blue + '{:30}'.format(t.account2) + black) + '\t\t\t\t' + amount2)


"""
----------- register_ledger function() -----------
Prints a register of transactions. Takes in a list of transactions and optional arguments sort
and filters. Balance dictionary keeps track for each currency. 
For each transaction iteration, it formats the amount as a str with the correct symbol and color.
It then updates the balance for 1st and 2nd account in the transaction and appends relevant info
"""
def register_ledger(transactions, sort=None, *filters):
    headers = ['Date', 'Comment', 'Account', 'Amount', 'Balance']
    register = []
    balance = collections.defaultdic(float)

    if sort == 'date':
        print('Sorting by date...\n')
        transactions.sort(key=lambda x: x.date)
    elif sort == 'amount':
        print('Sorting by amount...\n')
        transactions.sort(key=lambda x: x.amount1)

    for t in transactions: #register
        if t.amount1[1] < 0:
            amount1 = red + t.amount1[0] + ' ' + '{:.2f}'.format(t.amount1[1]) + black
        else:
            amount1 = t.amount1[0] + ' ' + '{:.2f}'.format(t.amount1[1])
        if t.amount2[1] < 0:
            amount2 = red + t.amount2[0] + ' ' + '{:.2f}'.format(t.amount2[1]) + black
        else:
            amount2 = t.amount2[0] + ' ' + '{:.2f}'.format(t.amount2[1])
        
        #update balance for amount1
        balance[t.amount1[0]] += t.amount1[1]
        colorbal = colorbalance(balance)
        register.append([t.date, t.comment, blue + t.account1 + black, amount1, ''.join('%s\n'% (val) for (key, val) in colorbal.items())])

        #update balance for amount2
        balance[t.amount2[0]] += t.amount2[1]
        colorbal = colorbalance(balance)
        register.append(['', '', blue + t.account2 + black, amount2, ''.join('%s\n'% (val) for (key, val) in colorbal.items())])
        register.append(['- ', ' ', ' ', ' ', ' '])

    print(tabulate(register, headers))


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

if args.price_db:
    read_pricedb(args.price_db[0])
    exchange_values(transactions, exchange, args.price_db[1])

if args.command == 'print':
    print_ledger(transactions, sort)

if args.command in ['balance', 'bal']:
    balance_ledger(transactions)

if args.command in ['register', 'reg']:
    register_ledger(transactions, sort)