#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
BASE=$(CDPATH= cd -- "$HERE/../.." && pwd)
CXX=${CXX:-clang++}
GENG=${GENG:-/opt/homebrew/bin/geng}
WORK=$(mktemp -d -t d5-rooted-interface.XXXXXX)
trap 'rm -rf -- "$WORK"' EXIT HUP INT TERM
BIN="$WORK/predicate_stream"
PRIMARY="$WORK/primary.txt"
VERIFY="$WORK/verify.txt"

"$CXX" -std=c++20 -O3 -DNDEBUG -Wno-return-type \
  "$HERE/predicate_stream.cpp" -o "$BIN"

"$GENG" -Cq -d3 -D3 16 2>/dev/null \
  | "$BIN" --witnesses "$WORK/order16.tsv" >> "$PRIMARY"

for n in 18 20 22 24 26; do
  "$BIN" --witnesses "$WORK/order$n.tsv" \
    < "$BASE/search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order$n.g6" \
    >> "$PRIMARY"
done

"$BIN" --witnesses "$WORK/strong34.tsv" \
  < "$BASE/search/strong_snarks/source/strongsnarks_34_5_cyc4.g6" \
  >> "$PRIMARY"
cmp "$HERE/expected-primary-output.txt" "$PRIMARY"

python3 "$HERE/verify_witnesses.py" "$WORK/order16.tsv" \
  --corpus-name order16-all-biconnected-cubic \
  --expected-sha256 57104aba69a542707e11ebdd8d6105afc2ce56d78b45f2e1ff0db55c1fab9de2 \
  --expected-graphs 3874 >> "$VERIFY"

python3 "$HERE/verify_witnesses.py" "$WORK/order18.tsv" \
  --corpus-name order18-cyclic4-nontait \
  --expected-sha256 2660e7d5c8a351b4ed3d69f8df316e748e264a630c01328ea4bed43f96f78dfd \
  --expected-graphs 2 --require-nontait --require-cyclic4 >> "$VERIFY"
python3 "$HERE/verify_witnesses.py" "$WORK/order20.tsv" \
  --corpus-name order20-cyclic4-nontait \
  --expected-sha256 a65153d9dc38bebffca52b2c2ec05f194807b10ca097f50a551d5aab871244f1 \
  --expected-graphs 6 --require-nontait --require-cyclic4 >> "$VERIFY"
python3 "$HERE/verify_witnesses.py" "$WORK/order22.tsv" \
  --corpus-name order22-cyclic4-nontait \
  --expected-sha256 2c3d91e55cb264450cf321e2299355f6cf0f5c2c60a83c99372a1d73ed5a4223 \
  --expected-graphs 31 --require-nontait --require-cyclic4 >> "$VERIFY"
python3 "$HERE/verify_witnesses.py" "$WORK/order24.tsv" \
  --corpus-name order24-cyclic4-nontait \
  --expected-sha256 37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456 \
  --expected-graphs 155 --require-nontait --require-cyclic4 >> "$VERIFY"
python3 "$HERE/verify_witnesses.py" "$WORK/order26.tsv" \
  --corpus-name order26-cyclic4-nontait \
  --expected-sha256 1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760 \
  --expected-graphs 1297 --require-nontait --require-cyclic4 >> "$VERIFY"
python3 "$HERE/verify_witnesses.py" "$WORK/strong34.tsv" \
  --corpus-name order34-retained-strong \
  --expected-sha256 2f087d5cbd1e97b1e10e7a5a064fe83d037872f838372e4d317c9d3f912fbf1f \
  --expected-graphs 7 --require-nontait --require-cyclic4 --require-girth 5 \
  >> "$VERIFY"
cmp "$HERE/expected-verifier-output.txt" "$VERIFY"

(
  cd "$HERE"
  shasum -a 256 -c SHA256SUMS
  shasum -a 256 -c SOURCES.sha256
)
echo "D5_ROOTED_INTERFACE_FRONTIER_THROUGH34 PASS"
