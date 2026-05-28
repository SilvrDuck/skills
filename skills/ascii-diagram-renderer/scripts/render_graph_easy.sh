#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 input.ge output.txt [boxart|ascii]" >&2
  exit 2
fi

input="$1"
output="$2"
mode="${3:-boxart}"

case "$mode" in
  boxart|ascii) ;;
  *) echo "mode must be 'boxart' or 'ascii'" >&2; exit 2 ;;
esac

if ! command -v graph-easy >/dev/null 2>&1; then
  echo "missing dependency: graph-easy" >&2
  echo "install Graph::Easy, then rerun: graph-easy --as=$mode < $input > $output" >&2
  exit 127
fi

graph-easy --as="$mode" < "$input" > "$output"
cat "$output"
