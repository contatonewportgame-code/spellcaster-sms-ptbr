import os
import sys

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: CAÇADOR DE LOADERS VRAM Z80 (V1.0 OFICIAL)
# AUTOR E ENGENHEIRO-CHEFE: CRISTIANO MARIANO - NEWPORTGAME
# FERRAMENTA #21 DO PLAYBOOK: LOCALIZA ORIGEM EXATA DE TILES NA PLACA DE VÍDEO
# EXTERMINA O 'EFEITO DO SÍMBOLO FANTASMA' (CAPÍTULO 8.2 DO COMPÊNDIO)
# =============================================================================

def escanear_loaders_vram(rom_path):
    if not os.path.exists(rom_path):
        print(f"Erro: '{rom_path}' não encontrada!")
        return

    with open(rom_path, "rb") as f:
        rom = f.read()

    print("=" * 78)
    print("🔬 SMS VDP LOADER HUNTER V1.0: RASTREAMENTO DE CARGA DE VRAM NO Z80")
    print(f"ROM Alvo: {os.path.basename(rom_path)} ({len(rom) // 1024} KB)")
    print("=" * 78)

    achados = 0

    # Varre a ROM caçando comandos Z80 que preparam escrita na VRAM (Bits 14-15 = %01)
    # No Master System: LD DE, $4xxx..$7xxx seguido de chamada de escrita ou OUT ($BF)
    for i in range(len(rom) - 16):
        # Padrão típico Sega:
        # LD HL, $xxxx (Origem) ➔ 21 xx xx
        # LD DE, $6xxx (Destino VRAM write) ➔ 11 xx 6x
        # LD BC, $xxxx (Tamanho em bytes) ➔ 01 xx xx
        if rom[i] == 0x21 and rom[i+3] == 0x11 and (rom[i+5] & 0xC0) == 0x40:
            origem_z80 = rom[i+1] | (rom[i+2] << 8)
            vram_dest = (rom[i+4] | (rom[i+5] << 8)) & 0x3FFF
            
            # Checa se o próximo é LD BC (tamanho)
            if rom[i+6] == 0x01:
                tam_bytes = rom[i+7] | (rom[i+8] << 8)
                banco_rom = i // 0x4000
                tiles_qtd = tam_bytes // 8  # Se for 1bpp
                
                # Checa chaveamento bancário imediatamente anterior (até 12 bytes antes)
                banco_slot2 = "Slot 2 Atual"
                for rec in range(max(0, i - 12), i):
                    if rom[rec] == 0x3E and rom[rec+2] == 0x32 and rom[rec+3] == 0xFF and rom[rec+4] == 0xFF:
                        banco_slot2 = f"Banco {rom[rec+1]:02X}h ({rom[rec+1] & 0x3F} dec)"
                        break

                print(f"🎯 Offset ROM: 0x{i:05X} (Banco {banco_rom:02d}) ➔ CARGA DE VRAM DETECTADA!")
                print(f"   Origem Z80:   ${origem_z80:04X} | Mapeamento: {banco_slot2}")
                print(f"   Destino VRAM: ${vram_dest:04X} (Tile {vram_dest // 32:3d} se 4bpp / Tile {vram_dest // 8:3d} se 1bpp)")
                print(f"   Tamanho:      {tam_bytes:3d} bytes (~{tiles_qtd} tiles de 1bpp / ~{tam_bytes // 32} tiles 4bpp)")
                print(f"   ⚠️ LIMITE:    Qualquer edição além de {tam_bytes} bytes NÃO chegará na VRAM!")
                print("-" * 78)
                achados += 1

    print("=" * 78)
    print(f"Total de rotinas de carga para a VRAM localizadas: {achados}")
    print("=" * 78)

if __name__ == "__main__":
    arquivo = sys.argv[1] if len(sys.argv) > 1 else "SpellCaster (USA, Europe).sms"
    escanear_loaders_vram(arquivo)