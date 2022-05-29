# A Verifiable Delay Function (VDF) on Ergo
* Author: Krasavice Blasen, Night Owl Team
* Created: 25-May-2022
* License: CC0

## To the Judges
Hello judges of Ergohack! This readme provides the relevant information for our VDF implementation. No one from night owl has a background in cryptography or strong mathematical background, so it would be highly appreciated if you could carefully go through our claims in the "Our Construction" section, your feedback would be highly appreciated. 

## What is a Verifiable Delay Function?
A Verifiable Delay function (VDF) is a function whose evaluation requires running a given number of sequential steps, yet the result can be efficiently verified. 

Unlike proof of work algorithms, a VDF offers a guarantee for the minimum computation time of some function, where this computation time cannot be meaningfully sped up with parallel processing. 

Like proof of work algorithms, a VDF can be efficiently verified. 
##  Use case on Ergo:
VDFs can be used to construct unmalleable randomness beacons on Ergo. Of course, a randomness beacon that nobody can influence is useful for Night Owl’s vision of a truly fair casino, but the applications of such a beacon spread far. Any dApp that requires incorruptible random numbers would likely require some VDF. We envision use cases such as: deciding tiebreaks, randomness in high-value games, randomness mechanisms in DAOs, vending machine style NFT drops…
## Our Randomness Beacon:
We present a VDF that takes at least 12 minutes to compute which uses an Ergo Block hash as the input to the VDF and produces a 128-bit output. We argue that a 12-minute VDF offers reasonable certainty that randomness beacon is unmalleable, as it would take 6x the block time for a miner to know what output their proof of work solution would produce under the VDF, by which time it is likely their proof of work solution is stale (this becomes more likely as the network hash rate increases), however, it is possible to adjust the parameters of our VDF such that the delay time is longer for increased security.

There are numerous functions that make fine candidate VDFs, however we have selected the composition of modular square roots as our function, drawing inspiration from an [Ethereum implementation](https://jbonneau.com/doc/BGB17-IEEESB-proof_of_delay_ethereum.pdf)
## Our Construction:
The major parts of our VDF construction are:
1.	Select a 128-bit gaussian prime _p_ `p ≡ 3 mod 4`
2.	Select a 128-bit seed _x_
3.	Compute `f(x) ≡ √x mod p` and	compose f(x) n times, `f^n(x) = (f ∘ f ∘ f...)(x)   (n iterations)` which gives an output _r_ (128 Bits)
4.	Verify output by computing `r ^ 2^n mod p = x mod p`

We detail each of these parts below.
### 1. Select a 128-bit gaussian prime _p_
Before we describe our selection of _p_, we would like to acknowledge some potential concerns with the bit-size of our selected prime:

- All selected values of our VDF implementation are 128 bits in length. Ideally, we would chose a larger _p_ since modular square roots are O(log _p_), however, we could not find a natural way to implement the verification `r ^ 2^n mod p = x mod p` under the 256-bit size limitation of BigInts in ergoscript for _p_, _x_ and _r_ of size larger than 128 bits.

- If we could select a larger _p_ there would be gains to the efficiency of our VDF, so if the Judges could see some way of increasing _p_ whilst still having it possible to verify the VDF in Ergoscript that would be great :)

- Another, possibly more important outcome of a larger _p_, is that for larger _p_ (and consequently larger seed value and result value) it becomes more and more unfeasible for an adversary to have a map from all input seeds under some _p_ to their result. Whilst we believe 128-bit sizes should be ok, we are concerned that this is not secure enough, particularily if _p_ is a static value in use by the protocol.

The above acknowledgements are important and any feedback would be appreciated, however, if we assume that a 128-bit sized _p_ and 128-bit sized seed can offer enough entropy for an input to output map being unfeasible then our VDF construction is valid. We offer two possible selections of _p_:

1. Use a static value that is known to be a 128-bit gaussian prime for all calculations under the VDF.
2. Define an epoch length for the VDF protocol and change the value of _p_ when the epoch ends. To prevent knowledge of future _p_, the value _p_ should be generated from some value of the previous epoch (like a box id from the protocol).

The implementation provided in this repository does not include the selection of _p_, instead we have allowed the prover to select their own _p_ (and seed) which is not secure, however once we have some feedback on the proper selection of our prime we can easily implement this for our VDF (for example publish _p_ on-chain, the prover reads and includes this in their proof, their proof's usage of _p_ can be easily evaluated using a dataInput in ErgoScript)


### 2.	Select a 128-bit seed _x_
The selection of the seed _x_ is no concern of the VDF protocol. Any dApp can provide a seed they want the VDF to publish (by funding a VDF mint box with their seed) and the VDF will calculate the result given that seed (or negation of that seed) as the input. 

We recommend that dApps use Ergo block headers as the source of their seed or trusted oracle box id's (like the ERG/USD oracle). Any source is fine as long as the source is able to go 'stale' after a period of time (to take advantage of the delay property of our VDF) and that period of time is longer than the VDF's expected minimum computation time. 


### 3.	Compute VDF
Our implementation shows the computation of a VDF with approximately 12.8 million compositions of `f(x) ≡ √x mod p`.

Empirically this took us 12 minutes to run, however with better hardware this time may be quicker. Further research of running times with more efficient VDF implementations and better hardware will be necessary to provide a guarantee of minimum running time. We doubt that anything larger than a 100x improvement is possible but this is just speculation for now. Any improvement to running time can be compensated by just increasing _n_ which requires more data to be stored on the blockchain (see verification) but this cost is minimal.

### 4.	Verify output
Perhaps this is the most exciting part of our presentation (going through the ergoscript!). 

For our VDF to be meaningfully useful, we need to be able to verify the output in Ergoscript. We have provided this verification for our VDF using 3 ergoscript [contracts](https://github.com/nightowlcasino/vdf/blob/master/contracts):
- [c1_proofTokenMinter](https://github.com/nightowlcasino/vdf/blob/master/contracts/c1_proofTokenMinter.md) (dApp Funds a VDF seed)
- [c2_proofDistribution](https://github.com/nightowlcasino/vdf/blob/master/contracts/c2_proofDistribution.md) (Prover accepts and publishes result)
- [c3_checkpointsContract](https://github.com/nightowlcasino/vdf/blob/master/contracts/c3_checkpointsContract.md) (Proof can be challenged by the public)


#### [c1_proofTokenMinter](https://github.com/nightowlcasino/vdf/blob/master/contracts/c1_proofTokenMinter.md)
A dapp funds c1_proofTokenMinter with any amount of Erg and the seed they wish to have a VDF compute. An entity running the VDF prover can scan the c1_proofTokenMinter address looking for a box with a desired level of funding. Once the prover settles on a box they can then work on calculating the output to the VDF function. 

When the prover finds the output _r_, they are ready to publish their result (spend c1_proofTokenMinter), they do this by:
- Providing some ERG that can be slashed for if they produce a bad result (we have set this to 0.1 ERG per checkpoint box which gives 36 ERG in total)
- Minting 360 _proof tokens_ which will be distrubuted to the checkpoint boxes. 
- Providing their result for the seed and prime they used (should match the seed that the dapp requested, the prime has been excluded from our contract since we have not defined how the prime shall be selected yet)
- The output to this transaction (output 0) will contain 360 proof tokens and be stored in a box guarded by the distrubution contract (c2_proofDistribution)

This contract is necessary so that any dApp using the outcome of the VDF can easily validate that the proof tokens used by the protocol were minted correctly (minted from c1_proofTokenMinter) which can be referenced in ErgoScript by providing the encoding of the original issuance box (it will have the boxId = proofTokenId)

#### [c2_proofDistribution](https://github.com/nightowlcasino/vdf/blob/master/contracts/c2_proofDistribution.md)
By this stage a VDF prover has committed to publishing the result of some VDF. 360 Proof tokens and the prover's ERG reserved for slashing have been sent to c2_proofDistribution from c1_proofTokenMinter, as well as the seed to be used.

c2_proofDistribution is a simple contract that distrubutes one proof token to each checkpoint box (c3_checkpointsContract) and equally splits the slashValue to each box. 

c2_proofDistribution also ensures that all of the relevant registers are defined so they can be verified by c3_checkpointsContract without any compilation errors.

There are no refunds for c2_proofDistribution, so once the prover has committed to producing a result they must provide a result or their ERG will be stuck.
Ideally, we could write a spending path that allows the entire ERG or at least the dApp Reward to be retrievable after some deadline so that dApps do not need to keep wasting ERG on bad VDF provers. 

#### [c3_checkpointsContract](https://github.com/nightowlcasino/vdf/blob/master/contracts/c3_checkpointsContract.md)
c3_checkpointsContract is the contract where the verification of the prover's VDF occurs. The prover has published a final result in R9 of every box under c3_checkpointsContract with 1 proof token in each box along with a series of checkpoint values which show the prover's progression from the seed to the result. The proof is assumed true if after 200 blocks (this value may be changed and made variable in future) the prover is able to combine all 360 proof tokens together in one result box. However, anyone in the public is able to dispute the prover's claim by attempting to burn any of the proof tokens. If the prover's output is inccorect, or if any checkpoint are incorrect, then it will be possible for the public to burn a proof token (and claim the slash reward as an incentive to verify VDF claims) and thus invalidate the VDF proof.


















