#!/usr/bin/env python3
"""Decrypt a RED ONE `redone.su` firmware upgrade file (build 16+ / v3.x).

Format:
  redone.su is a plain POSIX tar. Members:
    redone.1 = openssl `enc` AES-256-CBC (Salted__ + 8B salt), MD5 KDF -> gzip -> VxWorks PPC405 image (SundanceBootable)
    redone.2 = 128-byte RSA-1024 signature over redone.1
    redone.3 = same enc -> gzip -> Xilinx FPGA bitstream (iofpga_top)
    redone.4 = 128-byte RSA-1024 signature over redone.3
Passphrase recovered from the b16 VxWorks image string table.
  openssl enc -d -aes-256-cbc -md md5 -pass pass:<KEY>
Pre-encryption (build 15 / v2.2.x) `su.tar` shipped iofpga_top.bin.gz + SundanceBootable.bin.gz in the clear.
"""
import sys, os, tarfile, hashlib, gzip, io
KEY = b"M1H5gwOXh757rIRVY6Gj2tN080AYSX03"

def bytes_to_key(passwd, salt, klen=32, ivlen=16):
    d=b''; prev=b''
    while len(d)<klen+ivlen:
        prev=hashlib.md5(prev+passwd+salt).digest(); d+=prev
    return d[:klen], d[klen:klen+ivlen]

def dec(blob):
    assert blob[:8]==b"Salted__", "not openssl Salted__"
    salt=blob[8:16]; body=blob[16:]
    k,iv=bytes_to_key(KEY,salt)
    try:
        from Crypto.Cipher import AES
        pt=AES.new(k,AES.MODE_CBC,iv).decrypt(body)
    except ImportError:
        import subprocess
        pt=subprocess.run(["openssl","enc","-d","-aes-256-cbc","-md","md5","-pass",f"pass:{KEY.decode()}"],
                          input=blob, capture_output=True).stdout
        return pt
    pad=pt[-1]
    if 1<=pad<=16: pt=pt[:-pad]
    return pt

def main():
    if len(sys.argv)<2:
        print("usage: redone_su_decrypt.py redone.su [outdir]"); sys.exit(1)
    su=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else "redone_out"
    os.makedirs(out,exist_ok=True)
    with tarfile.open(su) as t:
        for m in t.getmembers():
            data=t.extractfile(m).read()
            if m.name.endswith((".1",".3")):
                plain=dec(data)
                raw=gzip.decompress(plain)
                base="SundanceBootable" if m.name.endswith(".1") else "iofpga_top"
                open(os.path.join(out,base+".bin"),"wb").write(raw)
                print(f"{m.name}: decrypted+inflated -> {base}.bin ({len(raw)} B)")
            else:
                open(os.path.join(out,m.name+".sig"),"wb").write(data)
                print(f"{m.name}: RSA-1024 signature ({len(data)} B) saved")
if __name__=="__main__": main()
