# Blockchain-Based Privacy-Preserving Image Deduplication

This is my M.Tech major project based on blockchain, cloud storage security and image deduplication.

The main idea of this project is to avoid storing the same or visually similar images multiple times in cloud storage. I used Perceptual Hashing (pHash) to identify exact and near-duplicate images. For new images, the image is encrypted before storing it in the CSP database. For duplicate images, ownership verification is performed.

I also integrated blockchain using Solidity, Web3.py and Ganache to record file information and provide an additional integrity verification layer.

## About the Project

Cloud storage can contain multiple copies of the same image or slightly modified versions of an image. Storing all these copies increases storage usage.
In this project, I tried to solve this problem using image-specific deduplication.
Instead of checking only whether two files are exactly the same, the system generates a pHash for each image and compares the hashes using Hamming distance.
Based on the comparison, the image is classified as:
- NEW_IMAGE
- NEAR_DUPLICATE
- EXACT_DUPLICATE

If it is a new image, it is encrypted and stored.
If it is a duplicate, the system performs ownership verification instead of storing another unnecessary copy.

## Main Features
- Image preprocessing and pHash generation
- Exact duplicate detection
- Near-duplicate detection using Hamming distance
- SHA-256 based file ID generation
- Image encryption
- Ownership verification
- CSP-side storage using SQLite
- Blockchain-based file recording
- Solidity smart contract
- Web3.py integration
- Image retrieval
- Integrity verification
- Local blockchain testing using Ganache

## Technologies Used
- Python
- Solidity
- Web3.py
- Ganache
- SQLite
- Pillow
- ImageHash
- Cryptography
- SHA-256
- Visual Studio Code
- 
**Important Modules**
client/preprocess.py
This module preprocesses the image and generates its perceptual hash.
The image is resized and converted before generating the pHash.
client/crypto.py
This module handles image encryption before the image is stored.
client/upload.py
This handles the image upload and preprocessing process.
csp/dedup.py
This is one of the main modules of my project.
It compares the generated pHash with existing hashes and checks the Hamming distance to identify:
New image
Near duplicate
Exact duplicate
csp/ownership.py
This module handles ownership verification when a duplicate image is detected.
csp/database.py
I used SQLite for the CSP-side metadata and encrypted image storage.
blockchain/blockchain.py
This module maintains the local blockchain-related functionality used in the project.
blockchain/eth_chain.py
This module connects the project with the Ethereum-compatible blockchain using Web3.py.
contracts/ImageAudit.sol
This is the Solidity smart contract used for recording and checking file information on the blockchain.
retrieve_image.py
This module is used to retrieve stored images and verify their integrity.

**Blockchain Part**
For the blockchain part, I used:
Solidity for the smart contract
Web3.py for Python and blockchain communication
Ganache as the local Ethereum development blockchain
The smart contract contains functions for recording files, checking whether a file exists and retrieving recorded information.
The contract used in the project is: contracts/ImageAudit.sol
The deployed contract information is stored in: contract_data.json

**Database**
SQLite is used as the CSP database in my implementation.
The database contains tables related to:

**Images**
File keys
File ownership

The image-related information includes the file ID, pHash and encrypted data.
The actual local database file is not uploaded to GitHub because it contains my local test data.

**Testing**
I tested the project with different image inputs.

1. New Image
When an image that is not already present is uploaded, the system produces: Deduplication Status: NEW_IMAGE
The image is then encrypted and stored.

2. Near Duplicate
I also tested visually similar images.
For example, one of my test executions produced: Best Hamming Distance: 4
                                                 Deduplication Status: NEAR_DUPLICATE
The system identifies the existing related image and performs the ownership-related processing.

3. Exact Duplicate
When the same image is uploaded again, the system detects: Deduplication Status: EXACT_DUPLICATE

The system then starts the ownership verification process instead of storing another copy.

4. Blockchain Recording
For a new image, the file information is also recorded through the blockchain/smart contract integration.

5. Image Retrieval
I tested image retrieval separately.
The retrieved image was checked against the stored integrity information.
Example output: Integrity Verified: Retrieved file matches stored hash
                Image download successful

**Execution Screenshots**
The screenshots folder contains screenshots from my actual project execution and testing.
They include:
Project architecture
New image detection
Near duplicate detection
Exact duplicate detection
Database records
Ownership records
Blockchain execution
Image retrieval and integrity verification

**How to Run**
Requirements
Install Python and the required packages.
pip install -r requirements.txt
Ganache is also required for the local blockchain part.
Start Ganache
Start Ganache and make sure the local blockchain is available at: http://127.0.0.1:7545
Deploy the Smart Contract
Run: python deploy_contract.py
This compiles and deploys the ImageAudit.sol smart contract and stores the contract information in contract_data.json.

Run the Main Program
Run: python main.py
This performs the main image upload, preprocessing, duplicate checking, encryption, storage and blockchain-related operations.

Test Image Retrieval
Run: python retrieve_image.py
This allows stored images to be retrieved and their integrity to be checked.

**Limitations**
This is an academic prototype and the current blockchain setup uses Ganache as a local development blockchain.
The CSP storage is also implemented locally using SQLite for demonstration and testing.
For a production system, the storage, blockchain network and key-management mechanisms would need to be deployed and secured appropriately.

**Future Improvements**
Some improvements that can be added in the future are:
Testing with a larger image dataset
Improving duplicate search performance for large-scale storage
Multi-cloud encrypted storage
Deployment on a public blockchain/testnet
More advanced ownership verification
Better access control using smart contracts
Scalable cloud storage integration

**My Project**
This project was developed as part of my M.Tech in Cyber Forensics & Information Security.
My main areas of work in this project are:
Blockchain + Cryptography + Image Deduplication + Cloud Storage Security

Author
Tanneeru Akhiladatta
M.Tech - Cyber Forensics & Information Security
B.Tech - Information Technology
GitHub:
https://github.com/akhilatanneeru
