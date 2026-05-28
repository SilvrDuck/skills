#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  echo "usage: $0 input.d2 output.txt [extended|standard]" >&2
  exit 2
fi

input="$1"
output="$2"
mode="${3:-extended}"

case "$mode" in
  extended|standard) ;;
  *) echo "mode must be 'extended' or 'standard'" >&2; exit 2 ;;
esac

if ! command -v d2 >/dev/null 2>&1; then
  echo "missing dependency: d2" >&2
  echo "install D2, then rerun: d2 --ascii-mode $mode $input $output" >&2
  exit 127
fi

d2 --ascii-mode "$mode" "$input" "$output"
cat "$output"
