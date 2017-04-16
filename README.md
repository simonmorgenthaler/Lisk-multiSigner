# Lisk-multiSigner
This script is used to automatically sign multiple pending multisig-transactions in a specific account.
After executing it, it will list the pending multisig transactions in this account and will ask you if you want to sign all these transactions in one batch.

### Screenshot
![Screenshot](screenshot.png?raw=true "Screenshot")

## Installation

### Installing needed python modules:
`sudo apt-get install python-requests`

If you start the script with missing modules it will tell you which modules you have to install.

### Cloning github repo
`git clone https://github.com/simonmorgenthaler/Lisk-multiSigner.git`

### Make script executable
`chmod +x multiSigner.py`


## Configuration
Before executing the script you have to adapt the file multiSigner.py
Open the file with a text editor and adapt the following three variables:

### NODE
Enter here the url of the node you want to use to sign your transactions. It is recommended to use your own node, or only a node you really trust
### PUBKEY
Entere here the publickey of the account which holds the multisign transactions. This is not the publickey of your own account.
### SECRET
Enter here your secret to sign the multisig transactions. This is the secret of your own account.


## Usage
Execute the script with `./multiSigner.py`
It will list the pending multisign transactions and will ask you if you want to sign all of them.
If you answer with `y` (for yes), it will sign the transactions.
If you answer anything else it will abort.


