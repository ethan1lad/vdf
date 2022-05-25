```scala
{
val slashValue = 1000000
val proofSize = 4
val checkpointAddress = fromBase58("")
val proofToken = SELF.tokens(0)._1
val checkpoints = OUTPUTS.slice(0,OUTPUTS.size - 1)
val checkpointConditions = checkpoints.forall{
(output: Box) => allOf(Coll(
output.tokens(0)._2 == 1,
output.tokens(0)._1 == proofToken,
output.value >= slashValue,
blake2b256(output.propositionBytes) == checkpointAddress))
} && OUTPUTS.size == proofSize + 1
val refundConditions = allOf(Coll(
OUTPUTS.size == 2,
OUTPUTS(0).tokens.size == 0,
OUTPUTS(0).propositionBytes == SELF.R7[Coll[Byte]].get))
sigmaProp(refundConditions || checkpointConditions)
}
```
