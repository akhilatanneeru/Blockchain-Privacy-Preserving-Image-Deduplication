// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract ImageAudit {

    struct Record {
        address owner;
        uint256 timestamp;
        bool exists;
    }

    mapping(bytes32 => Record) private records;

    event FileRecorded(
        bytes32 indexed fileId,
        address indexed owner,
        uint256 timestamp
    );

    event OwnershipUpdated(
        bytes32 indexed fileId,
        address indexed newOwner,
        uint256 timestamp
    );

    function recordFile(bytes32 fileId) public {

        require(
            !records[fileId].exists,
            "File already exists"
        );

        records[fileId] = Record({
            owner: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });

        emit FileRecorded(
            fileId,
            msg.sender,
            block.timestamp
        );
    }

    function updateOwner(bytes32 fileId) public {

        require(
            records[fileId].exists,
            "File does not exist"
        );

        records[fileId].owner = msg.sender;

        emit OwnershipUpdated(
            fileId,
            msg.sender,
            block.timestamp
        );
    }

    function fileExists(bytes32 fileId)
    public
    view
    returns (bool)
    {
        return records[fileId].exists;
    }

    function getRecord(bytes32 fileId)
    public
    view
    returns (
        address owner,
        uint256 timestamp,
        bool exists
    )
    {
        Record memory record = records[fileId];

        return (
            record.owner,
            record.timestamp,
            record.exists
        );
    }
}