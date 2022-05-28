Need to put proof complete conditions in
```scala
{
val proofAddress = fromBase58("")

// Prover Provides
val checkpoints = SELF.R4[Coll[BigInt]].get
val p = SELF.R5[BigInt].get
val myCol = SELF.R6[Coll[Byte]].get
val index = SELF.R7[Int].get
val seed = SELF.R8[BigInt].get
val finalAns = SELF.R9[BigInt].get

// Challenger provides (Bad Checkpoints)
val falseIndex = OUTPUTS(0).R4[Int].get
val ans = checkpoints(falseIndex + 1)
val start = checkpoints(falseIndex)

// Challenger provides (bad next box)
val nextBox = CONTEXT.dataInputs(0)

// Bad checkpoints
val badCheckpoints = myCol.fold(ans, {(z: BigInt, base:Byte) => (z * z) % p}) != start % p

// Bad next box
val badNextStart = allOf(Coll(
nextBox.propositionBytes == SELF.propositionBytes,
nextBox.R7[Int].get == index + 1,
nextBox.R4[Coll[BigInt]].get(0) != checkpoints(checkpoints.size - 1),
nextBox.tokens(0)._1 == SELF.tokens(0)._1))

// Bad Seed 
val badSeed = allOf(Coll(
nextBox.propositionBytes == SELF.propositionBytes,
nextBox.R7[Int].get == 0,
nextBox.R4[Coll[BigInt]].get(0) != seed,
nextBox.tokens(0)._1 == SELF.tokens(0)._1))

// Bad finalAns
val badFinalAns = allOf(Coll(
nextBox.propositionBytes == SELF.propositionBytes,
nextBox.R7[Int].get == 100,
nextBox.R4[Coll[BigInt]].get(checkpoints.size - 1) != finalAns,
nextBox.tokens(0)._1 == SELF.tokens(0)._1))

// Bad proof spend path
val badProofSpend = allOf(Coll(
OUTPUTS.size == 2,
OUTPUTS(0).tokens.size == 0))

// Window Closed, proof assumed true spend path
val windowClosed  = allOf(Coll(
OUTPUTS(0).tokens(0)._1 == SELF.tokens(0)._1,
OUTPUTS(0).tokens(0)._2 == 100,
blake2b256(OUTPUTS(0).propositionBytes)== proofAddress,
OUTPUTS(0).R4[BigInt].get == seed,
OUTPUTS(0).R5[BigInt].get == finalAns,
OUTPUTS(0).R6[BigInt].get == p
)) // Something about proof address outputs
if (HEIGHT > SELF.creationInfo._1 + 5) {
sigmaProp(windowClosed)
} else{
sigmaProp(badProofSpend && (badCheckpoints || badNextStart || badSeed || badFinalAns))
}
}
```
