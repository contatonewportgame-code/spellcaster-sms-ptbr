import os
import sys

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: RASTREADOR DE TILEMAP & JANELAS 2D (V2.0)
# AUTOR E ENGENHEIRO-CHEFE: CRISTIANO MARIANO - NEWPORTGAME
# UPGRADE V2.0: BUSCA DE MOLDURAS 2D, WILDCARDS (?) E CORRELAÇÃO DE VRAM
# =============================================================================

def rastrear_tilemap_avancado(rom_path, padrao_hex_lista, largura_linha=26):
    if not os.path.exists(rom_path):
        print(f"Erro: Arquivo '{rom_path}' não encontrado!")
        return

    with open(rom_path, "rb") as f:
        rom = f.read()

    print("=" * 78)
    print(f"📍 SMS VRAM TILEMAP TRACER V2.0 - ROM: {os.path.basename(rom_path)}")
    print(f"Modo: Varredura com Suporte a Células de 2 Bytes e Padrões de Janela")
    print("=" * 78)

    # Converte padrão permitindo wildcards (-1 representa qualquer byte)
    padrao_bytes = []
    for item in padrao_hex_lista:
        if item in ("??", "?", None):
            padrao_bytes.append(-1)
        else:
            padrao_bytes.append(int(item, 16))

    tam_padrao = len(padrao_bytes)
    encontrados = 0

    for i in range(len(rom) - tam_padrao):
        match = True
        for k in range(tam_padrao):
            if padrao_bytes[k] != -1 and rom[i + k] != padrao_bytes[k]:
                match = False
                break
        
        if match:
            banco = i // 0x4000
            offset_banco = i % 0x4000
            z80_slot2 = 0x8000 + offset_banco
            print(f"🎯 PADRÃO LOCALIZADO na ROM: 0x{i:05X} (Banco {banco:02d})")
            print(f"   Offset no Banco: 0x{offset_banco:04X} | Z80 Slot 2: ${z80_slot2:04X}")
            
            # Mostra contexto da linha inteira (largura_linha bytes)
            inicio_linha = (i // 2) * 2
            contexto = rom[inicio_linha : inicio_linha + largura_linha].hex(' ').upper()
            print(f"   Contexto da Linha (26B): [{contexto}]")
            print("-" * 78)
            encontrados += 1

    if encontrados == 0:
        print("[-] Nenhum padrão correspondente localizado na ROM.")
    else:
        print(f"Total de ocorrências localizadas: {encontrados}")
    print("=" * 78)

if __name__ == "__main__":
    rom = sys.argv[1] if len(sys.argv) > 1 else "SpellCaster (USA, Europe).sms"
    # Exemplo: Procura moldura da Caixa de Armas (Canto 00:09, depois 4 tiles de letras, depois 00:09)
    # [00 09 ?? ?? ?? ?? ?? ?? ?? ?? 00 09]
    padrao_teste = ["00", "09", "??", "??", "??", "??", "??", "??", "??", "??", "00", "09"]
    rastrear_tilemap_avancado(rom, padrao_teste)