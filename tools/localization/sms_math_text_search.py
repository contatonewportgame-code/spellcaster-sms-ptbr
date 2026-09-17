import os
import sys

def busca_relativa(rom_path, palavra):
    if not os.path.exists(rom_path):
        print(f"Erro: Arquivo '{rom_path}' não encontrado!")
        return

    with open(rom_path, "rb") as f:
        rom = f.read()

    palavra = palavra.upper()
    print("=" * 75)
    print(f"🔬 BUSCA MATEMÁTICA RELATIVA: '{palavra}'")
    print(f"Analisando assinatura relativa entre letras em todas as 256 bases...")
    print("=" * 75)

    # Calcula deltas relativos à letra 'A' (base 0)
    deltas = [ord(c) - ord('A') for c in palavra if 'A' <= c <= 'Z']
    if len(deltas) != len(palavra):
        print("Aviso: Apenas caracteres A-Z são suportados na busca relativa padrão.")

    # 1. Busca em 1 Byte por caractere
    print("\n[MODO 1: Bytes Contíguos / Texto Linear]")
    achou_modo1 = False
    for base in range(256):
        padrao = bytes([(base + d) & 0xFF for d in deltas])
        pos = 0
        while True:
            idx = rom.find(padrao, pos)
            if idx == -1:
                break
            banco = idx // 0x4000
            offset_banco = idx % 0x4000
            print(f"  🎯 Encontrado em 0x{idx:05X} (Banco {banco:02d}, Offset 0x{offset_banco:04X}) | Base do 'A' = 0x{base:02X}")
            pos = idx + 1
            achou_modo1 = True

    if not achou_modo1:
        print("  [-] Nenhuma ocorrência em formato de 1 byte contíguo.")

    # 2. Busca em 2 Bytes por caractere (Padrão Tilemap VDP: Tile ID + Atributo)
    print("\n[MODO 2: Padrão Tilemap VDP (Tile ID + Atributo Intercalado)]")
    atributos_sms = [0x00, 0x01, 0x04, 0x05, 0x08, 0x09, 0x0C, 0x0D]
    achou_modo2 = False
    for base in range(256):
        for attr in atributos_sms:
            padrao = bytearray()
            for d in deltas:
                padrao.append((base + d) & 0xFF)
                padrao.append(attr)

            pos = 0
            while True:
                idx = rom.find(bytes(padrao), pos)
                if idx == -1:
                    break
                banco = idx // 0x4000
                offset_banco = idx % 0x4000
                print(f"  🎯 Encontrado Tilemap em 0x{idx:05X} (Banco {banco:02d}) | Base 'A' = 0x{base:02X} | Atributo = 0x{attr:02X}")
                pos = idx + 1
                achou_modo2 = True

    if not achou_modo2:
        print("  [-] Nenhuma ocorrência em formato Tilemap VDP.")

    print("=" * 75)

if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 2 else "SpellCaster (USA, Europe).sms"
    termo = sys.argv[2] if len(sys.argv) > 2 else (sys.argv[1] if len(sys.argv) == 2 else "PASSWORD")
    busca_relativa(arquivo, termo)