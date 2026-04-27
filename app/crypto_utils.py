from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad

reference_DNA = {'00':'A','01':'T','10':'C','11':'G'}

def blowfish_encrypt(text, key):
    cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
    return cipher.encrypt(pad(text.encode(), Blowfish.block_size))

def blowfish_decrypt(cipher_text, key):
    cipher = Blowfish.new(key.encode(), Blowfish.MODE_ECB)
    return unpad(cipher.decrypt(cipher_text), Blowfish.block_size).decode()

def encrypt_to_fake_DNA(cipher_text):
    binary = ''.join(format(b,'08b') for b in cipher_text)
    return binary_to_fake_DNA(binary)

def decrypt_fake_DNA(fake_dna):
    binary = fake_DNA_to_binary(fake_dna)
    return bytes(int(binary[i:i+8],2) for i in range(0,len(binary),8))

def binary_to_fake_DNA(binary):
    dna=""
    for i in range(0,len(binary),2):
        dna+=reference_DNA[binary[i:i+2]]
    return dna

def fake_DNA_to_binary(dna):
    binary=""
    for ch in dna:
        for k,v in reference_DNA.items():
            if v==ch:
                binary+=k
    return binary

def dna_to_binary(dna):
    return fake_DNA_to_binary(dna)
