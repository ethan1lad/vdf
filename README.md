# A Verifiable Delay Function (VDF) on Ergo
* Author: Krasavice Blasen, Night Owl Team
* Created: 25-May-2022
* License: CC0
## What is a Verifiable Delay Function?
A Verifiable Delay function (VDF) is a function whose evaluation requires running a given number of sequential steps, yet the result can be efficiently verified. 

Unlike proof of work algorithms, a VDF offers a guarantee for the minimum computation time of some function, where this computation time cannot be meaningfully sped up with parallel processing. 

Like proof of work algorithms, a VDF can be efficiently verified. 
##  Use case on Ergo:
VDFs can be used to construct unmalleable randomness beacons on Ergo. Of course, a randomness beacon that nobody can influence is useful for Night Owl’s vision of a truly fair casino, but the applications of such a beacon spread far. Any dApp that requires incorruptible random numbers would likely require some VDF. We envision use cases such as: deciding tiebreaks, randomness in high-value games, randomness mechanisms in DAOs, vending machine style NFT drops…
## Our Randomness Beacon:
We present a VDF that takes at least 10 minutes to compute which uses an Ergo Block hash as the input to the VDF and produces a 128-bit output. We argue that a 10-minute VDF offers reasonable certainty that randomness beacon is unmalleable, as it would take 5x the block time for a miner to know what output their proof of work solution would produce under the VDF, by which time it is likely their proof of work solution is stale (this becomes more likely as the network hash rate increases), however, it is possible to adjust the parameters of our VDF such that the delay time is longer for increased security.

There are numerous functions that make fine candidate VDFs, however we have selected the composition of modular square roots as our function, drawing inspiration from an [Ethereum implementation](https://jbonneau.com/doc/BGB17-IEEESB-proof_of_delay_ethereum.pdf)
## Our Construction:
1.	Select a gaussian prime p (p congruent 3 mod 4) (128 Bits)
2.	Select a seed x (first 128-bits of Ergo Block Hash)
3.	Compute f(x) congruent sqrt(x) mod p
4.	Compose f(x) n times, fn(x) = f o f o f o f = random output r (128 Bits)
5.	Verify output by computing r^ 2^n mod p == x mod p


