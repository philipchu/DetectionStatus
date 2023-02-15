import hashlib
from datetime import datetime
from pymongo import MongoClient
import base64
import os
import logging


logger = logging.getLogger()

"""
Main Functions
----------------
This set of functions interfaces between an app and a MongoDB backend

"""
## gets a database using Linux environment
def getDatabase():
    client = MongoClient(os.environ.get("MONGO_URL"))
    db = client.flask_db
    txns = db.txns
    return txns


##  create a transaction key from a set of encoded bytes (string-like object) ##
##  inputs: string, length to hash
##  outputs: datestamped hash
def getTxnKey(image_encoded, byte_length=128):
    byte_length = min(byte_length, len(image_encoded))
    imageHash = image_encoded[0 : byte_length - 1]
    timeStamp = datetime.now().strftime("%m%d%Y%H%M%S")
    txnKey = str(
        base64.b64encode(hashlib.md5(base64.b64decode(imageHash + "==")).digest())
    )
    txnKey = timeStamp + txnKey
    return txnKey


##  store a result in a MongoDB database ##
##  inputs: key, data to store
##  outputs: ObjectID
def storeResult(txnKey, stringToStore, txnType=""):
    logger.info(f"inserting into {os.environ.get('MONGO_URL')}")
    txns = getDatabase()
    return txns.insert_one(
        {"txnKey": txnKey, "txnType": txnType, "data": stringToStore}
    )


def updateResult(txnKey, stringToStore, txnType=""):
    logger.info(f"updating {os.environ.get('MONGO_URL')}")
    txns = getDatabase()
    return txns.update_one(
        {"txnKey": txnKey, "txnType": txnType}, {"$set": {"data": stringToStore}}
    )


##  get an object from a database ##
##  inputs: key, txnType
##  outputs: "data" field associated with key/txnType
def getResult(txnKey, txnType=""):
    logger.info(f"getting from {os.environ.get('MONGO_URL')}")
    txns = getDatabase()

    if txnType == "":
        matches = txns.find({"txnKey": txnKey})
    else:
        matches = txns.find({"txnKey": txnKey, "txnType": txnType})
    matches = list(matches)
    print(matches)

    if len(matches) == 1:
        return matches[0]["data"]
    else:
        logger.error(f"{len(matches)} matches for txnKey: {txnKey}")
        return len(matches)
