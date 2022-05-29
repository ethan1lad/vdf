# Proof Distribution Contract
This contract distrubutes the proof tokens for the VDF.

It is only spendable by the VDF prover (the entity that provided the ERG to be slashed) and cannot be refunded (to penalise the spending of a funded VDF mint box where the VDF prover does not return a result)


```scala
{
val slashValue = 100000000L
val miningFee = 1000000
val proofSize = 360
val checkpointAddress = fromBase58("")
val proofToken = SELF.tokens(0)._1
val checkpoints = OUTPUTS.slice(0,OUTPUTS.size - 1)
val checkpointConditions = checkpoints.forall{
(output: Box) => allOf(Coll(
output.tokens(0)._2 == 1,
output.tokens(0)._1 == proofToken,
output.value >= slashValue,
blake2b256(output.propositionBytes) == checkpointAddress,
output.R4[Coll[BigInt]].isDefined, // enter checkpoints
output.R5[BigInt].isDefined, // prime p
output.R6[Coll[Byte]].isDefined, // fold sized collection of bytes
output.R7[Int].isDefined, // box index
output.R8[BigInt].get == SELF.R8[BigInt].get, // Seed 
output.R9[BigInt].isDefined)) // Prover result r
} && OUTPUTS.size == proofSize + 1
val pubKey = SELF.R7[GroupElement].get // Only allow prover to spend
sigmaProp(checkpointConditions && proveDlog(pubKey))
}
```
