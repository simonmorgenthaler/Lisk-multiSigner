#!/usr/bin/python

####################################################################################################################
# File name: multiSigner.py                                                                                        #
# Author: cc001                                                                                                    #
# Last modified: 2017-04-16                                                                                        #
#                                                                                                                  #
# This script is used to automatically sign multiple pending multisig-transactions in a specific account.          #
# Adapt NODE, PUBKEY, SECRET to your needs before using the script.                                                #
#                                                                                                                  #
# If you like and use this script, please vote for 'cc001' 6787154358850114730L as Delegate Lisk mainnet, Thanks!  #
####################################################################################################################

import json
import requests
from sys import version_info

#### ADAPT THESE VARIABLES TO YOUR NEEDS/CONFIG ####

# Node to connect to. Recommended to use your own node or a node you trust
NODE = "https://my.node.io"

# Publickey of the account which contains the Multisig transactions.
# This is not your account you are using to sign the transactions.
PUBKEY = "CHANGE_ME"

# This is the secret of the account you use to sign the transactions.
# It must be registered as on of the signing accounts
SECRET = "CHANGE_ME"

#### DON'T CHANGE ANYTHING BELOW THIS LINE ####

SATOSHI = 100000000.0

# COLORS
OK = '\033[92m'
ERROR = '\033[91m'
STANDARD = '\033[0m'


def getAnswer(query):
    answer = ""
    try:
        response = requests.get(url=query, timeout=5)
        answer = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        answer = []
    except ValueError, e:
        print "Not allowed"
        answer = []
        
    return answer
    
def postServer(query, payload):
    try:
        response = requests.post(query, data=payload)
        answer = json.loads(response.text)
        if answer and 'success' in answer and answer['success']:
            print OK + "SUCCESS" + STANDARD
        else:
            print ERROR + "ERROR: " + answer['error'] + STANDARD
    except requests.exceptions.ConnectionError as e:
        print "Error:", e.message

    
def getPendingMultisigTransactions():
    transactions = None
    query = NODE + "/api/multisignatures/pending?publicKey=" + PUBKEY 
    answer = getAnswer(query)
    if answer and 'success' in answer and answer['success']:
        transactions = answer['transactions']
    return transactions
    
def signMultisigTransaction(transactionId):
    query = NODE + "/api/multisignatures/sign"
    print "Signing transaction {:>22}: ".format(transactionId),
    payload = {'secret': SECRET, 'transactionId': transactionId}
    postServer(query, payload)
    

if NODE == "https://my.node.io" or PUBKEY == "CHANGE_ME" or SECRET == "CHANGE_ME":
    print "Please adapt NODE, PUBKEY, SECRET to your needs before running this script."
    exit(1)

transactions = getPendingMultisigTransactions()

if transactions == None:
    print ERROR + "ERROR:\nNo valid NODE ("+NODE+") or\nNo valid PUBKEY ("+PUBKEY+")" + STANDARD
    exit(1)
if len(transactions) == 0:
    print "No pending multisig transactions"
    exit(1)

print ""
print str(len(transactions)) + " pending multisig transactions:"
print ""
template_header = "{:25}|{:25}|{:25}|{:>18}|{:>12}"
template = "{:25}|{:25}|{:25}|{:>14.4f} LSK|{:>12}"
line = "-------------------------------------------------------------------------------------------------------------"
print template_header.format("TransactionId", "Sender", "Recipient", "Amount", "Signatures");
print line

for transaction in transactions:
    
    txId = transaction['transaction']['id']
    sender = transaction['transaction']['senderId']
    recipient = "-"
    if 'recipientId' in transaction['transaction']:
        recipient = transaction['transaction']['recipientId']
    nmbrSignatures = len(transaction['transaction']['signatures'])
    neededSignatures = transaction['min']
    amount = float(transaction['transaction']['amount']) / SATOSHI
    
    print template.format(txId, sender, recipient, amount, str(nmbrSignatures) + "/" + str(neededSignatures))

py3 = version_info[0] > 2

question = "Sign these transactions?: [y/N] "
yes = set(['yes','y'])

print ""
if py3:
    answer = input(question).lower()
else:
    answer = raw_input(question).lower()

if answer in yes:
    print ""
    for transaction in transactions:
        txId = transaction['transaction']['id']
        signMultisigTransaction(txId)
    print ""
else:
    print "Aborted"

    


