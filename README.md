# Securing Digital Identity Data using Two-Layer Encryption and LSB Steganograpy

This project is one step ahead from the chapter provided in the Springer series "Applied Computing and Information Technology Volume-847" having the title "Elliptic Curve Cryptography and LSB Steganography for Securing Identity Data". [Link](https://link.springer.com/chapter/10.1007/978-3-030-25217-5_9)


## Description
In the chapter mentioned above, they have encrypted the data using ElGamalcryptosystem and further calculated the PSNR value of the images. By using Elgamalcryptosystem, we can generate the cipher text of double size as two cipher characters are used to seize one character of plain text. We have reduced this redundancy by applying Huffman encoding to the cipher text. This also add-on an extra level of security with reducing the size of cipher text produced, which further leads to improve the PSNR values of the images.


## Methods

Encryption process was defined as:

![Encryption](https://github.com/bhargav-roy/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/assets/79373109/a1361b46-9436-4e22-aeee-5fba9870cda9)


Decryption process was defined as:
![Decryption](https://github.com/bhargav-roy/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/assets/79373109/40e52999-7709-42c8-8102-ef6fa57ff581)

## Results

We have obtained a significant decrease in the size of cipher code. There was an improvement in the PSNR value obtained between the original and encrypted image. Also, we can see the negligible distortion between the original and encrypted image.
![Result](https://github.com/bhargav-roy/Securing-Digital-Identity-Data-using-Two-Layer-Encryption-LSB-Steganography/assets/79373109/bf26e3c3-7681-4b6e-834a-cd37eb285b66)
