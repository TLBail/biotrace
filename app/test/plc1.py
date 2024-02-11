#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------#
# programme: plc1.py                                                    #
# Modbus TCP                                                            #
# Si le port 502, ou 503 est utilisé, l'exécution doit se faire avec    #
# les privilèges de root du fait de l'écoute sur un port <= 1024.       #
# Utilitaire EasyModbus Client accessible depuis le lien ci-dessous:    #
# https://sourceforge.net/projects/easymodbustcp/                       #
#                                                                       #
# répertoire : /u/data/prog/modbus/master/apps                          #
# Création du mercredi 25 octobre 2023                                  #
# Modification du jeudi 21 décembre 2023                                #
#-----------------------------------------------------------------------#

#----------< Modules >--------------------------------------------------#
import sys
import threading, multiprocessing
import struct
from bitlist import bitlist     # $ pip install bitlist
from pyModbusTCP import utils   # $ pip install pyModbusTCP
from pyModbusTCP.server import ModbusServer, DataHandler, DataBank
from pyModbusTCP.constants import EXP_ILLEGAL_FUNCTION
import psutil                   # $ pip install psutil

#----------< Constantes >-----------------------------------------------#
WD142  = '127.0.0.1'
NIPOGI = '127.0.0.1'
PC     = '127.0.0.1'
PC2    = '127.0.0.1'
ALLOW_R_L = [NIPOGI, WD142, PC, PC2]
ALLOW_W_L = [NIPOGI, WD142, PC, PC2]
PORT_MODBUS = 8502  # Habituellement 502

#---------< Classe >----------------------------------------------------#
class MyDataHandler(DataHandler):
    ###########################################################
    # FC1: lecture Coils (relais, moteurs, tout ou rien bits) #
    ###########################################################
    def read_coils(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            print('FC1', ' address->', address, ' count->', count)
            etats = fc1Handle(address, count)
            super().write_coils(address, etats, srv_info)
            return super().read_coils(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
            
    ##########################################################################
    # FC2: lecture Discrete Inputs (commutateurs, fins de courses, TOR bits) #
    ##########################################################################
    def read_d_inputs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            print('FC2', ' address->', address, ' count->', count)
            etats = fc2Handle(address, count)
            mbServer.data_bank.set_discrete_inputs(address, etats)
            return super().read_d_inputs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
            
    ##########################################################################
    # FC3: lecture Holding Registers (afficheurs, indicateurs, mots 16 bits) #
    ##########################################################################
    def read_h_regs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            words_l = fc3Handle(address, count)
            print('FC3', ' address->', address, ' count->', count, '  ', words_l)
            super().write_h_regs(address, words_l, srv_info)
            return super().read_h_regs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    #########################################################
    # FC4: lecture Input Registers (capteurs, mots 16 bits) #
    #########################################################
    def read_i_regs(self, address, count, srv_info):
        if srv_info.client.address in ALLOW_R_L:
            words_l = fc4Handle(address, count)
            print('FC4', ' address->', address, ' count->', count, '  ', words_l)
            mbServer.data_bank.set_input_registers(address, words_l)
            return super().read_i_regs(address, count, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    #############################
    # FC5: ecriture Single Coil #
    #############################
    def write_coils(self, address, bits_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            print('FC5', ' address->', address, ' bits_l->', bits_l)
            return super().write_coils(address, bits_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)

    ##################################
    # FC6: ecriture Holding Register #
    ##################################
    def write_h_regs(self, address, words_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            print('FC6', ' address->', address, ' words_l->', words_l)
            return super().write_h_regs(address, words_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
            
    #################################
    # FC15: ecriture Multiple Coils #
    #################################
    def write_multiple_coils(self, address, bits_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            print('FC15', ' address->', address, ' bits_l->', bits_l)
            return super().write_multiple_coils(address, bits_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
    
    #####################################
    # FC16: ecriture Multiple Registers #
    #####################################
    def write_multiple_registers(self, address, words_l, srv_info):
        if srv_info.client.address in ALLOW_W_L:
            print('FC16', ' address->', address, ' words_l->', words_l)
            return super().write_multiple_registers(address, words_l, srv_info)
        else:
            return DataHandler.Return(exp_code=EXP_ILLEGAL_FUNCTION)
            
#----------< Fonction de codage des nombres flottants sur 32 bits >-----#
# Non signé, non inversé
def float_to_hex(float_num, endian='big'):
    # Convertir le float en binaire
    bits = struct.pack('>f', float_num)
    if endian == 'little':
        bits = struct.pack('<f', float_num)
    # Extraire les deux mots de 16 bits
    word1, word2 = struct.unpack('>HH', bits[:4]) # 4 premiers octets
    # Convertir chaque mot en hexadecimal
    # hex1, hex2 = hex(word1), hex(word2)
    # Retourner les deux valeurs décimales
    return word1, word2
    
#----------< Fonction de décodage des nombres flottants sur 32 bits >-----#
def hex_to_float(hex1, hex2, endian='big'):
    # Convertir les valeurs hexadécimales en bits
    bits = struct.pack('>HH', hex1, hex2)
    # Convertir les bits en nombre flottant
    float_num = struct.unpack('>f', bits)[0]
    if endian == 'little':
        float_num = struct.unpack('<f', bits)[0]
    return float_num
    
#----------< Fonction acquisition de données FC1 >----------------------#
''' Read Coils:
    De 1 à 2.000 valeurs booleenes, plage d'adresses de 1 à 9.999 '''
def fc1Handle(address, count):
    value = bitlist()
    if (address == 1):
        value = bitlist('1001011')
    return(value)

#----------< Fonction acquisition de données FC2 >----------------------#
''' Read Discrete Inputs:
    De 1 à 2.000 valeurs booleennes, plage d'adresses de 10.000 à 19.999 '''
def fc2Handle(address, count):
    value = bitlist()
    if (address >= 10000) and (address <= 19999):
        value = bitlist('110111')
    return(value)
    
#----------< Fonction acquisition de données FC3 >----------------------#
''' Read Holding Register:
    De 1 à 125 mots de 16 bits, plage d'adresses de 40.000 à 49.999 '''
def fc3Handle(address, count):
    value = [0]
    if (address >= 40000) and (address <=49999):
        if (address == 40001):
            value = [625, -512, 1025]   # 3 valeurs
        if (address == 45000):
            # Les nombres flottants sont codifiès sur 32 bits norme IEE754
            # Exemple value = [0x4049, 0x0FD0] pour 3.14159
            value = 3.14159 # pi
            word1, word2 = float_to_hex(value)
            value = [word1, word2]
    return(value)

#----------< Fonction acquisition de données FC4 >----------------------#
''' Read Input Register:
    De 1 à 125 mots de 16 bits, plage d'adresses de 30.000 à 39.999 '''
def fc4Handle(address, count):
    print('FC4', ' address->', address, ' count->', count)
    value = [0]
    if (address >= 30000) and (address <= 39999):
        if (address == 30001):
            value = [55, -612, -227, 1415, 2568]    # 5 valeurs
            #        55;64924;65309; 1415; 2568 si data unsigned
            #        55; -612; -227; 1415; 2568 si data signed
    return(value)

#----------< Lecture des températures CPU >-----------------------------#
def get_cpu_temperature():
    try:
        if os.name == 'posix':
            # Sur les systèmes Linux, la température de la CPU est généralement dans le fichier thermal_zone
            # Vous devrez peut-être ajuster le chemin du fichier en fonction de votre système.
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                temp0 = file.read()
                temperature0 = int(temp0) / 1000  # Convertir en degrés Celsius
            with open("/sys/class/thermal/thermal_zone1/temp", "r") as file:
                temp1 = file.read()
                temperature1 = int(temp1) / 1000  # Convertir en degrés Celsius
        else:
            temperature0 = 0
            tempertaure1 = 0
        l_temp = [temperature0, temperature1]
        return l_temp
    except Exception as e:
        return None
        
#----------< Fonction principale >--------------------------------------#
def main():
    global mbServer
    mbServer = ModbusServer(host="127.0.0.1", port=PORT_MODBUS, no_block=False, data_hdl=MyDataHandler())
    print('Serveur start')
    mbServer.start()

    mbServer.stop()
    print('Serveur stop')
    
#----------< Démarrage programme >--------------------------------------#
if __name__ == '__main__':
    verrou = threading.Lock()
    t1 = threading.Thread(target=main)
    t1.start()
    sys.exit(0)
