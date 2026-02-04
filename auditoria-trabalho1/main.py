"""
Atividadde 1 de Auditoria e Segurança da Informação: Implementação de Esquema Criptográfico Simplificado
Nome: Amanda Ferreira
Matricula: 12211BSI225
"""

import hashlib
import time
import random


def GEN(seed: list[int]) -> list[int]:
    """Gera chave binária de tamanho 4 * len(seed)"""
    if not all(isinstance(bit, int) for bit in seed):
        raise ValueError("A seed deve ser uma lista de inteiros")
    if not all(bit in (0, 1) for bit in seed):
        raise ValueError("A seed deve conter apenas 0 e 1")

    tamanho_chave = 4 * len(seed)

    # Converte lista de bits em bytes para gerar o hash
    byte_val = 0
    packed_bytes = bytearray()
    for i, bit in enumerate(seed):
        byte_val = (byte_val << 1) | bit
        if (i + 1) % 8 == 0:
            packed_bytes.append(byte_val)
            byte_val = 0
    if len(seed) % 8 != 0:
        remaining = 8 - (len(seed) % 8)
        packed_bytes.append(byte_val << remaining)

    hash_bytes = hashlib.sha256(bytes(packed_bytes)).digest()

    
    # Converte bytes para bits
    chave = []
    for byte in hash_bytes:
        #print(f"byte: {byte}")
        for i in range(8):
            chave.append((byte >> (7 - i)) & 1)
            #print(f"  bit: {(byte >> (7 - i)) & 1}")
            if len(chave) == tamanho_chave:
                return chave
    
    return chave[:tamanho_chave]


def ENC(key, msg):
    """Criptografa mensagem M com chave K"""
    if len(key) != len(msg):
        print("Chave e mensagem estão com tamanhos diferentes")
    
    n = len(key)

    # Passo 1: XOR da mensagem com a chave (^), resulta em uma cifra intermediaria
    C = [key[i] ^ msg[i] for i in range(n)]

    # Passo 2: Difusão reversível (XOR em cadeia) 
    for i in range(1, n):
        C[i] = C[i] ^ C[i - 1]

    return C


def DEC(key, cifra):
    """Descriptografa cifra C com chave K"""
    if len(key) != len(cifra):
        print("Chave e cifra estão com tamanhos diferentes")
    
    n = len(key)

    # Passo 1: Desfazer difusão (XOR em cadeia reverso) 
    result = cifra.copy()
    for i in range(n - 1, 0, -1):
        result[i] = result[i] ^ result[i - 1]

    # Passo 2: XOR com chave para recuperar a mensagem original
    M = [key[i] ^ result[i] for i in range(n)]
    return M





