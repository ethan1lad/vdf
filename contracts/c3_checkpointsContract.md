# Checkpoints Contract
A contract that is challengable by anyone for a period of time. VDF is assumed true if no one successfully challenges.

Possible ways to successfully challenge checkpoint contract:
- Going from a checkpoint to the next checkpoint yields a different value to that stored in SELF.R4
- The box with the next index has a different start to the current boxes end checkpoint
- The first indexed box does not start at the seed
- The last indexed box does not end at the final answer

If challenged successfuly the proof token will be burnt and thus any dApps using the VDF output will reject the output due to not enough proof tokens.


```scala
{
val proofAddress = fromBase58("")

// Prover Provides
val checkpoints = SELF.R4[Coll[BigInt]].get
val bigIntNums = SELF.R5[Coll[BigInt]].get
val p = bigIntNums(0)
val myCol = SELF.R6[Coll[Byte]].get
val index = SELF.R7[Int].get
val seed = bigIntNums(1)
val finalAns = bigIntNums(2)

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

// Bad start 
val badStart = allOf(Coll(
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
OUTPUTS(0).R6[BigInt].get == p,
OUTPUTS(0).R7[Box].get.id == SELF.tokens(0)._1
)) // Something about proof address outputs
if (HEIGHT > SELF.creationInfo._1 + 5) {
val pubKey = SELF.R8[GroupElement].get // Only allow prover to spend
sigmaProp(windowClosed && proveDlog(pubKey))
} else{
sigmaProp(badProofSpend && (badCheckpoints || badNextStart || badStart || badFinalAns))
}
}
```
