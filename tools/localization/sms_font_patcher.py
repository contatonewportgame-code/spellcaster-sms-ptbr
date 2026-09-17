import os
import sys

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: ESTÚDIO TIPOGRÁFICO DE FONTES SMS (V4.0)
# AUTOR E ENGENHEIRO-CHEFE: CRISTIANO MARIANO - NEWPORTGAME
# NOVIDADES V4.0: SUPORTE A 8x16 (TOPO+BASE) E SIMULADOR DE KERNING (RESPIRO)
# =============================================================================

# Matrizes 8x16 do HUD e Caixas (Topo + Base)
FONTES_8x16_BANCO05 = {
    "A (VIDA/ATAQ)": {
        "topo": bytes.fromhex("00183C6666C3C3FF"),
        "base": bytes.fromhex("FFC3C3C3C3C3C300")
    },
    "T (ATAQ - 1E/1F)": {
        "topo": bytes.fromhex("007E7E1818181818"),
        "base": bytes.fromhex("1818181818180000")
    },
    "Q (ATAQ - 20/21 com respiro)": {
        "topo": bytes.fromhex("003C7E6666666666"),
        "base": bytes.fromhex("6666666E7E3F0F00")
    },
    "D (DEFS/VIDA - 1C)": {
        "topo": bytes.fromhex("00FCFEC6C6C6C6C6"),
        "base": bytes.fromhex("C6C6C6C6C6FEFC00")
    },
    "S (DEFS - 22/23 Sega)": {
        "topo": bytes.fromhex("007CFEC6C6C6E070"),
        "base": bytes.fromhex("1C0EC6C6C6FE7C00")
    }
}

def render_8x16_terminal(dicionario_letras):
    print("\n📺 ESTÚDIO TIPOGRÁFICO 8x16 (ARRANGEMENT VRAM NATIVO):")
    print("=" * 78)
    
    for nome, dados in dicionario_letras.items():
        topo = dados["topo"]
        base = dados["base"]
        print(f"\n🔤 Letra: {nome}")
        print("   " + "-" * 20)
        # 8 linhas do topo
        for r in range(8):
            linha = "".join("██" if (topo[r] >> (7 - c)) & 1 else ".." for c in range(8))
            print(f"   {linha} | Linha {r:02d} (Topo)")
        # Linha divisória de células
        print("   " + "==" * 8 + " [Emenda 8x16]")
        # 8 linhas da base
        for r in range(8):
            linha = "".join("██" if (base[r] >> (7 - c)) & 1 else ".." for c in range(8))
            print(f"   {linha} | Linha {r:02d} (Base)")

def simular_palavra_8x16(palavra_letras, espaco_entre_letras=0):
    print("\n" + "=" * 78)
    print("🔬 SIMULADOR DE KERNING & ESPAÇAMENTO HORIZONTAL NO TERMINAL:")
    print("=" * 78)
    
    # 8 linhas de topo
    for r in range(8):
        linha_str = ""
        for dados in palavra_letras:
            t = dados["topo"]
            linha_str += "".join("██" if (t[r] >> (7 - c)) & 1 else "  " for c in range(8))
            linha_str += "  " * espaco_entre_letras
        print(f"   {linha_str}")
        
    # 8 linhas de base
    for r in range(8):
        linha_str = ""
        for dados in palavra_letras:
            b = dados["base"]
            linha_str += "".join("██" if (b[r] >> (7 - c)) & 1 else "  " for c in range(8))
            linha_str += "  " * espaco_entre_letras
        print(f"   {linha_str}")
    print("=" * 78)

if __name__ == "__main__":
    print("=" * 78)
    print("🎨 SMS FONT PATCHER V4.0: ESTÚDIO DE FONTES & SIMULADOR DE KERNING")
    print("=" * 78)
    render_8x16_terminal(FONTES_8x16_BANCO05)
    
    # Simula a palavra ATAQ montada
    palavra_ataq = [
        FONTES_8x16_BANCO05["A (VIDA/ATAQ)"],
        FONTES_8x16_BANCO05["T (ATAQ - 1E/1F)"],
        FONTES_8x16_BANCO05["A (VIDA/ATAQ)"],
        FONTES_8x16_BANCO05["Q (ATAQ - 20/21 com respiro)"]
    ]
    print("\n👉 Visualização Montada de 'ATAQ' (com respiro de 1 pixel no Q):")
    simular_palavra_8x16(palavra_ataq)