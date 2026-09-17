import os
import sys

# =============================================================================
# SUÍTE FORENSE SEGA MASTER SYSTEM: CODEC & PATCHER PLANAR RLE (4BPP)
# AUTOR: CRISTIANO MARIANO - NEWPORTGAME
# BASEADO NO CAPÍTULO 4 DO COMPÊNDIO MASTER SYSTEM
# =============================================================================

def descompactar_plano(rom_bytes, pos):
    """Descompacta um único plano de cor Sega RLE."""
    dados = bytearray()
    n = len(rom_bytes)
    while pos < n:
        ctrl = rom_bytes[pos]; pos += 1
        if ctrl == 0x00: break  # Terminador Sega
        if ctrl < 0x80:
            if pos >= n: return None, pos
            val = rom_bytes[pos]; pos += 1
            dados.extend([val] * ctrl)
        else:
            qtd = ctrl & 0x7F
            if pos + qtd > n: return None, pos
            dados.extend(rom_bytes[pos : pos + qtd]); pos += qtd
        if len(dados) > 0x4000: # Limite de 1 banco (16 KB)
            return None, pos
    return dados, pos

def descompactar_bloco_4bpp(rom_bytes, offset_inicial):
    """Descompacta os 4 planos simétricos da Sega a partir de um offset."""
    pos = offset_inicial
    planos = []
    for _ in range(4):
        plano, pos = descompactar_plano(rom_bytes, pos)
        if plano is None or len(plano) == 0:
            return None, 0
        planos.append(bytearray(plano))
    
    # Validação estrita de simetria Sega
    t0 = len(planos[0])
    if t0 != len(planos[1]) or t0 != len(planos[2]) or t0 != len(planos[3]) or t0 % 8 != 0:
        return None, 0

    tam_comprimido = pos - offset_inicial
    return planos, tam_comprimido

def compactar_plano(dados):
    """Comprime dados brutos para o formato Sega Planar RLE."""
    out = bytearray()
    i = 0
    n = len(dados)
    while i < n:
        run_len = 1
        while i + run_len < n and dados[i + run_len] == dados[i] and run_len < 127:
            run_len += 1
        if run_len >= 2:
            out.append(run_len)
            out.append(dados[i])
            i += run_len
        else:
            lit = []
            while i < n and len(lit) < 127:
                if i + 2 < n and dados[i] == dados[i+1] == dados[i+2]:
                    break
                lit.append(dados[i])
                i += 1
            out.append(0x80 | len(lit))
            out.extend(lit)
    out.append(0x00) # Terminador obrigatório Sega
    return bytes(out)

def compactar_bloco_4bpp(planos):
    """Comprime os 4 planos na sequência canônica da Sega."""
    saida = bytearray()
    for p in range(4):
        saida.extend(compactar_plano(planos[p]))
    return bytes(saida)

def aplicar_patch_rle_tile(rom_path, offset_bloco, dicionario_tiles_1bpp, rom_saida=None):
    """
    Descompacta o bloco, injeta matrizes 1bpp em tiles específicos, 
    recomprime e valida a Regra da Folga Positiva.
    """
    if not os.path.exists(rom_path):
        print(f"Erro: '{rom_path}' não encontrada!")
        return False

    with open(rom_path, "rb") as f:
        rom = bytearray(f.read())

    print("=" * 75)
    print(f"🔬 CIRURGIA PLANAR RLE IN-PLACE - ROM: {os.path.basename(rom_path)}")
    print(f"   Offset Inicial do Bloco: 0x{offset_bloco:05X}")
    print("=" * 75)

    planos, tam_orig = descompactar_bloco_4bpp(rom, offset_bloco)
    if planos is None:
        print("[!] Erro: Offset não contém um bloco Planar RLE válido da Sega.")
        return False

    total_tiles = len(planos[0]) // 8
    print(f"[✓] Bloco descompactado com sucesso! {total_tiles} tiles de 8x8 recuperados.")
    print(f"[✓] Tamanho comprimido original: {tam_orig} bytes.")

    # Injeção das matrizes nos tiles selecionados
    for tile_id, matriz_8b in dicionario_tiles_1bpp.items():
        if tile_id >= total_tiles:
            print(f"[!] Erro: Tile {tile_id} fora do bloco (máximo {total_tiles-1})!")
            return False
        for r in range(8):
            idx = tile_id * 8 + r
            planos[0][idx] = matriz_8b[r] # Plano 0 (Branco)
            planos[1][idx] = 0x00         # Zera outros planos
            planos[2][idx] = 0x00
            planos[3][idx] = 0x00
        print(f"   ➔ Tile {tile_id:3d} (0x{tile_id:02X}) injetado com sucesso!")

    # Recompressão
    bloco_novo = compactar_bloco_4bpp(planos)
    tam_novo = len(bloco_novo)
    print(f"[*] Novo tamanho comprimido: {tam_novo} bytes")

    if tam_novo > tam_orig:
        print(f"[!] ERRO: Estouro de bloco! Ficou {tam_novo - tam_orig} bytes maior.")
        return False

    folga = tam_orig - tam_novo
    bloco_final = bloco_novo + (b'\x00' * folga) # Regra da Folga Positiva
    rom[offset_bloco : offset_bloco + len(bloco_final)] = bloco_final
    print(f"🎉 SUCESSO! Bloco recompactado com {folga} bytes de folga segura!")

    arquivo_final = rom_saida if rom_saida else rom_path
    with open(arquivo_final, "wb") as f:
        f.write(rom)
    print(f"[✓] ROM gravada com sucesso: '{arquivo_final}'")
    print("=" * 75)
    return True

if __name__ == "__main__":
    print("Módulo Planar RLE Sega carregado com sucesso.")
    print("Uso: importar funções ou chamar aplicar_patch_rle_tile().")