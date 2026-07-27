#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 4 ]]; then
  echo "usage: run_full_transcript_shards.sh POLE_STREAM CADICAL_BINARY CSP_BINARY OUTPUT_DIRECTORY" >&2
  exit 2
fi

pole_stream=$1
cadical_binary=$2
csp_binary=$3
output_directory=$4
script_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
audit_script="$script_directory/../four-pole-order18-exceptional-20260727/audit_transcript_stream.py"

for executable in "$cadical_binary" "$csp_binary"; do
  if [[ ! -x "$executable" ]]; then
    echo "classifier binary is not executable: $executable" >&2
    exit 2
  fi
done
if [[ ! -f "$pole_stream" || ! -f "$audit_script" ]]; then
  echo "pole stream or transcript auditor is missing" >&2
  exit 2
fi

mkdir -p "$output_directory"
python3 "$script_directory/prepare_full_pole_shards.py" \
  "$pole_stream" "$output_directory"

run_one() {
  local implementation=$1
  local binary=$2
  local shard=$3
  local input="$output_directory/input-shard${shard}.g6"
  local prefix="$output_directory/${implementation}-shard${shard}"

  set -o pipefail
  "$binary" --transcript --fail-on-hit --progress 100000 \
    <"$input" 2>"${prefix}.classifier.log" |
    python3 "$audit_script" \
      --implementation "$implementation" \
      --shard "$shard" >"${prefix}.transcript.audit.json"
  printf 'PASS implementation=%s shard=%s\n' \
    "$implementation" "$shard" >"${prefix}.status"
}

pids=()
for shard in 0 1 2 3 4 5 6 7; do
  run_one cadical "$cadical_binary" "$shard" &
  pids+=("$!")
  run_one csp "$csp_binary" "$shard" &
  pids+=("$!")
done

failed=0
for pid in "${pids[@]}"; do
  if ! wait "$pid"; then
    failed=1
  fi
done
if [[ "$failed" -ne 0 ]]; then
  echo "one or more order-22 full transcript shards failed" >&2
  exit 1
fi
echo "all sixteen order-22 full transcript shards completed"
