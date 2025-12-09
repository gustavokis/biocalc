"""
Módulo para geração de gráficos
Cria visualizações dos resultados
"""

import matplotlib.pyplot as plt
import matplotlib
from typing import Dict, Any
import numpy as np

# Configurar matplotlib para usar backend não-interativo
matplotlib.use('Agg')

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')


class GeradorGraficos:
    """Classe para geração de gráficos"""

    # Paleta de cores melhorada
    CORES = {
        'agricola': '#4CAF50',      # Verde
        'industrial': '#2196F3',     # Azul
        'distribuicao': '#FF9800',   # Laranja
        'uso': '#9C27B0',           # Roxo (mudado de vermelho)
        'fossil': '#D32F2F',        # Vermelho
        'bio': '#4CAF50'            # Verde
    }

    @staticmethod
    def grafico_barras_fases(resultados: Dict[str, Any], salvar: str = None):
        """
        Gera gráfico de barras com emissões por fase (MELHORADO).

        Args:
            resultados: Dicionário com resultados do cálculo
            salvar: Caminho para salvar o gráfico (opcional)

        Returns:
            Figura matplotlib
        """
        # Preparar dados
        fases = []
        emissoes = []
        percentuais = []

        for fase, dados in resultados['resultados_por_fase'].items():
            fases.append(fase.capitalize())
            emissoes.append(dados['emissoes_kg_co2'])
            percentuais.append(dados['percentual'])

        # Criar figura com tamanho maior
        fig, ax = plt.subplots(figsize=(12, 7))

        # Criar barras com gradiente
        cores_lista = [GeradorGraficos.CORES.get(f.lower(), '#999') for f in fases]
        barras = ax.bar(fases, emissoes, color=cores_lista, alpha=0.85,
                       edgecolor='black', linewidth=2, width=0.6)

        # Adicionar valores e percentuais nas barras
        for i, barra in enumerate(barras):
            altura = barra.get_height()
            # Valor absoluto
            ax.text(barra.get_x() + barra.get_width()/2., altura,
                   f'{altura:.2f} kg',
                   ha='center', va='bottom', fontsize=12, fontweight='bold')
            # Percentual
            ax.text(barra.get_x() + barra.get_width()/2., altura/2,
                   f'{percentuais[i]:.1f}%',
                   ha='center', va='center', fontsize=11,
                   color='white', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))

        # Adicionar linha de referência para o total
        total = resultados['emissoes_totais_kg_co2']
        ax.axhline(y=total, color='red', linestyle='--', linewidth=2.5,
                  label=f'Total: {total:.2f} kg CO₂', alpha=0.8)

        # Configurar eixos e títulos
        ax.set_ylabel('Emissões (kg CO₂)', fontsize=13, fontweight='bold')
        ax.set_xlabel('Fases do Ciclo de Vida', fontsize=13, fontweight='bold')
        ax.set_title(f'Emissões de GEE por Fase do Ciclo de Vida\nBiomassa: {resultados["biomassa"].capitalize()} | '
                    f'CI: {resultados["intensidade_carbono_g_co2_mj"]:.2f} gCO₂/MJ',
                    fontsize=15, fontweight='bold', pad=20)

        # Grid melhorado
        ax.grid(axis='y', alpha=0.4, linestyle='--', linewidth=0.8)
        ax.set_axisbelow(True)

        # Legenda melhorada
        ax.legend(loc='upper right', fontsize=11, framealpha=0.9, shadow=True)

        # Melhorar aparência dos eixos
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Ajustar layout
        plt.tight_layout()

        # Salvar se solicitado
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight', facecolor='white')

        return fig

    @staticmethod
    def grafico_pizza_fases(resultados: Dict[str, Any], salvar: str = None):
        """
        Gera gráfico de pizza com percentuais por fase (MELHORADO).

        Args:
            resultados: Dicionário com resultados do cálculo
            salvar: Caminho para salvar o gráfico (opcional)

        Returns:
            Figura matplotlib
        """
        # Preparar dados
        fases = []
        percentuais = []
        emissoes = []

        for fase, dados in resultados['resultados_por_fase'].items():
            if dados['percentual'] > 0.1:  # Apenas fases com emissões > 0.1%
                fases.append(fase.capitalize())
                percentuais.append(dados['percentual'])
                emissoes.append(dados['emissoes_kg_co2'])

        # Criar figura
        fig, ax = plt.subplots(figsize=(11, 9))

        # Cores
        cores_lista = [GeradorGraficos.CORES.get(f.lower(), '#999') for f in fases]

        # Criar pizza com explode automático
        explode = [0.05 if p == max(percentuais) else 0.02 for p in percentuais]

        # Criar função autopct com closure para acessar emissões
        def make_autopct(emissoes_list, percentuais_list):
            def autopct_func(pct):
                # Encontrar índice correto baseado no percentual
                for i, p in enumerate(percentuais_list):
                    if abs(p - pct) < 0.01:  # Tolerância para comparação de floats
                        if pct > 5:
                            return f'{pct:.1f}%\n({emissoes_list[i]:.1f} kg)'
                        else:
                            return ''
                return ''
            return autopct_func

        wedges, texts, autotexts = ax.pie(
            percentuais,
            labels=None,  # Vamos adicionar legenda separada
            colors=cores_lista,
            autopct=make_autopct(emissoes, percentuais),
            startangle=90,
            explode=explode,
            shadow=True,
            textprops={'fontsize': 11, 'fontweight': 'bold'}
        )

        # Estilizar textos
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        # Adicionar legenda com informações
        legend_labels = [f'{fase}: {perc:.1f}% ({emis:.2f} kg CO₂)'
                        for fase, perc, emis in zip(fases, percentuais, emissoes)]
        ax.legend(wedges, legend_labels,
                 title="Fases",
                 loc="center left",
                 bbox_to_anchor=(1, 0, 0.5, 1),
                 fontsize=10)

        # Título
        ax.set_title(f'Distribuição de Emissões por Fase\nBiomassa: {resultados["biomassa"].capitalize()}\n'
                    f'Total: {resultados["emissoes_totais_kg_co2"]:.2f} kg CO₂',
                    fontsize=14, fontweight='bold', pad=20)

        # Ajustar layout
        plt.tight_layout()

        # Salvar se solicitado
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight', facecolor='white')

        return fig

    @staticmethod
    def grafico_comparacao_fossil(resultados: Dict[str, Any], salvar: str = None):
        """
        Gera gráfico de comparação com combustível fóssil (MELHORADO).

        Args:
            resultados: Dicionário com resultados do cálculo
            salvar: Caminho para salvar o gráfico (opcional)

        Returns:
            Figura matplotlib
        """
        # Preparar dados
        comparacao = resultados['comparacao_fossil']
        categorias = ['Combustível\nFóssil', f'Biocombustível\n({resultados["biomassa"].capitalize()})']
        valores = [
            comparacao['ci_fossil_referencia_g_co2_mj'],
            comparacao['ci_biocombustivel_g_co2_mj']
        ]
        cores_barras = [GeradorGraficos.CORES['fossil'], GeradorGraficos.CORES['bio']]

        # Criar figura
        fig, ax = plt.subplots(figsize=(12, 7))

        # Criar barras
        barras = ax.bar(categorias, valores, color=cores_barras, alpha=0.85,
                       edgecolor='black', linewidth=2, width=0.5)

        # Adicionar valores nas barras
        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura + 2,
                   f'{altura:.2f}\ngCO₂/MJ',
                   ha='center', va='bottom', fontsize=13, fontweight='bold')

        # Adicionar área de redução
        reducao = comparacao['reducao_percentual']
        reducao_valor = comparacao['reducao_g_co2_mj']

        # Desenhar área de redução
        ax.fill_between([-0.5, 1.5],
                       [valores[1], valores[1]],
                       [valores[0], valores[0]],
                       alpha=0.2, color='green',
                       label=f'Redução: {reducao_valor:.2f} gCO₂/MJ')

        # Adicionar seta e texto de redução
        mid_x = 0.5
        mid_y_start = valores[0]
        mid_y_end = valores[1]

        ax.annotate(
            f'REDUÇÃO\n{reducao:.1f}%',
            xy=(mid_x, mid_y_end),
            xytext=(mid_x, (mid_y_start + mid_y_end) / 2),
            ha='center',
            fontsize=14,
            fontweight='bold',
            color='darkgreen',
            bbox=dict(boxstyle='round,pad=0.7', facecolor='lightgreen', alpha=0.8, edgecolor='green', linewidth=2),
            arrowprops=dict(arrowstyle='->', lw=3, color='green')
        )

        # Configurar eixos e títulos
        ax.set_ylabel('Intensidade de Carbono (gCO₂/MJ)', fontsize=13, fontweight='bold')
        ax.set_title('Comparação: Biocombustível vs. Combustível Fóssil\nAnálise de Intensidade de Carbono',
                    fontsize=15, fontweight='bold', pad=20)

        # Grid
        ax.grid(axis='y', alpha=0.4, linestyle='--', linewidth=0.8)
        ax.set_axisbelow(True)

        # Legenda
        ax.legend(loc='upper right', fontsize=11, framealpha=0.9, shadow=True)

        # Melhorar aparência
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Ajustar layout
        plt.tight_layout()

        # Salvar se solicitado
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight', facecolor='white')

        return fig

    @staticmethod
    def grafico_completo(resultados: Dict[str, Any], salvar: str = None):
        """
        Gera um dashboard completo com múltiplos subplots (MELHORADO).

        Args:
            resultados: Dicionário com resultados do cálculo
            salvar: Caminho para salvar o gráfico (opcional)

        Returns:
            Figura matplotlib
        """
        # Criar figura com subplots
        fig = plt.figure(figsize=(18, 12))

        # Definir grid
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # Subplot 1: Barras por fase (grande, 2 colunas)
        ax1 = fig.add_subplot(gs[0, :2])
        GeradorGraficos._subplot_barras_fases(ax1, resultados)

        # Subplot 2: Comparação com fóssil (grande, 2 colunas)
        ax2 = fig.add_subplot(gs[1, :2])
        GeradorGraficos._subplot_comparacao_fossil(ax2, resultados)

        # Subplot 3: Pizza de percentuais
        ax3 = fig.add_subplot(gs[0, 2])
        GeradorGraficos._subplot_pizza_fases(ax3, resultados)

        # Subplot 4: Métricas textuais (aumentado)
        ax4 = fig.add_subplot(gs[1:, 2])
        GeradorGraficos._subplot_metricas_melhorado(ax4, resultados)

        # Subplot 5: Gráfico de linha horizontal (detalhamento por fase)
        ax5 = fig.add_subplot(gs[2, :2])
        GeradorGraficos._subplot_detalhamento_fases(ax5, resultados)

        # Título geral
        fig.suptitle(f'Dashboard Completo - Análise do Ciclo de Vida\n{resultados["biomassa"].capitalize()} Pellets',
                    fontsize=18, fontweight='bold', y=0.98)

        # Ajustar layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Salvar se solicitado
        if salvar:
            plt.savefig(salvar, dpi=300, bbox_inches='tight', facecolor='white')

        return fig

    @staticmethod
    def _subplot_barras_fases(ax, resultados):
        """Helper para subplot de barras (melhorado)"""
        fases = [f.capitalize() for f in resultados['resultados_por_fase'].keys()]
        emissoes = [d['emissoes_kg_co2'] for d in resultados['resultados_por_fase'].values()]
        cores = [GeradorGraficos.CORES.get(f.lower(), '#999') for f in fases]

        barras = ax.bar(fases, emissoes, color=cores, alpha=0.85, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Emissões (kg CO₂)', fontweight='bold')
        ax.set_title('Emissões por Fase', fontweight='bold', fontsize=12)
        ax.grid(axis='y', alpha=0.3)

        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura,
                   f'{altura:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    @staticmethod
    def _subplot_pizza_fases(ax, resultados):
        """Helper para subplot de pizza (melhorado)"""
        fases = [f.capitalize() for f in resultados['resultados_por_fase'].keys()]
        percentuais = [d['percentual'] for d in resultados['resultados_por_fase'].values()]
        cores = [GeradorGraficos.CORES.get(f.lower(), '#999') for f in fases]

        # Filtrar fases com emissões
        dados_filtrados = [(f, p, c) for f, p, c in zip(fases, percentuais, cores) if p > 0.1]
        if dados_filtrados:
            fases_f, perc_f, cores_f = zip(*dados_filtrados)
            ax.pie(perc_f, labels=fases_f, colors=cores_f, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
        ax.set_title('Distribuição (%)', fontweight='bold', fontsize=11)

    @staticmethod
    def _subplot_comparacao_fossil(ax, resultados):
        """Helper para subplot de comparação (melhorado)"""
        comparacao = resultados['comparacao_fossil']
        categorias = ['Fóssil', 'Bio']
        valores = [
            comparacao['ci_fossil_referencia_g_co2_mj'],
            comparacao['ci_biocombustivel_g_co2_mj']
        ]
        cores = [GeradorGraficos.CORES['fossil'], GeradorGraficos.CORES['bio']]

        barras = ax.bar(categorias, valores, color=cores, alpha=0.85, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('gCO₂/MJ', fontweight='bold')
        ax.set_title('Comparação com Fóssil', fontweight='bold', fontsize=12)
        ax.grid(axis='y', alpha=0.3)

        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura,
                   f'{altura:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

        # Adicionar texto de redução
        reducao = comparacao['reducao_percentual']
        ax.text(0.5, max(valores) * 0.5, f'↓ {reducao:.1f}%',
               ha='center', fontsize=12, fontweight='bold', color='green',
               bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    @staticmethod
    def _subplot_detalhamento_fases(ax, resultados):
        """Helper para subplot de detalhamento por fase (NOVO)"""
        fases = list(resultados['resultados_por_fase'].keys())

        # Preparar dados de detalhamento
        componentes_unicos = set()
        for dados_fase in resultados['resultados_por_fase'].values():
            componentes_unicos.update(dados_fase.get('detalhamento', {}).keys())

        componentes_unicos = [c for c in componentes_unicos if isinstance(
            resultados['resultados_por_fase'][fases[0]].get('detalhamento', {}).get(c, 0), (int, float))]

        if not componentes_unicos:
            ax.text(0.5, 0.5, 'Detalhamento não disponível', ha='center', va='center', fontsize=11)
            ax.axis('off')
            return

        # Criar barras empilhadas
        x = np.arange(len(fases))
        width = 0.6

        bottom = np.zeros(len(fases))
        cores_comp = plt.cm.Set3(np.linspace(0, 1, len(componentes_unicos)))

        for i, comp in enumerate(componentes_unicos):
            valores = []
            for fase in fases:
                detalhamento = resultados['resultados_por_fase'][fase].get('detalhamento', {})
                valor = detalhamento.get(comp, 0)
                valores.append(valor if isinstance(valor, (int, float)) else 0)

            ax.bar(x, valores, width, label=comp.capitalize(), bottom=bottom,
                  color=cores_comp[i], alpha=0.8, edgecolor='black', linewidth=0.5)
            bottom += valores

        ax.set_ylabel('Emissões (kg CO₂)', fontweight='bold')
        ax.set_title('Detalhamento de Emissões por Componente', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels([f.capitalize() for f in fases])
        ax.legend(loc='upper right', fontsize=8, ncol=2)
        ax.grid(axis='y', alpha=0.3)

    @staticmethod
    def _subplot_metricas_melhorado(ax, resultados):
        """Helper para subplot de métricas (melhorado)"""
        ax.axis('off')

        # Criar caixa de métricas com formatação melhorada
        metricas_texto = f"""
╔═══════════════════════════════════╗
║      MÉTRICAS PRINCIPAIS          ║
╚═══════════════════════════════════╝

🌱 Biomassa: {resultados['biomassa'].capitalize()}
⚡ PCI: {resultados['biomassa_info']['pci']} MJ/kg
📦 Densidade: {resultados['biomassa_info']['densidade']} kg/m³

───────────────────────────────────
💨 EMISSÕES
───────────────────────────────────
Total: {resultados['emissoes_totais_kg_co2']:.2f} kg CO₂
Energia: {resultados['energia_total_mj']:.2f} MJ

───────────────────────────────────
📊 INDICADORES
───────────────────────────────────
CI: {resultados['intensidade_carbono_g_co2_mj']:.2f} gCO₂/MJ

NEEA: {resultados['neea']:.2f} gCO₂/MJ

───────────────────────────────────
✅ DESEMPENHO AMBIENTAL
───────────────────────────────────
Redução vs. Fóssil:
   {resultados['comparacao_fossil']['reducao_percentual']:.1f}%
   ({resultados['comparacao_fossil']['reducao_g_co2_mj']:.2f} gCO₂/MJ)

───────────────────────────────────
🏆 CLASSIFICAÇÃO
───────────────────────────────────
"""
        # Adicionar classificação baseada na redução
        reducao = resultados['comparacao_fossil']['reducao_percentual']
        if reducao >= 80:
            classificacao = "⭐⭐⭐⭐⭐ EXCELENTE"
        elif reducao >= 60:
            classificacao = "⭐⭐⭐⭐ MUITO BOM"
        elif reducao >= 40:
            classificacao = "⭐⭐⭐ BOM"
        elif reducao >= 20:
            classificacao = "⭐⭐ REGULAR"
        else:
            classificacao = "⭐ BAIXO"

        metricas_texto += f"{classificacao}"

        ax.text(0.05, 0.95, metricas_texto,
               fontsize=9,
               verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='#f0f0f0', alpha=0.9, edgecolor='black', linewidth=2))
