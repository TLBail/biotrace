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


def hex_to_double(hex1, hex2, hex3, hex4, endian=0):
    # Convertir les valeurs hexadécimales en bits
    bits = struct.pack('>HHHH', hex1, hex2, hex3, hex4)
    # Convertir les bits en nombre flottant
    double_num = struct.unpack('>d', bits)[0]
    if endian:
        double_num = struct.unpack('<d', bits)[0]
    return double_num


def hex_to_int(hex1, hex2, endian=0):
    # Convertir les valeurs hexadécimales en bits
    bits = struct.pack('>HH', hex1, hex2)
    # Convertir les bits en nombre entier
    int_num = struct.unpack('>i', bits)[0]
    if endian:
        int_num = struct.unpack('<i', bits)[0]
    return int_num


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


def double_to_hex(double_num, endian=0):
    # Convertir le double en binaire
    bits = struct.pack('>d', double_num)
    if endian:
        bits = struct.pack('<d', double_num)
    # Extraire les deux mots de 16 bits
    word1, word2, word3, word4 = struct.unpack('>HHHH', bits[:8])  # 8 premiers octets
    # Convertir chaque mot en hexadecimal
    # hex1, hex2 = hex(word1), hex(word2)
    # Retourner les deux valeurs décimales
    return word1, word2, word3, word4


def int_to_hex(int_num, endian=0):
    # Convertir le int en binaire
    bits = struct.pack('>i', int_num)
    if endian:
        bits = struct.pack('<i', int_num)
    # Extraire les deux mots de 16 bits
    word1, word2 = struct.unpack('>HH', bits[:4])  # 4 premiers octets
    # Convertir chaque mot en hexadecimal
    # hex1, hex2 = hex(word1), hex(word2)
    # Retourner les deux valeurs décimales
    return word1, word2