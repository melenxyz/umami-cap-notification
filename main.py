import json
from decimal import Decimal
from web3 import Web3
import discordWH
#import twitter


vaults = json.loads(open("vaults.json", 'r').read()) #Loads Cauldrons.json as a nested dic


def checkTreshold(previous_amount, amount, treshold):
    if amount - previous_amount > treshold: #check if the increase is > treshold
        if previous_amount == 0: #if previousAmount is "pure" 0, we send message
            return True
        elif amount - previous_amount > Decimal(0.001) * previous_amount: #check wether the increase is at least a 30% increase
            return True
        else:
            return False

def getAvailableSpace(vault):
    totalDeposited = vault.functions.checkpointTotalBalance().call()
    cap = vault.functions.cap().call()
    return cap - totalDeposited


for tokens in vaults.keys(): #Go through each Cauldron entry
    w3 = Web3(Web3.HTTPProvider(vaults[tokens]['RPC'])) #Network RPC
    vault = w3.eth.contract(address=w3.toChecksumAddress(vaults[tokens]['address']), abi=json.load(open('vaultABI.json', 'r')))
    available=getAvailableSpace(vault) #Gets MIM available for the cauldron
    if checkTreshold(Decimal(vaults[tokens]['previous_amount']), Decimal(available), Decimal(vaults[tokens]['threshold'])): #Compare amount with previous amount and check if above threshold, defined per chain
        print("%s vault:" %(tokens))
        print("Old amount : ", vaults[tokens]['previous_amount'])
        print("New amount : ", available)
        print("-----")
        
        try:
            discordWH.sendMessage(tokens, available, vaults) #Send discord msg
        except:
            print("error sending discord message")
        #twitter.tweet(tokens, amount, settings, chain)
 
    vaults[tokens]['previous_amount']=str(available) #Store amount as Previous_amount
    
json.dump(vaults, open("vaults.json", 'w'), indent=4, sort_keys=True)
