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
    > - 