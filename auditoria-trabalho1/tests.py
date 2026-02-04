import time
import random

from main import GEN, ENC, DEC

# Metodos auxiliares para conversão entre texto e bits

def texto_para_bits(texto):
    bits = []
    for ch in texto:
        b = ord(ch)
        for i in range(7, -1, -1):
            bits.append((b >> i) & 1)
    return bits


def bits_para_texto(bits):
    texto = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            if i + j < len(bits):
                byte = (byte << 1) | bits[i + j]
        texto.append(chr(byte))
    return "".join(texto)


def ajustar_tamanho_bits(bits, tamanho):
    if len(bits) < tamanho:
        return bits + [0] * (tamanho - len(bits))
    if len(bits) > tamanho:
        return bits[:tamanho]
    return bits

# ============================================================================
# TESTES
# ============================================================================
def teste_basico():
    """Testa se criptografia e descriptografia funcionam"""
    print("\n" + "=" * 60)
    print("TESTE 1: Funcionalidade Básica")
    print("=" * 60)

    senha = "auditoria_e_seguranca"
    chave = GEN(senha)
    print(f"Senha: '{senha}'")
    print(f"Tamanho chave: {len(chave)} bits")

    mensagem = [random.randint(0, 1) for _ in range(len(chave))]
    #mensagem = texto_para_bits("The quick brown fox jumps over the lazy dog.")
    #mensagem = ajustar_tamanho_bits(mensagem, len(chave))
    amostra_msg = "".join(map(str, mensagem[:32]))
    print(f"Mensagem (amostra 32 bits): {amostra_msg}")

    inicio = time.time()
    cifra = ENC(chave, mensagem)
    tempo_enc = (time.time() - inicio) * 1000
    amostra_cifra = "".join(map(str, cifra[:32]))
    print(f"Cifra (amostra 32 bits):   {amostra_cifra}")
    print(f"Tempo ENC: {tempo_enc:.2f} ms")

    inicio = time.time()
    mensagem_recuperada = DEC(chave, cifra)
    tempo_dec = (time.time() - inicio) * 1000
    amostra_dec = "".join(map(str, mensagem_recuperada[:32]))
    print(f"Decifrado (amostra 32 bits): {amostra_dec}")
    print(f"Tempo DEC: {tempo_dec:.2f} ms")

    if mensagem == mensagem_recuperada:
        print("OK: Mensagem recuperada corretamente\n")
    else:
        print("ERRO: Mensagem não foi recuperada\n")


def teste_difusao():
    """Testa quantos bits mudam quando altera 1 bit da mensagem"""
    print("=" * 60)
    print("TESTE 2: Difusão (Efeito Avalanche)")
    print("=" * 60)

    chave = GEN("teste")
    mensagem1 = [0] * len(chave)

    mensagem2 = mensagem1.copy()
    mensagem2[0] = 1

    cifra1 = ENC(chave, mensagem1)
    cifra2 = ENC(chave, mensagem2)

    bits_mudaram = sum(1 for i in range(len(cifra1)) if cifra1[i] != cifra2[i])
    porcentagem = (bits_mudaram / len(cifra1)) * 100

    print("Alterado: 1 bit da mensagem")
    print(f"Bits alterados na cifra: {bits_mudaram} de {len(cifra1)}")
    print(f"Porcentagem: {porcentagem:.1f}%")

    if porcentagem >= 40:
        print("OK: Houve difusão\n")
    else:
        print("AVISO: Difusao pode melhorar\n")


def teste_confusao():
    """Testa quantos bits mudam quando altera 1 caractere da senha"""
    print("=" * 60)
    print("TESTE 3: Confusão (Mudança na Senha)")
    print("=" * 60)

    senha1 = "auditoria_e_seguranca"
    senha2 = "Auditoria_e_seguranca"

    chave1 = GEN(senha1)
    chave2 = GEN(senha2)

    mensagem = [1, 0] * (len(chave1) // 2)

    cifra1 = ENC(chave1, mensagem)
    cifra2 = ENC(chave2, mensagem)

    bits_mudaram = sum(1 for i in range(len(cifra1)) if cifra1[i] != cifra2[i])
    porcentagem = (bits_mudaram / len(cifra1)) * 100

    print(f"Senha 1: '{senha1}'")
    print(f"Senha 2: '{senha2}' (mudou 1 letra)")
    print(f"Bits alterados na cifra: {bits_mudaram} de {len(cifra1)}")
    print(f"Porcentagem: {porcentagem:.1f}%")

    if porcentagem >= 40:
        print("OK: Houve confusão\n")
    else:
        print("AVISO: Confusao pode melhorar\n")


def teste_chaves_equivalentes():
    """Verifica se senhas diferentes geram cifras diferentes"""
    print("=" * 60)
    print("TESTE 4: Chaves Equivalentes")
    print("=" * 60)

    senhas = ["teste1", "teste10", "maca", "banana", "laranja", "uva", "abacaxi", "melancia",
              "kiwi", "pera", "pessego", "manga", "caju", "goiaba",
              "jabuticaba", "pitanga", "graviola", "tangerina",
              "carambola", "framboesa", "amora", "mirtilo", "cereja"]

    cifras = {}
    colisoes = 0

    for senha in senhas:
        chave = GEN(senha)
        msg = [1, 0] * (len(chave) // 2)
        if len(msg) < len(chave):
            msg.append(1)
        cifra = ENC(chave, msg)
        cifra_str = "".join(map(str, cifra))

        if cifra_str in cifras:
            colisoes += 1
            print(f"  AVISO: Colisão entre '{senha}' e '{cifras[cifra_str]}'")
        else:
            cifras[cifra_str] = senha

    print(f"\nTestadas {len(senhas)} senhas diferentes")
    print(f"Colisões encontradas: {colisoes}")

    if colisoes == 0:
        print("OK: Nenhuma chave equivalente\n")
    else:
        print("AVISO: Foram encontradas chaves equivalentes\n")


def teste_performance():
    """Mede tempo de execução"""
    print("=" * 60)
    print("TESTE 5: Performance")
    print("=" * 60)

    senha = "senha_teste_123"

    inicio = time.time()
    chave = GEN(senha)
    tempo_gen = (time.time() - inicio) * 1000

    mensagem = [random.randint(0, 1) for _ in range(len(chave))]

    inicio = time.time()
    cifra = ENC(chave, mensagem)
    tempo_enc = (time.time() - inicio) * 1000

    inicio = time.time()
    _msg_dec = DEC(chave, cifra)
    tempo_dec = (time.time() - inicio) * 1000

    tempo_total = tempo_gen + tempo_enc + tempo_dec

    print(f"GEN: {tempo_gen:.2f} ms")
    print(f"ENC: {tempo_enc:.2f} ms")
    print(f"DEC: {tempo_dec:.2f} ms")
    print(f"TOTAL: {tempo_total:.2f} ms")



def main():
    """Executa todos os testes"""
    print("\n" + "=" * 60)
    print("  ESQUEMA CRIPTOGRÁFICO SIMPLIFICADO")
    print("  Python 3.10")
    print("=" * 60 + "\n")

    teste_basico()
    teste_difusao()
    teste_confusao()
    teste_chaves_equivalentes()
    teste_performance()

    print("=" * 60)
    print("TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
