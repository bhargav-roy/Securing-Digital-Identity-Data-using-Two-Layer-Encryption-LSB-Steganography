# import libraries
import sys
import numpy as np
from PIL import Image

np.set_printoptions(threshold=sys.maxsize)


# def Binary(s):
#     return ''.join([format(ord(i), "08b") for i in s])


# encoding function
def Encode(src, message, dest):
    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n
    message += '$rbr9'
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < len(b_message):
                    if int(b_message[index], 2) == 1 and int(bin(array[p][q])[-1], 2) == 0:
                        array[p][q] += 1
                    elif int(b_message[index], 2) == 0 and int(bin(array[p][q])[-1], 2) == 1:
                        array[p][q] -= 1
                    index += 1
                # if index < req_pixels:
                #
                #     # array[p][q] = int(bin(array[p][q])[-1] + b_message[index], 2)
                #     # index += 1

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")


#
# def decode(src,msg_length):
#     img = Image.open(src, 'r')
#     array = np.array(list(img.getdata()))
#     message=''
#     if img.mode == 'RGB':
#         n = 3
#     elif img.mode == 'RGBA':
#         n = 4
#
#     total_pixels = array.size // n
#
#     for p in range(total_pixels):
#         for q in range(0,3):
#             if len(message)<msg_length:
#                 message+=bin(array[p][q])[-1]
#     return message

# decoding function
def Decode(src):
    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[-1])

    hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$rbr9":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$rbr9" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")


