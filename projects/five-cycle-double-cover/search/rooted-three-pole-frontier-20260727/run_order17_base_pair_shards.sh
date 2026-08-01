#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 3 ]]; then
  echo "usage: run_order17_base_pair_shards.sh CADICAL_BINARY CSP_BINARY OUTPUT_DIRECTORY" >&2
  exit 2
fi

cadical_binary=$1
csp_binary=$2
output_directory=$3
geng_binary=${GENG_BINARY:-/opt/homebrew/bin/geng}
script_directory=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
audit_script="$script_directory/audit_base_pair_transcript_stream.py"

for executable in "$cadical_binary" "$csp_binary" "$geng_binary"; do
  if [[ ! -x "$executable" ]]; then
    echo "required executable is missing: $executable" >&2
    exit 2
  fi
done
if [[ ! -f "$audit_script" ]]; then
  echo "missing transcript auditor: $audit_script" >&2
  exit 2
fi

mkdir -p "$output_directory"

run_one() {
  local implementation=$1
  local binary=$2
  local shard=$3
  local prefix="$output_directory/${implementation}-shard${shard}"

  set -o pipefail
  "$geng_binary" -cq -d2 -D3 17 24:24 "${shard}/8" \
    2>"${prefix}.geng.log" |
    "$binary" --transcript --fail-on-violation \
      2>"${prefix}.classifier.log" |
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
  echo "one or more rooted order-17 shards failed" >&2
  exit 1
fi

echo "all sixteen rooted order-17 shards completed"
