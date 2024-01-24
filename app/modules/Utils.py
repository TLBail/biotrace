import struct

# Big endian: 0
# Little endian: 1


def hex_to_float(hex1, hex2, endian=0):
    # Convertir les valeurs hexadécimales en bits
    bits = struct.pack('>HH', hex1, hex2)
    # Convertir les bits en nombre flottant
    float_num = struct.unpack('>f', bits)[0]
    if endian:
        float_num = struct.unpack('<f', bits)[0]
    return float_num


def float_to_hex(float_num, endian=0):
    # Convertir le float en binaire
    bits = struct.pack('>f', float_num)
    if endian:
        bits = struct.pack('<f', float_num)
    # Extraire les deux mots de 16 bits
    word1, word2 = struct.unpack('>HH', bits[:4])  # 4 premiers octets
    # Convertir chaque mot en hexadecimal
    # hex1, hex2 = hex(word1), hex(word2)
    # Retourner les deux valeurs décimales
    return word1, word2
