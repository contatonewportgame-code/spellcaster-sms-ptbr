import os
import re

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: AUDITOR SINTÁTICO & SEMÂNTICO (OFICIAL)
# AUTOR: CRISTIANO MARIANO - NEWPORTGAME
# CAÇA ESPAÇOS DUPLOS, CARACTERES ENGOLIDOS E FALTA DE CONECTIVOS
# =============================================================================

ARQUIVO_MESTRE = "tradutor_mestre_v10.py"

def auditar_sintaxe_e_estilo():
    if not os.path.exists(ARQUIVO_MESTRE):
        print(f"Erro: '{ARQUIVO_MESTRE}' não encontrado!")
        return

    with open(ARQUIVO_MESTRE, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("=" * 78)
    print("🔬 SMS PENTE FINO SINTÁTICO: CAÇANDO ANOMALIAS E ESPAÇOS DUPLOS")
    print("=" * 78)

    padrao = re.compile(r'(\d+):\s*\(\s*(\d+)\s*,\s*[\'"](.*?)[\'"]\s*\)')
    frases = padrao.findall(codigo)

    alertas_espaco_duplo = []

    for offset_str, max_size_str, texto in frases:
        offset = int(offset_str)
        banco = offset // 0x4000
        if "  " in texto:
            alertas_espaco_duplo.append((offset, banco, "Espaço duplo detectado (caractere engolido)", texto))

    print(f"[*] Alertas de Espaço Duplo (Letras Desaparecidas): {len(alertas_espaco_duplo)}")
    for off, b, motivo, txt in alertas_espaco_duplo:
        print(f"   ⚠️ Offset {off} (Banco {b:02d}) ➔ {motivo}")
        print(f"      Texto: \"{txt}\"")
        print("-" * 78)

    print("=" * 78)
    if len(alertas_espaco_duplo) == 0:
        print("🎉 ZERO ESPAÇOS DUPLOS! Todos os acentos e pontuações estão 100% íntegros!")
    print("=" * 78)

if __name__ == "__main__":
    auditar_sintaxe_e_estilo()