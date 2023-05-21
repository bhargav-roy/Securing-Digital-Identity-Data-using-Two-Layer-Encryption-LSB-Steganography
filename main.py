from LSB_HFM import encode_hfm, decode_hfm
from hoffmanencoding import Node, Calculate_Codes, Calculate_Probability, Output_Encoded, Total_Gain, Huffman_Encoding, Huffman_Decoding
from LSB_ECC import Encode, Decode
from ECC import EllipticCurveCryptography, Point
from math import inf
import random
import sys
import cv2
import numpy as np
from PSNR import PSNR
np.set_printoptions(threshold=sys.maxsize)


# Alphabets used for storing the data
Alphabets = 'abcdefghijklmnopqrstuvwxyz0123456789#.+-'

# the E(a,b,p) finite elliptic curve
a, b, p = 1, 6, 37
ecc = EllipticCurveCryptography(a, b, p)

# Generating points of the elliptic curve over field Fp
Points = []
for i in range(p):
    for j in range(p):
        if pow(j, 2) % p == (pow(i, 3) + a * i + b) % p:
            Points.append(Point(i, j))
# Including Point of infinity
Points.append(Point(inf, inf))

# Defining Public Keys
G = Point(2, 4)  # Generator Point
H = ecc.double_and_add(5, G)  # d=5 is the private key
# print(H)
# Creating dictionary for assigning points to alphabets
Assign = {}
for i in range(len(Alphabets)):
    Assign[Alphabets[i]] = Points[i]


# Helping function for getting key from value
def get_key(val):
    for key, value in Assign.items():
        if val == value:
            return key
    return "key doesn't exist"


# Creating ECC encoding Function
def ecc_encoding(plain_text, e1, e2):
    cipher_text = ''
    for i in plain_text:
        r = random.randint(2, len(Assign) + 1)
        C1 = ecc.double_and_add(r, e1)
        C2 = ecc.point_addition(Assign[i], ecc.double_and_add(r, e2))
        T1 = get_key(C1)
        T2 = get_key(C2)
        cipher_text = cipher_text + T1 + T2
    return cipher_text


# Creating ECC Decoding Function
def ecc_decoding(cipher_text, private_key):
    plain_text = ''
    for i in range(0, len(cipher_text), 2):
        C1 = Assign[cipher_text[i]]
        C2 = Assign[cipher_text[i + 1]]
        M = ecc.point_addition(C2, -ecc.double_and_add(private_key, C1))
        M.x %= p
        M.y %= p
        plain_text = plain_text + get_key(M)
    return plain_text


# Generating Plain Text of various sizes
Plain_Text_1 = 'arvind#kumar#rakesh#kumar#sanjanadevi#123456789#b-45#ajay#tenament#maninagar#ahmedabad#gujarat'
Plain_Text_2 = Plain_Text_1 * 10
Plain_Text_3 = Plain_Text_1 * 30

# Generating Cipher Text from Plain Text using ECC
Cipher_Text_1 = ecc_encoding(Plain_Text_1, G, H)
Cipher_Text_2 = ecc_encoding(Plain_Text_2, G, H)
Cipher_Text_3 = ecc_encoding(Plain_Text_3, G, H)

# Encrypting Cipher Text in Lena image without HFM encoding
Encode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', Cipher_Text_1,
       'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt1.png')
Encode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', Cipher_Text_2,
       'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt2.png')
Encode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', Cipher_Text_3,
       'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt3.png')


# Calculating PSNR without HFM
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt1.png')))
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt2.png')))
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt3.png')))

# Decoding & Checking with Cipher Text
Decode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt1.png')
print(Cipher_Text_1)
Decode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt2.png')
print(Cipher_Text_2)
Decode('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_ECC/Encrypt3.png')
print(Cipher_Text_3)

# Encoding Cipher_text through Huffman encoding
print("Encoding Details For Cipher_Text_1:")
encoding1, tree1 = Huffman_Encoding(Cipher_Text_1)
print("Encoding Details For Cipher_Text_2:")
encoding2, tree2 = Huffman_Encoding(Cipher_Text_2)
print("Encoding Details For Cipher_Text_3:")
encoding3, tree3 = Huffman_Encoding(Cipher_Text_3)

# Ecrypting the Encoded code using LSB
encode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', encoding1,
           'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt1.png')
encode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', encoding2,
           'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt2.png')
encode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png', encoding3,
           'E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt3.png')

# calculating PSNR with HFM
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt1.png')))
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt2.png')))
print(PSNR(cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/Lena.png'),
      cv2.imread('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt3.png')))


# Decoding Encoded Text & checking
decode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt1.png', len(encoding1))
print(encoding1)
decode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt2.png', len(encoding2))
print(encoding2)
decode_hfm('E:/Github/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/Data/LSB_HFM/Encrypt3.png', len(encoding3))
print(encoding3)
