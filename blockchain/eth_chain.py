import json
from pathlib import Path

from web3 import Web3

GANACHE_RPC = "http://127.0.0.1:7545"
CONTRACT_DATA = Path("contract_data.json")


def _load_contract():
    if not CONTRACT_DATA.exists():
        raise FileNotFoundError(
            "contract_data.json not found. Run deploy_contract.py first."
        )

    with open(CONTRACT_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    w3 = Web3(Web3.HTTPProvider(GANACHE_RPC))
    if not w3.is_connected():
        raise ConnectionError("Cannot connect to Ganache at 127.0.0.1:7545")

    contract = w3.eth.contract(
        address=Web3.to_checksum_address(data["address"]),
        abi=data["abi"],
    )
    return w3, contract


def record_file_on_chain(file_id_hex: str) -> str:
    w3, contract = _load_contract()
    account = w3.eth.accounts[0]

    file_id_bytes = bytes.fromhex(file_id_hex)
    tx_hash = contract.functions.recordFile(file_id_bytes).transact(
        {"from": account, "gas": 3000000}
    )
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt.transactionHash.hex()


def file_exists_on_chain(file_id_hex: str) -> bool:
    _, contract = _load_contract()
    file_id_bytes = bytes.fromhex(file_id_hex)
    return contract.functions.fileExists(file_id_bytes).call()


def get_file_record(file_id_hex: str):
    _, contract = _load_contract()
    file_id_bytes = bytes.fromhex(file_id_hex)
    return contract.functions.getRecord(file_id_bytes).call()