#!/bin/sh
set -eu

CXX=${CXX:-clang++}
"$CXX" -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  verify_sharded.cpp -o verify_sharded

for shape in 4+4+7 4+5+6 5+5+5 4+11 5+10 6+9 7+8
do
  slug=$(printf '%s' "$shape" | tr '+' 'p')
  shard=0
  while [ "$shard" -lt 16 ]
  do
    ./verify_sharded "$shape" "$shard" 16 \
      > "${slug}-shard16-${shard}.txt" &
    shard=$((shard + 1))
  done
  wait
done

"$CXX" -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic \
  ../minimum-projection-single-circuit-anchor-factorization-20260729/anchor_single_census.cpp \
  -o anchor_single15
shard=0
while [ "$shard" -lt 16 ]
do
  ./anchor_single15 "$shard" 16 -1 anchor \
    > "15-shard16-${shard}.txt" &
  shard=$((shard + 1))
done
wait

python3 verify_summary.py | tee verification-output.txt
