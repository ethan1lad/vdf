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
We present a VDF that takes at least 10 minutes to compute which uses an Ergo Block hash as the input to the VDF and produces a 128-bit output. We argue that a 10-minute VDF offers reasonable certainty that randomness beacon is unmalleable, as it would take 5x the block time for a miner to know what output their proof of work solution would produce under the VDF, by which time it is likely their proof of work solution is stale (this becomes more likely as the network hash rate increases), however, it is possible to adjust the parameters of our VDF such that the delay time is longer for increased security.

There are numerous functions that make fine candidate VDFs, however we have selected the composition of modular square roots as our function, drawing inspiration from an [Ethereum implementation](https://jbonneau.com/doc/BGB17-IEEESB-proof_of_delay_ethereum.pdf)
## Our Construction:
The major parts of our VDF construction are:
1.	Select a 128-bit gaussian prime _p_ `p ≡ 3 mod 4`
2.	Select a 128-bit seed _x_
3.	Compute `f(x) ≡ √x mod p`
4.	Compose f(x) n times, `f^n(x) = (f ∘ f ∘ f...)(x)   (n iterations)` which gives an output _r_ (128 Bits)
5.	Verify output by computing `r ^ 2^n mod p = x mod p`
We detail each of these parts below.
### 1. Select a 128-bit gaussian prime _p_
To begin we describe our concerns with how we are selecting _p_:

- All selected values of our VDF implementation are 128 bits in length. Ideally, we would chose a larger _p_ since modular square roots are O(log _p_), however, we could not find a natural way to implement the verification `r ^ 2^n mod p = x mod p` under the 256-bit size limitation of BigInts in ergoscript for _p_, _x_ and _r_ of size larger than 128 bits.

- If we could select a larger _p_, there would be gains to the efficiency of our VDF, so if the Judges could see some way of increasing _p_ whilst still having it possible to verify the VDF in Ergoscript that would be great :)

- Another, possibly more important, outcome of a larger _p_ is that for larger _p_ (and consequently larger seed value and result value) it becomes more and more unfeasible for an adversary to have a map from all input seeds under some _p_ to their result. Whilst we believe 128-bit sizes should be ok, we are concerned that this is not secure enough, particularily if we do not find some way to randomly rotate the _p_ in use by the protocol.

Our selection for _p_:

Our presentation is missing a few small parts of a fully secure VDF. One such part is a proper selection of _p_.

The files provided here have the VDF prover select their own _p_ (provide link), there are no checks in the verification process that ensure _p_ is a prime, is congruent to 3 mod 4 or is of 128-bits in length. We did not implement these checks because we are not certain on whether it is necessary to change _p_ (to avoid the mapping of inputs seeds to results) or if 128-bit sized _p_ is large enough to not have it change for each VDF calculation. We require someone with the relevant background to let us know if this changing of _p_ is neccessary. If it is neccessary, our selection process we envision would involve the creation of epochs under the VDF protocol, where each epoch would change _p_ based on the latest Ergo block header to prevent pre-calculation of future _p_.

### 2.	Select a 128-bit seed _x_
The selection of the seed _x_ is not described by our VDF as this will be up to the smart contract looking to use the VDF. Any selection is fine, so long as the source can take advantage of our VDF's delay property. So selections like a 128-bit part of an Ergo block header or a selection of the 128-bit part of an oracle box id would suffice.





