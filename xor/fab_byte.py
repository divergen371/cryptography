from pwn import *


data = bytes.fromhex(
    "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
)


for i in range(127):
    f = xor(data, bytes(chr(i), "utf-8"))
    flag = f.decode("utf-8")
    if "crypto" in flag:
        print(flag)
