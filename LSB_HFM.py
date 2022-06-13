import numpy as np
from PIL import Image
import sys


def encode_hfm(src, message, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n
    req_pixels = (len(message)//n)+ len(message)%n

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < len(message):
                    if int(message[index],2) == 1 and int(bin(array[p][q])[-1], 2) == 0:
                        array[p][q] += 1
                    elif int(message[index], 2) == 0 and int(bin(array[p][q])[-1], 2) == 1:
                        array[p][q] -= 1
                    index +=1

    array = array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    enc_img.save(dest)
    print("Image Encoded Successfully")


def decode_hfm(src,msg_length):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))
    message=''
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    for p in range(total_pixels):
        for q in range(0,3):
            if len(message)<msg_length:
                message+=bin(array[p][q])[-1]
    print(message)

# message='00110111101101101100110100101111001001100010111000001110100010111010100100100100101001010010001101000110001010000011000011100000111011010000101010011011000110111010011101011111010110110010001000001001101010011001100101101001010000001110001010010110111010000111111000010100000000011010110100100110110001101110000010011010011000000001110000010101011000101010010000001100100001010000101000111111110010000001110110000010001000000100000001110100010001100101101111101010110011000011001010011011011100011101010101010010111001000010001101010100001100100101101110111000011010110011100110100000000111110011110111110100110100110111100000111110101010101011110001100011110001000001100000111100001000001101101110011110100011011001011111101010111001110011110011110001111000101'
# src='C:/Users/Lenovo/Downloads/Lena.png'
# dest='C:/Users/Lenovo/Downloads/Encrypt.png'
# #encode_hfm(src,message,dest)
# decode_hfm(dest,len(message))