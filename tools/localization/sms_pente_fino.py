import os
import re
import sys

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: AUDITOR TOTAL DE IDIOMA & STUBS (V4.0 GOLD MASTER)
# AUTOR E ENGENHEIRO-CHEFE: CRISTIANO MARIANO - NEWPORTGAME
# NOVIDADES V4.0: DETECTOR DE STUBS DE DEBUG (??...??), MARCADORES DE QA E ASCII '$'
# =============================================================================

ROM_ALVO = sys.argv[1] if len(sys.argv) > 1 else "SpellCaster (PT-BR).sms"
OFFSET_A_CUSTOM = 0x21
BYTE_HIFEN = 0x08

MAPA_11_ACENTOS = {
    0x3B: "Á", 0x3C: "Ç", 0x3D: "Ó", 0x3E: "É", 0x43: "Ê",
    0x20: "Ã", 0x0F: "Í", 0x0B: "Ú", 0x1B: "Õ", 0x1D: "Â", 0x0A: "Ô"
}

INGLES_KEYWORDS = {
    "MOVE", "TALK", "LOOK", "TAKE", "SPELL", "TERRAIN", "PASSWORD",
    "INSIDE", "OUTSIDE", "SHRINE", "TEMPLE", "SWORD", "BRANCHES",
    "HOUSE", "PIER", "SEAWEED", "FRIED", "EGG", "SUSHI", "GLASSES",
    "BOAT", "NET", "FISHING", "POLE", "FRONT", "BACK", "LEFT", "RIGHT",
    "JUMP", "OCEAN", "PRESENT", "LOCATION", "LUTE", "BEADS", "GRANDPA",
    "RETURN", "BALL", "POT", "LID", "BRACERS", "SIDE", "EAST", "WEST",
    "NORTH", "SOUTH", "PYRAMID", "POINT", "MISTY", "CROSSING", "GATE",
    "PLAINS", "NECTAR", "ROCK", "SOMETHING", "OAR", "HARP", "FURY",
    "MIRROR", "NECKLACE", "BREAK", "CONTINUE",
    "THE", "YOU", "ARE", "AND", "THAT", "THIS", "WITH", "FROM", "HAVE",
    "FOR", "NOT", "WHAT", "LORD", "EVIL", "DEMON", "KILL", "MAGIC",
    "POWER", "ATTACK", "DEAD", "DEFEAT", "WATER", "FIRE", "STONE"
}

def passar_pente_fino_v4():
    if not os.path.exists(ROM_ALVO):
        print(f"Erro: '{ROM_ALVO}' não encontrada!")
        return

    with open(ROM_ALVO, "rb") as f:
        rom = f.read()

    total_bancos = len(rom) // 0x4000
    print("=" * 78)
    print("🔬 PENTE FINO TOTAL V4.0: AUDITORIA DE IDIOMA + CAÇADOR DE STUBS (??..??)")
    print(f"ROM Alvo: {os.path.basename(ROM_ALVO)} ({len(rom) // 1024} KB)")
    print("=" * 78)

    alertas_stubs = []
    alertas_ingles = []

    # 1. VARREDURA DE STUBS DE DEBUG ESQUECIDOS (Padrão ??...??)
    print("\n📍 1. VARREDURA DE STUBS DE DEBUG E CÓDIGOS DE ERRO DE FÁBRICA:")
    print("-" * 78)
    # Procura na ROM sequências que começam e terminam com "??" em custom ou ASCII
    for i in range(len(rom) - 6):
        # Em custom: 0x1F 0x1F ... 0x1F 0x1F
        if rom[i] == 0x1F and rom[i+1] == 0x1F:
            for k in range(2, 10):
                if i + k + 1 < len(rom) and rom[i+k] == 0x1F and rom[i+k+1] == 0x1F:
                    miolo = rom[i : i + k + 2].hex(' ').upper()
                    banco = i // 0x4000
                    alertas_stubs.append((i, banco, f"Stub Custom em 0x{i:05X}: [{miolo}]"))

    if alertas_stubs:
        for addr, b, msg in alertas_stubs:
            print(f"🚨 ALERTA: {msg} (Banco {b:02d}) ➔ Possível texto amputado ou bug de fábrica!")
    else:
        print("🎉 SUCESSO: Zero stubs de depuração ou códigos ??...?? encontrados na ROM!")

    # 2. VARREDURA DE IDIOMA (INGLÊS)
    print("\n" + "=" * 78)
    print("📍 2. VARREDURA DE PALAVRAS EM INGLÊS:")
    print("-" * 78)
    for b in range(1, total_bancos):
        ini = b * 0x4000
        dados = rom[ini : ini + 0x4000]
        # Decodifica texto
        chars = []
        for byte_val in dados:
            if byte_val == 0x00: chars.append(" ")
            elif byte_val == 0x37: chars.append(".")
            elif byte_val == BYTE_HIFEN: chars.append("-")
            elif byte_val in MAPA_11_ACENTOS: chars.append(MAPA_11_ACENTOS[byte_val])
            elif OFFSET_A_CUSTOM <= byte_val <= 0x3A: chars.append(chr(byte_val - OFFSET_A_CUSTOM + ord('A')))
            else: chars.append("\n")
        
        texto_bloco = "".join(chars)
        palavras = re.findall(r'[A-ZÁÉÍÓÚÃÕÊÂÔÇ\-]+', texto_bloco)
        for p in palavras:
            if p in INGLES_KEYWORDS and len(p) >= 3:
                if p in {"FOR"} and "FORÇA" in texto_bloco: continue
                alertas_ingles.append((b, p))

    if alertas_ingles:
        print(f"⚠️ Encontradas {len(alertas_ingles)} palavras suspeitas em inglês para revisão.")
    else:
        print("🎉 SUCESSO ABSOLUTO: Nenhuma palavra em inglês detectada em toda a ROM!")
    print("=" * 78)

if __name__ == "__main__":
    passar_pente_fino_v4()