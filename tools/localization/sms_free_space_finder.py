import os
import sys

def escanear_espaco_livre(rom_path, tamanho_minimo=64, tam_banco=0x4000):
    if not os.path.exists(rom_path):
        print(f"Erro: Arquivo '{rom_path}' não encontrado!")
        return

    with open(rom_path, "rb") as f:
        rom = f.read()

    total_tamanho = len(rom)
    total_bancos = total_tamanho // tam_banco

    print("=" * 75)
    print(f"🔍 MAPEADOR DE ESPAÇO LIVRE (SMS) - ROM: {os.path.basename(rom_path)}")
    print(f"Tamanho Total: {total_tamanho // 1024} KB | Bancos de 16KB: {total_bancos}")
    print(f"Filtro: Blocos vazios contíguos de no mínimo {tamanho_minimo} bytes")
    print("=" * 75)

    espaco_total_livre = 0

    for banco in range(total_bancos):
        banco_inicio = banco * tam_banco
        banco_fim = banco_inicio + tam_banco
        dados_banco = rom[banco_inicio:banco_fim]

        em_bloco = False
        ini_bloco = 0
        byte_padrao = 0
        blocos_encontrados = []

        for i, b in enumerate(dados_banco):
            addr = banco_inicio + i
            if not em_bloco:
                if b in (0x00, 0xFF):
                    em_bloco = True
                    ini_bloco = addr
                    byte_padrao = b
            else:
                if b != byte_padrao:
                    tam = addr - ini_bloco
                    if tam >= tamanho_minimo:
                        blocos_encontrados.append((ini_bloco, addr - 1, tam, byte_padrao))
                        espaco_total_livre += tam
                    em_bloco = False

        if em_bloco:
            tam = banco_fim - ini_bloco
            if tam >= tamanho_minimo:
                blocos_encontrados.append((ini_bloco, banco_fim - 1, tam, byte_padrao))
                espaco_total_livre += tam

        print(f"\n📁 BANCO {banco:02d} (0x{banco_inicio:05X} a 0x{banco_fim - 1:05X}):")
        if not blocos_encontrados:
            print("   ⚠️ ATENÇÃO: 0 bytes livres! Banco 100% entupido (proibido injetar código).")
        else:
            for ini, fim, tam, val in blocos_encontrados:
                offset_banco = ini - banco_inicio
                print(f"   [✓] 0x{ini:05X} a 0x{fim:05X} ({tam:4d} bytes livres de 0x{val:02X}) | Offset no Banco: 0x{offset_banco:04X}")

    print("\n" + "=" * 75)
    print(f"Espaço livre total na ROM: {espaco_total_livre} bytes ({espaco_total_livre // 1024} KB)")
    print("=" * 75)

if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "SpellCaster (USA, Europe).sms"
    escanear_espaco_livre(arquivo)