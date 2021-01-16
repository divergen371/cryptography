from pwn import *  # pip install pwntools
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
import base64
import codecs
import random
from binascii import unhexlify

r = remote("socket.cryptohack.org", 13377, level="debug")


def json_recv():
    line = r.recvline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


def list_to_string(s):
    output = ""
    return output.join(s)


for i in range(1, 102):
    received = json_recv()
    if "flag" in received:
        print(f"\n Flag: {received['flag']}")
        break
    print(f"\n cycle: {i}")
    print(f"Received type: {received['type']}")
    print(f"Received encoded value: {received['encoded']}")
    word = received["encoded"]
    enc = received["type"]

    if enc == "base64":
        dec = base64.b64decode(word).decode("utf8").replace("'", '"')
    elif enc == "hex":
        dec = (unhexlify(word)).decode("utf8").replace("'", '"')
    elif enc == "rot13":
        dec = codecs.decode(word, "rot_13")
    elif enc == "bigint":
        dec = unhexlify(word.replace("0x", "")).decode("utf8").replace("'", '"')
    elif enc == "utf-8":
        dec = list_to_string([chr(b) for b in word])

    print(f"Decoded: {dec}")
    print(f"Decoded type: {type(dec)}")

    to_send = {"decoded": dec}
    json_send(to_send)
