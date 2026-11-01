#!/usr/bin/env python3
"""Decode a RED DSMC log using the extracted 1024-byte XOR table (exact).

    python3 decode_direct.py <enc_log> [out]

Uses log_xor_table.bin next to this script. Unlike decode_red_log.py, this is
exact and works on short logs (no statistical key recovery needed).
"""
import sys, os

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    tbl = open(os.path.join(os.path.dirname(__file__), 'log_xor_table.bin'), 'rb').read()
    data = open(sys.argv[1], 'rb').read()
    out = bytes(c ^ tbl[i & 0x3FF] for i, c in enumerate(data))
    dst = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1] + '.decoded'
    open(dst, 'wb').write(out)
    print('Decoded:', dst)

if __name__ == '__main__':
    main()
