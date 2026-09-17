import os
import re

# =============================================================================
# SUÍTE FORENSE NEWPORTGAME: AUDITOR DE BORDAS & RETRATO (OFICIAL)
# AUTOR: CRISTIANO MARIANO - NEWPORTGAME
# AUDITA O COMPILADOR CAÇANDO LINHAS QUE EXCEDEM O TETO DE 17 COLUNAS DO KANE
# =============================================================================

ARQUIVO_MESTRE = "tradutor_mestre_v10.py"
LIMITE_COLUNAS_RETRATO = 17

def limpar_tags(linha):
    limpo = re.sub(r'<[0-9A-Fa-f]{2}>', '', linha)
    limpo = limpo.replace('[PULA]', '').replace('<FC>', '').replace('<1A>', '')
    return limpo

def auditar_compilador():
    if not os.path.exists(ARQUIVO_MESTRE):
        print(f"Erro: '{ARQUIVO_MESTRE}' não encontrado!")
        return

    with open(ARQUIVO_MESTRE, "r", encoding="utf-8") as f:
        conteudo = f.read()

    padrao = re.compile(r'(\d+):\s*\(\s*(\d+)\s*,\s*[\'"](.*?)[\'"]\s*\)')
    frases = padrao.findall(conteudo)

    print("=" * 78)
    print(f"🔍 SMS AUDITOR DE BORDAS: CAÇA DE VAZAMENTO DE TEXTO (> {LIMITE_COLUNAS_RETRATO} COLUNAS)")
    print("=" * 78)

    alertas = 0
    for offset_str, tam_max_str, texto in frases:
        offset = int(offset_str)
        linhas = texto.split('[PULA]')
        
        for idx, lin in enumerate(linhas, 1):
            sublinhas = lin.split('<FC>')
            for sub in sublinhas:
                texto_visivel = limpar_tags(sub)
                tamanho_real = len(texto_visivel)
                if tamanho_real > LIMITE_COLUNAS_RETRATO:
                    banco = offset // 0x4000
                    print(f"⚠️ Offset: {offset} (Banco {banco:02d}) | Linha {idx}: {tamanho_real} colunas!")
                    print(f"   Texto: \"{texto_visivel}\"")
                    print(f"   Original: \"{texto}\"")
                    print("-" * 78)
                    alertas += 1

    print("=" * 78)
    if alertas == 0:
        print("🎉 SUCESSO SUPREMO! 0 linhas ultrapassam 17 colunas! Borda 100% blindada.")
    else:
        print(f"🚨 Encontradas {alertas} linhas que podem invadir a moldura do Kane!")
    print("=" * 78)

if __name__ == "__main__":
    auditar_compilador()