slashValue and proofSize to become variable
```scala
{
val proofToken = SELF.id
val proofSize = 4
val slashValue = 1000000
val miningFee = 1000000
val mintProofs = allOf(Coll(
OUTPUTS.size == 2,
OUTPUTS(0).tokens.size == 1,
OUTPUTS(0).tokens(0)._1 == proofToken,
OUTPUTS(0).tokens(0)._2 == proofSize,
blake2b256(OUTPUTS(0).propositionBytes) == fromBase58("GNz4iSGQFqKap4W1d5cpZ3gQYhF2PNmAXURwYAC2THin"),
OUTPUTS(0).value == proofSize * slashValue + miningFee,
OUTPUTS(0).R7[Coll[Byte]].get == SELF.R4[Coll[Byte]].get))
val refund = allOf(Coll(
OUTPUTS.size == 2,
OUTPUTS(0).tokens.size == 0,
OUTPUTS(0).propositionBytes == SELF.R4[Coll[Byte]].get,
OUTPUTS(0).value == SELF.value - miningFee))
sigmaProp(mintProofs || refund)
}
```
