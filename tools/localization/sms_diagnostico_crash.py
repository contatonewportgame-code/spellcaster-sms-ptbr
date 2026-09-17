import os

ROM_ORIGINAL = "SpellCaster (USA, Europe).sms"
ROM_MODIFICADA = "SpellCaster (PT-BR).sms"

def gerar_diagnostico():
    if not os.path.exists(ROM_ORIGINAL) or not os.path.exists(ROM_MODIFICADA):
        print("Erro: ROMs não encontradas para diagnóstico!")
        return

    with open(ROM_ORIGINAL, "rb") as f:
        orig = bytearray(f.read())
    with open(ROM_MODIFICADA, "rb") as f:
        mod = bytearray(f.read())

    print("=" * 78)
    print("🔬 DIAGNÓSTICO DE FALHA POR ISOLAMENTO DE BANCOS (ANTI-CRASH)")
    print("=" * 78)

    # Mapeia quais bancos foram alterados
    tam_banco = 0x4000
    total_bancos = len(orig) // tam_banco
    bancos_alterados = []

    for b in range(total_bancos):
        ini = b * tam_banco
        fim = ini + tam_banco
        difs = sum(1 for i in range(ini, fim) if orig[i] != mod[i])
        if difs > 0:
            bancos_alterados.append((b, ini, fim, difs))
            print(f"[*] Banco {b:02d} (0x{ini:05X} a 0x{fim-1:05X}): {difs:5d} bytes modificados")

    print("=" * 78)
    print("Gerando ROMs de teste isoladas para identificar o culpado exato...")

    # Dicionário de testes de isolamento (reverte apenas 1 componente para o original)
    testes = [
        ("diag_1_sem_banco17.sms", [(0x44000, 0x48000)], "Banco 17 revertido (Epílogo e Créditos)"),
        ("diag_2_sem_banco24.sms", [(0x60000, 0x64000)], "Banco 24 revertido (Yakisoba original)"),
        ("diag_3_sem_banco31.sms", [(0x7C000, 0x80000)], "Banco 31 revertido (História Parte 2)"),
        ("diag_4_sem_banco19.sms", [(0x4C000, 0x50000)], "Banco 19 revertido (Menus originais)"),
        ("diag_5_sem_banco12.sms", [(0x30000, 0x34000)], "Banco 12 revertido (Oásis original)"),
    ]

    for nome_arquivo, faixas, descricao in testes:
        rom_teste = bytearray(mod) # Começa com a tradução completa
        for ini, fim in faixas:
            rom_teste[ini:fim] = orig[ini:fim] # Restaura só essa área para a original da Sega
        
        with open(nome_arquivo, "wb") as f:
            f.write(rom_teste)
        print(f"[✓] Gerada: '{nome_arquivo}' ➔ {descricao}")

    print("=" * 78)
    print("👉 TESTE RÁPIDO NO EMULICIOUS:")
    print("   Abra 'diag_1_sem_banco17.sms', 'diag_2...', clique em JOGAR.")
    print("   A que abrir o Templo do Cume revela exatamente quem causou a tela preta!")
    print("=" * 78)

if __name__ == "__main__":
    gerar_diagnostico()
