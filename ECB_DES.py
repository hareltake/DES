import struct

from Util import to_binary, add_pads_if_necessary, dec_to_bin, bin_to_dec
from DES_Algorithm import DES, generate_keys

HEADER_LENGTH = (54 + 256 * 3) * 8

def split_header_and_content(img):
    """plain text to binary, split header and content for image
    """
    cipher_bits = []
    for i in img:
        cipher_bits.extend(to_binary(ord(i)))
    header_bits = cipher_bits[0: HEADER_LENGTH]
    text_bits = cipher_bits[HEADER_LENGTH:]
    return header_bits, text_bits


def encode(filename, keys):
    fi = open(filename, 'rb', )
    plaintext = fi.read()
    fi.close()

    header_bits, text_bits = split_header_and_content(plaintext)
    text_bits = add_pads_if_necessary(text_bits)

    final_cipher = ''
    for i in range(0, len(text_bits), 64):
        final_cipher += DES(text_bits, i, (i + 64), keys)

    # conversion of binary cipher into hex-decimal form
    fo = open("encrypted_ecb.bmp", "wb")
    header_str = ""
    for each in header_bits:
        header_str += str(each)
    final_cipher = header_str + final_cipher
    i = 0
    print("The length of final_cipher")
    print(len(final_cipher))
    while i < len(final_cipher) - 8:
        val = bin_to_dec(final_cipher[i:i + 4]) * 16 + bin_to_dec(final_cipher[i + 4:i + 8])
        fo.write(struct.pack('B', val))
        i += 8
    fo.close()
    print('the cipher is saved in encrypted_ecb.bmp')


def decode(filename, keys):
    fi = open(filename, "rb")
    cipher = fi.read()
    fi.close()
    cipher_bits = []
    header_str = ''

    for i in cipher:
        cipher_bits.extend(to_binary(ord(i)))

    header_bits = cipher_bits[0:HEADER_LENGTH]
    text_bits = cipher_bits[HEADER_LENGTH:]
    for i in header_bits:
        header_str += str(i)

    text_bits = add_pads_if_necessary(text_bits)

    keys.reverse()
    bin_mess = ''
    for i in range(0, len(text_bits), 64):
        bin_mess += DES(text_bits, i, (i + 64), keys)

    text_mess = header_str + bin_mess
    i = 0
    fo = open("decrypted_ecb.bmp", 'wb')
    print("The length of final_cipher")
    print(len(text_mess))
    while i < len(text_mess) - 8:
        val = bin_to_dec(text_mess[i:i + 4]) * 16 + bin_to_dec(text_mess[i + 4:i + 8])
        fo.write(struct.pack('B', val))
        i += 8
    fo.close()

    print('the original image has been saved in decrypted_ecb.bmp')


if __name__ == '__main__':
    keys = generate_keys('guogaoyang')
    encode('lena.bmp', keys)
    decode('encrypted_ecb.bmp', keys)