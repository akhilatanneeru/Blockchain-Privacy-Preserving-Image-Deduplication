from solcx import compile_source, install_solc
from web3 import Web3
import json

# Install Solidity compiler version
install_solc('0.8.19')

# Read Solidity contract
with open("contracts/ImageAudit.sol", "r") as file:
    contract_source_code = file.read()

# Compile contract
compiled_sol = compile_source(
    contract_source_code,
    output_values=['abi', 'bin'],
    solc_version="0.8.19"
)

# Extract contract interface
contract_id, contract_interface = compiled_sol.popitem()

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Check connection
if not w3.is_connected():
    raise Exception("Failed to connect to Ganache")

# Get first Ganache account
account = w3.eth.accounts[0]

# Create contract object
ImageAudit = w3.eth.contract(
    abi=contract_interface['abi'],
    bytecode=contract_interface['bin']
)

# Deploy contract
tx_hash = ImageAudit.constructor().transact({
    'from': account,
    'gas': 3000000
})

# Wait for transaction receipt
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Print deployed contract address
print("Contract deployed at:")
print(tx_receipt.contractAddress)

# Save contract details
with open("contract_data.json", "w") as f:
    json.dump({
        "abi": contract_interface['abi'],
        "address": tx_receipt.contractAddress
    }, f, indent=4)

print("Contract data saved successfully")