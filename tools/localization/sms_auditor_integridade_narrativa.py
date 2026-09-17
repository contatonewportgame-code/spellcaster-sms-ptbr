import os
import re

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: AUDITOR DE INTEGRIDADE NARRATIVA (OFICIAL)
# AUTOR: CRISTIANO MARIANO - NEWPORTGAME
# COMPARA A ROM ORIGINAL DA SEGA CONTRA A TRADUÇÃO CAÇANDO TELAS DELETADAS
# =============================================================================

ROM_ORIGINAL_SEGA = "SpellCaster (USA, Europe).sms"
ARQUIVO_MESTRE = "tradutor_mestre_v10.py"
OFFSET_A = 0x21

def decodificar_rom_original(rom_bytes, pos_inicial):
    texto = ""
    telas = 1
    pos = pos_inicial
    while pos < len(rom_bytes):
        b1 = rom_bytes[pos]
        if b1 == 0xFC and pos + 1 < len(rom_bytes) and rom_bytes[pos + 1] == 0xFF:
            pos += 2
            break
        if b1 == 0xFC:
            texto += "<FC>"
            telas += 1
            pos += 1
            continue
        if b1 == 0xFD:
            texto += "[PULA]"
            pos += 1
            continue
        if b1 == 0x0E:
            texto += "<0E>"
            pos += 1
            continue
        if b1 in (0x02, 0x1A, 0x0C, 0x01, 0x1F, 0x07):
            pos += 1
            continue
        if b1 == 0x00:
            texto += " "
        elif b1 == 0x37:
            texto += "."
        elif OFFSET_A <= b1 <= 0x3A:
            texto += chr(b1 - OFFSET_A + ord('A'))
        pos += 1
    return texto.strip(), telas, (pos - pos_inicial)

def auditar_integridade_total():
    if not os.path.exists(ROM_ORIGINAL_SEGA) or not os.path.exists(ARQUIVO_MESTRE):
        print("Erro: Arquivos base não encontrados!")
        return

    with open(ROM_ORIGINAL_SEGA, "rb") as f: rom_orig = f.read()
    with open(ARQUIVO_MESTRE, "r", encoding="utf-8") as f: mestre_codigo = f.read()

    print("=" * 78)
    print("🔬 AUDITORIA FORENSE DE INTEGRIDADE NARRATIVA (ROM SEGA x TRADUÇÃO)")
    print("=" * 78)

    # 1. Banco 12 (Oásis)
    print("\n📍 1. Auditando Banco 12 (Oásis de Diálogos e NPCs)...")
    print("-" * 78)
    alertas_b12 = 0
    padrao_oas = re.compile(r'(\d+):\s*[\'"](.*?)[\'"],?')
    bloco_oasis = mestre_codigo.split("OASIS_260_FRASES = {")[1].split("MENUS_BANCO19 = {")[0]
    frases_oasis = padrao_oas.findall(bloco_oasis)
    dict_pt = {int(k): v for k, v in frases_oasis}

    for id_frase in range(83):
        ptr_addr = 0x30000 + (id_frase * 2)
        ptr = rom_orig[ptr_addr] | (rom_orig[ptr_addr + 1] << 8)
        addr_orig = (ptr - 0x8000) + 0x30000

        txt_orig, telas_orig, bytes_orig = decodificar_rom_original(rom_orig, addr_orig)
        txt_pt = dict_pt.get(id_frase, "")
        telas_pt = txt_pt.count("<FC>") + 1

        if bytes_orig < 15 or not txt_orig: continue

        razao = len(txt_pt) / max(1, len(txt_orig))
        if telas_pt < telas_orig or (razao < 0.65 and len(txt_orig) > 30):
            print(f"🚨 ALERTA NO BANCO 12 (Frase ID {id_frase}):")
            print(f"   [Original Sega ({telas_orig} Telas)]: \"{txt_orig}\"")
            print(f"   [Português Atual ({telas_pt} Telas)]: \"{txt_pt}\"")
            print("-" * 78)
            alertas_b12 += 1

    # 2. Bancos 30 e 31 (História)
    print("\n📍 2. Auditando Bancos 30 e 31 (História Principal)...")
    print("-" * 78)
    alertas_hist = 0
    padrao_hist = re.compile(r'(\d+):\s*\(\s*(\d+)\s*,\s*[\'"](.*?)[\'"]\s*\)')
    frases_hist = padrao_hist.findall(mestre_codigo)

    for offset_str, max_sz_str, txt_pt in frases_hist:
        offset = int(offset_str)
        banco = offset // 0x4000
        txt_orig, telas_orig, bytes_orig = decodificar_rom_original(rom_orig, offset)
        telas_pt = txt_pt.count("<FC>") + 1

        if not txt_orig or len(txt_orig) < 15: continue

        razao = len(txt_pt) / max(1, len(txt_orig))
        if telas_pt < telas_orig or (razao < 0.65 and len(txt_orig) > 40):
            alertas_hist += 1

    print(f"[*] Total de telas/diálogos em análise: {alertas_b12 + alertas_hist}")
    if alertas_b12 == 0:
        print("🎉 BANCO 12 100% LIMPO E RESTAURADO! ZERO TELAS PERDIDAS!")
    print("=" * 78)

if __name__ == "__main__":
    auditar_integridade_total()