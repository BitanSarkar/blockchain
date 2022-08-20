# Blockchain
This is a part of tutorial I have been studying, I can pull the materials from anywhere I want.

Course Material:
https://www.superdatascience.com/blockchain/

## Blockchain Intuition
1. Concept started with a research paper on how to time stamp a digital document 
    > - Read Blockchain Intuition/Haber-Stornetta1991_Chapter_HowToTime-StampADigitalDocumen.pdf


2. Understanding SHA256 hash
    > - https://tools.superdatascience.com/blockchain/hash/
    >
    > - Read Blockchain Intuition/CrypCont.pdf

3. Immutable Ledger
    > - Read https://medium.com/cryptoeconomics-australia/the-blockchain-economy-a-beginners-guide-to-institutional-cryptoeconomics-64bf2f2beec4

4. Distributed P2P Network
    > - https://medium.com/@VitalikButerin/the-meaning-of-decentralization-a0c92b76a274

5. Byzantine Fault Tolerance
    > - Read 1. Blockchain Intuition/The-Weak-Byzantine-Generals-Problem.pdf
    >
    > - https://medium.com/loom-network/understanding-blockchain-fundamentals-part-1-byzantine-fault-tolerance-245f46fe8419

6. Consensus Protocol
    > - https://www.mail-archive.com/cryptography@metzdowd.com/msg09997.html
    >
    > - https://www.coindesk.com/markets/2017/03/04/a-short-guide-to-blockchain-consensus-protocols/

## Crytocurrency Intuition
1. What is Bitcoin?
    > - It is a protocol that facilitates blockchain.
    >
    > - Read : https://www.bitcoin.org/
    >
    > - Read : 2a. Crytocurrency Intuition/bitcoin.pdf

2. Bitcoin's Monetary Policy
    > - Read https://hackernoon.com/this-time-is-different-part-2-what-bitcoin-really-is-ae58c69b3bf0

3. Understanding Mining Difficulty
    > - Right now leading 18 zeros, current target
    >
    > - Max target which was initially, 8 zeros
    >
    > - Difficulty is adjusted every 2 weeks

4. Mining Pools
    > - Bitcoin mining pool setup, https://blog.bitcoin.org.hk/bitcoin-mining-and-energy-consumption-4526d4b56186

5. Nonce Range
    > - It is a 32 bit number, thus 1 nonce range is not enough
    >
    > - Unix timestamp increases the range to infinite

6. How miners pick Transactions
    > - Having the highest transaction fee
    >
    > - transactions are stored in mempool temporarily before going into a block

7. CPUs vs GPUs vs ASICs
    > - CPU 10 MH/s uses logic
    >
    > - GPU 1000 MH/s uses logic
    >
    > - ASIC 1000000 MH/s more specialized in a circuital hardware level to calculate SHA256
    >
    > - Cloud mining, using a cloud servers
    >
    > - Bitcoin uses SHA256, which is easy to create a circuital hardware to calculate SHA256. but Etherium uses EHash, which is a memory based hashing, which prevents us from creating a circuital hardware because anyway we would need memory support and would increase computational time. In conclusion, Ehash stops people from creating ASICs for Etherium.
    >
    > - Read https://www.vijaypradeep.com/blog/2017-04-28-ethereums-memory-hardness-explained/

8. How do Mempools work?
    > -  Read https://blog.kaiko.com/an-in-depth-guide-into-how-the-mempool-works-c758b781c608

9. The 51% Attack
    > - Read https://blog.sia.tech/choosing-asics-for-sia-b318505b5b51

### Transaction logic

10. Transactions and UTXOs
    > - UTxO is Unspent Transaction Output
    >
    <br/>Mark -> Me 0.1 BTC // These all are called UTxOs
    <br/>Dave -> Me 0.6 BTC
    <br/>Ruuk -> Me 0.7 BTC
    <br/>Mate -> Me 0.2 BTC
    
    Suppose I want to now spent 0.5 BTC on a bike.

    I would need to create 2 Txs, using the BTC I got from Dave. I can't directly split transaction in wallet so I need to create a change for myself and create the remaining BTC as a self transaction.
    <br> Me -> Bike shop 0.5 BTC
    <br> Me -> Me 0.1 BTC

    Now these 2 became transactions which would be later added to the blocks.

    Now, the UTxOs left

    <br/>Mark -> Me 0.1 BTC
    <br/>Ruuk -> Me 0.7 BTC
    <br/>Mate -> Me 0.2 BTC
    <br/>Me -> Me 0.1 BTC

11. Where do transaction fees come from?
    > Left over money in transaction
    > Theoretically you can give 0 fees but then miners won't even consider your transaction and after 72 hours staying in the mempool it would be just returned back to you are transaction failed.

12. How wallet work?
    > Adds up all the UTxOs which is given to Me and becomes the total amount present in wallet.

13. Signatures: Private and Public Key
    > Basically there is a Private Key, which is private and must not be shared. And from Private Key, a hash algo creates a Public key which can be shared, and while any transaction, you can provide a signature which uses a message and private key as a key. Now there is verification function which can take the signature and public key and verify the tranction signature is valid or not. Basically it will check whther it is you or not.
    >
    > - Demo https://tools.superdatascience.com/blockchain/public-private-keys/signatures

14. What is Segregated Witness? (SegWit)
    > - There is limit of **1MB** for a block, too large the mempool sharing would take time to find the best transactions, thus reducing bandwidth and too small, it will hold few very few transactions which would increase the waiting time.
    >
    > - To solve the problem, we would be using segregated witness. Remove the Signature and Public Key from blocks and pass it through a messaging server which would be linked to the transactionID.
    >
    > - Read https://jimmysong.medium.com/understanding-segwit-block-size-fd901b87c9d4

15. Public Keys Vs Bitcoin Address
    > - ![public keys vs bitcoin address](https://github.com/BitanSarkar/blockchain/blob/main/2a.%20Crytocurrency%20Intuition/public_key_vs_bitcoin_address.jpeg?raw=true)
    >
    > - Read https://www.reddit.com/r/Bitcoin/comments/3filud/whats_the_difference_between_public_key_and/

16. Hierarchically Deterministic (HD) Wallets
    > - ![Hierarchically Deterministic Wallet](https://github.com/BitanSarkar/blockchain/blob/main/2a.%20Crytocurrency%20Intuition/HD_wallet.jpg?raw=true)
    >
    > - Read [DETERMINISTIC WALLETS, THEIR ADVANTAGES AND THEIR UNDERSTATED FLAWS](https://bitcoinmagazine.com/technical/deterministic-wallets-advantages-flaw-1385450276)

## Part 3 - Smart Contract
1. What is Etherium
    > - It is programmable, basic idea is to store codes in each blocks which would be further decentralized. (Kinda like open source code with security) Decentralized super-computer.