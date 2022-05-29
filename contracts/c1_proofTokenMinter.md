# Proof Token Minter Contract
This is the contract which dApps will fund with some Erg Value and a seed for the VDF prover to calculate the output for.

Proof size refers to the the number of iterations the modular square root function should be composed (the number of iterations = proofSize * 35,600 in our implementation), in future this value should be made dynamic (set by the contract funder) however for simiplicity we present it with the static value 360.

To spend the box, a VDF prover must input their own ERG, the amount they provide will be:

```proofSize * slashValue + 2 * miningFee - dAppReward``` 

If the VDF prover provides a correct result for the VDF calculation they will keep the entire value of their inputted ERG and the dAppReward.

The contract has a register R4 which the dapp can use to record a refund address if they no longer wish for the VDF calculation to be made. The refund condition can be met immediately, but it would be nice to implement a deadline so that a VDF prover knows when it is possible for the VDF reward to be refunded.


```scala
{
val proofToken = SELF.id // proofToken will be minted
val proofSize = 360 
val slashValue = 100000000L
val miningFee = 1000000
val mintProofs = allOf(Coll(
OUTPUTS(0).tokens.size == 1,
OUTPUTS(0).tokens(0)._1 == proofToken,
OUTPUTS(0).tokens(0)._2 == proofSize,
blake2b256(OUTPUTS(0).propositionBytes) == fromBase58("GNz4iSGQFqKap4W1d5cpZ3gQYhF2PNmAXURwYAC2THin"), // Send to distrubution address
OUTPUTS(0).value == proofSize * slashValue + miningFee, 
OUTPUTS(0).R8[BigInt].get == SELF.R5[BigInt].get)) // Set R8 to the seed value (R7 should be populated by VDF prover ERG address)
val refund = allOf(Coll(
OUTPUTS.size == 2,
OUTPUTS(0).tokens.size == 0,
OUTPUTS(0).propositionBytes == SELF.R4[Coll[Byte]].get,
OUTPUTS(0).value == SELF.value - miningFee))
sigmaProp(mintProofs || refund)
}
```
