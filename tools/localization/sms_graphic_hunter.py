import os
import sys
import json

ROM_ALVO = sys.argv[1] if len(sys.argv) > 1 else "SpellCaster (PT-BR).sms"

# =============================================================================
# MOTOR DE DESCOMPRESSÃO PLANAR RLE (SEGA 4BPP)
# =============================================================================
def descompactar_plano(rom_bytes, pos):
    dados = bytearray()
    n = len(rom_bytes)
    while pos < n:
        ctrl = rom_bytes[pos]
        pos += 1
        if ctrl == 0x00: # Fim do plano Sega
            break
        if ctrl < 0x80:
            if pos >= n: return None, pos
            val = rom_bytes[pos]
            pos += 1
            dados.extend([val] * ctrl)
        else:
            qtd = ctrl & 0x7F
            if pos + qtd > n: return None, pos
            dados.extend(rom_bytes[pos : pos + qtd])
            pos += qtd
        if len(dados) > 0x4000: # Limite de segurança de 1 banco
            return None, pos
    return dados, pos

def tentar_descompactar_bloco_4bpp(rom_bytes, offset_inicial):
    pos = offset_inicial
    planos = []
    for _ in range(4):
        plano, pos = descompactar_plano(rom_bytes, pos)
        if plano is None or len(plano) == 0:
            return None, 0
        planos.append(plano)
    
    # Validações estritas de simetria gráfica Sega
    t0 = len(planos[0])
    if t0 != len(planos[1]) or t0 != len(planos[2]) or t0 != len(planos[3]):
        return None, 0
    if t0 % 8 != 0 or t0 < 64: # Mínimo de 8 tiles de 8x8
        return None, 0
    
    tam_comprimido = pos - offset_inicial
    if tam_comprimido < 16:
        return None, 0

    return planos, tam_comprimido

def decodificar_tiles_para_pixels(planos):
    """Converte os 4 planos em uma matriz de índices de cores (0 a 15)."""
    total_tiles = len(planos[0]) // 8
    tiles_pixels = [] # Lista de listas com 64 pixels (8x8) cada

    for t in range(total_tiles):
        tile_px = []
        for lin in range(8):
            idx = t * 8 + lin
            p0 = planos[0][idx]
            p1 = planos[1][idx]
            p2 = planos[2][idx]
            p3 = planos[3][idx]
            for bit in range(7, -1, -1):
                c = (((p3 >> bit) & 1) << 3) | (((p2 >> bit) & 1) << 2) | (((p1 >> bit) & 1) << 1) | ((p0 >> bit) & 1)
                tile_px.append(c)
        tiles_pixels.append(tile_px)
    return tiles_pixels

def calcular_pontuacao_texto(tile_px):
    """Calcula se o tile parece conter letras/ideogramas (alta densidade de bordas)."""
    transicoes = 0
    cores_distintas = set(tile_px)
    if len(cores_distintas) < 2:
        return 0 # Tile sólido ou vazio
    
    for r in range(8):
        for c in range(7):
            if tile_px[r * 8 + c] != tile_px[r * 8 + c + 1]:
                transicoes += 1
    for c in range(8):
        for r in range(7):
            if tile_px[r * 8 + c] != tile_px[(r + 1) * 8 + c]:
                transicoes += 1

    # Textos e kanjis costumam ter entre 18 e 45 transições por bloco 8x8
    return transicoes

# =============================================================================
# VARREDOR GERAL E GERADOR DE GALERIA VISUAL
# =============================================================================
def escanear_e_gerar_galeria():
    if not os.path.exists(ROM_ALVO):
        print(f"Erro: Arquivo '{ROM_ALVO}' não encontrado!")
        return

    with open(ROM_ALVO, "rb") as f:
        rom = f.read()

    print("=" * 78)
    print(f"🔬 SEGA MASTER SYSTEM: CAÇADOR DE GRÁFICOS & PLACAS JAPONESAS")
    print(f"ROM Alvo: {ROM_ALVO} ({len(rom) // 1024} KB)")
    print("Varrendo todos os 32 bancos caçando blocos gráficos Planar RLE da Sega...")
    print("=" * 78)

    blocos_encontrados = []
    pos = 0x4000 # Inicia após o Banco 0 (gráficos ficam nos bancos 1 a 31)
    tam_rom = len(rom)

    while pos < tam_rom - 32:
        planos, tam_comp = tentar_descompactar_bloco_4bpp(rom, pos)
        if planos is not None:
            total_tiles = len(planos[0]) // 8
            banco = pos // 0x4000
            offset_banco = pos % 0x4000
            tiles_px = decodificar_tiles_para_pixels(planos)

            # Heurística: checa quantos tiles têm pontuação de ideograma
            tiles_com_texto = []
            for t_idx, t_px in enumerate(tiles_px):
                score = calcular_pontuacao_texto(t_px)
                if score >= 22:
                    tiles_com_texto.append(t_idx)

            tem_placa_suspeita = len(tiles_com_texto) >= 4

            blocos_encontrados.append({
                "offset": pos,
                "banco": banco,
                "offset_banco": offset_banco,
                "tam_comp": tam_comp,
                "total_tiles": total_tiles,
                "tem_placa": tem_placa_suspeita,
                "tiles_texto": tiles_com_texto,
                "tiles_px": tiles_px
            })

            status = "⚠️ POSSÍVEL PLACA/LETRA DETECTADA!" if tem_placa_suspeita else "Cenário/Textura"
            print(f"🎯 0x{pos:05X} (Banco {banco:02d}) | {total_tiles:3d} tiles ({tam_comp:4d}b comp) | {status}")
            
            # Pula o bloco descompactado para acelerar
            pos += tam_comp
        else:
            pos += 1

    print("=" * 78)
    print(f"Total de blocos gráficos de cenário identificados: {len(blocos_encontrados)}")
    print("Gerando Galeria Visual Interativa em HTML...")

    # Gera o arquivo HTML com visualizador Canvas
    html_filename = "galeria_graficos_sms.html"
    
    # Paleta Master System de alto contraste (para revelar qualquer traço escuro em fundo claro)
    paleta_hex = [
        "#000000", "#FFFFFF", "#E02020", "#20E020", 
        "#2040E0", "#E0E020", "#E08020", "#20E0E0",
        "#E020E0", "#808080", "#C0C0C0", "#600000", 
        "#006000", "#000060", "#606000", "#E8D8B8"
    ]

    # Prepara JSON leve dos blocos para o HTML
    blocos_json = []
    for b in blocos_encontrados:
        blocos_json.append({
            "offset": f"0x{b['offset']:05X}",
            "banco": b["banco"],
            "total_tiles": b["total_tiles"],
            "tem_placa": b["tem_placa"],
            "tiles_texto": b["tiles_texto"],
            "pixels": b["tiles_px"]
        })

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Galeria Visual de Gráficos - SpellCaster (SMS)</title>
    <style>
        body {{ background: #121216; color: #E0E0E0; font-family: 'Segoe UI', Tahoma, sans-serif; padding: 20px; }}
        h1 {{ color: #FFCC00; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .toolbar {{ background: #1A1A22; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        button {{ background: #FFCC00; color: #000; border: none; padding: 8px 16px; font-weight: bold; border-radius: 4px; cursor: pointer; margin-right: 10px; }}
        button:hover {{ background: #FFE066; }}
        .card {{ background: #1A1A22; border: 1px solid #2C2C38; border-radius: 8px; padding: 15px; margin-bottom: 25px; }}
        .card.alerta {{ border: 2px solid #FF3344; box-shadow: 0 0 10px rgba(255, 51, 68, 0.3); }}
        .tag-alerta {{ background: #FF3344; color: #FFF; font-size: 11px; padding: 3px 8px; border-radius: 3px; font-weight: bold; margin-left: 10px; }}
        .tile-container {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 15px; background: #0A0A0E; padding: 10px; border-radius: 6px; }}
        canvas {{ image-rendering: pixelated; width: 24px; height: 24px; border: 1px solid #222; }}
        canvas.suspeito {{ border: 1px solid #FFCC00; box-shadow: 0 0 4px #FFCC00; }}
    </style>
</head>
<body>
    <h1>🔬 Galeria Visual de Gráficos de Cenário - Sega Master System</h1>
    <div class="toolbar">
        <span>Filtro:</span>
        <button onclick="filtrar('todos')">Mostrar Todos ({len(blocos_encontrados)} blocos)</button>
        <button onclick="filtrar('placas')">Apenas Suspeitas de Placas/Ideogramas</button>
    </div>
    <div id="galeria"></div>

    <script>
        const blocos = {json.dumps(blocos_json)};
        const paleta = {json.dumps(paleta_hex)};

        function renderizar() {{
            const galeria = document.getElementById('galeria');
            galeria.innerHTML = '';

            blocos.forEach((b, bIdx) => {{
                const card = document.createElement('div');
                card.className = 'card' + (b.tem_placa ? ' alerta' : '');
                card.id = 'bloco-' + bIdx;

                let tag = b.tem_placa ? '<span class="tag-alerta">⚠️ POSSÍVEL PLACA / TEXTO DETECTADO</span>' : '';
                if (b.offset === "0x6158E") tag += '<span class="tag-alerta" style="background:#20E020; color:#000;">🍜 BARRACA DO YAKISOBA (BANCO 24)</span>';

                card.innerHTML = `<h3>Offset ROM: ${{b.offset}} | Banco: ${{b.banco}} | Total: ${{b.total_tiles}} tiles ${{tag}}</h3>
                                  <div class="tile-container" id="tiles-${{bIdx}}"></div>`;
                galeria.appendChild(card);

                const container = document.getElementById('tiles-' + bIdx);
                b.pixels.forEach((pxData, tIdx) => {{
                    const cv = document.createElement('canvas');
                    cv.width = 8;
                    cv.height = 8;
                    cv.title = 'Tile #' + tIdx;
                    if (b.tiles_texto.includes(tIdx)) cv.className = 'suspeito';

                    const ctx = cv.getContext('2d');
                    const imgData = ctx.createImageData(8, 8);
                    for (let i = 0; i < 64; i++) {{
                        const colorHex = paleta[pxData[i]] || '#000000';
                        const r = parseInt(colorHex.substr(1, 2), 16);
                        const g = parseInt(colorHex.substr(3, 2), 16);
                        const bVal = parseInt(colorHex.substr(5, 2), 16);
                        imgData.data[i * 4 + 0] = r;
                        imgData.data[i * 4 + 1] = g;
                        imgData.data[i * 4 + 2] = bVal;
                        imgData.data[i * 4 + 3] = 255;
                    }}
                    ctx.putImageData(imgData, 0, 0);
                    container.appendChild(cv);
                }});
            }});
        }}

        function filtrar(tipo) {{
            blocos.forEach((b, bIdx) => {{
                const el = document.getElementById('bloco-' + bIdx);
                if (tipo === 'placas' && !b.tem_placa) {{
                    el.style.display = 'none';
                }} else {{
                    el.style.display = 'block';
                }}
            }});
        }}

        renderizar();
    </script>
</body>
</html>
"""

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\n🎉 SUCESSO! Galeria gerada com perfeição: '{html_filename}'")
    print("👉 Para abrir e inspecionar visualmente com o mouse, digite no terminal:")
    print(f"   xdg-open {html_filename}")
    print("=" * 78)

if __name__ == "__main__":
    escanear_e_gerar_galeria()
