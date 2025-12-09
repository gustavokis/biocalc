"""
BioCalc - Aplicação Streamlit
Calculadora de Intensidade de Carbono para Biocombustíveis Sólidos
"""

import streamlit as st
from src.core.calculo import CalculadoraBioCalc
from src.utils.validacao import Validador
from src.utils.export import Exportador
from src.utils.graficos import GeradorGraficos

# Configuração da página
st.set_page_config(
    page_title="BioCalc - Calculadora de Carbono",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2e7d32;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'calculadora' not in st.session_state:
    st.session_state.calculadora = CalculadoraBioCalc()
    st.session_state.resultados = None
    st.session_state.dados_entrada = None


def main():
    """Função principal da aplicação"""

    # Header
    st.markdown('<div class="main-header">🌱 BioCalc</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Calculadora de Intensidade de Carbono para Biocombustíveis Sólidos</div>',
                unsafe_allow_html=True)

    # Sidebar - Seleção de Biomassa
    with st.sidebar:
        st.header("⚙️ Configuração")

        biomassa_selecionada = st.selectbox(
            "Selecione a Biomassa",
            options=['pinus', 'eucalipto', 'amendoim'],
            format_func=lambda x: {
                'pinus': '🌲 Pinus',
                'eucalipto': '🌳 Eucalipto',
                'amendoim': '🥜 Amendoim'
            }[x]
        )

        # Mostrar informações da biomassa
        biomassa_info = st.session_state.calculadora.get_biomassa_info(biomassa_selecionada)
        st.info(f"""
        **{biomassa_info['nome']}**

        {biomassa_info['descricao']}

        **PCI:** {biomassa_info['pci']} MJ/kg
        **Densidade:** {biomassa_info['densidade']} kg/m³
        **Tipo:** {biomassa_info['tipo'].replace('_', ' ').title()}
        """)

        st.divider()
        st.caption("v1.0.0 | Sustentabilidade em Computação - 2025")

    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["📝 Entrada de Dados", "📊 Resultados", "📚 Histórico"])

    with tab1:
        entrada_dados(biomassa_selecionada)

    with tab2:
        exibir_resultados()

    with tab3:
        exibir_historico()


def entrada_dados(biomassa: str):
    """Interface de entrada de dados"""

    st.header("Entrada de Dados por Fase")
    st.markdown("Preencha os dados para cada fase do ciclo de vida do biocombustível.")

    # Criar abas para cada fase
    fase_tabs = st.tabs(["🌾 Fase Agrícola", "🏭 Fase Industrial", "🚛 Fase Distribuição", "🔥 Fase Uso"])

    # Fase Agrícola
    with fase_tabs[0]:
        st.subheader("Fase Agrícola")
        st.markdown("*Produção, colheita e transporte curto da biomassa*")

        col1, col2 = st.columns(2)

        with col1:
            quantidade_biomassa = st.number_input(
                "Quantidade de Biomassa (kg)",
                min_value=0.0,
                value=1000.0,
                step=100.0,
                help="Quantidade total de biomassa a ser processada"
            )

            distancia_transporte = st.number_input(
                "Distância de Transporte (km)",
                min_value=0.0,
                value=50.0,
                step=10.0,
                help="Distância do ponto de coleta até a planta industrial"
            )

        with col2:
            uso_fertilizantes = st.number_input(
                "Uso de Fertilizantes (kg)",
                min_value=0.0,
                value=10.0,
                step=1.0,
                help="Quantidade de fertilizantes utilizados"
            )

            uso_pesticidas = st.number_input(
                "Uso de Pesticidas (kg)",
                min_value=0.0,
                value=2.0,
                step=0.5,
                help="Quantidade de pesticidas utilizados"
            )

        luc_dluc = st.number_input(
            "LUC/dLUC Opcional (kg CO₂)",
            min_value=0.0,
            value=0.0,
            step=10.0,
            help="Emissões de mudança de uso da terra (opcional, campo agregado)"
        )

        dados_agricola = {
            'quantidade_biomassa_kg': quantidade_biomassa,
            'distancia_transporte_km': distancia_transporte,
            'uso_fertilizantes_kg': uso_fertilizantes,
            'uso_pesticidas_kg': uso_pesticidas,
            'luc_dluc_opcional_kg_co2': luc_dluc
        }

    # Fase Industrial
    with fase_tabs[1]:
        st.subheader("Fase Industrial")
        st.markdown("*Processamento da biomassa em pellets/briquetes*")

        col1, col2 = st.columns(2)

        with col1:
            energia_eletrica = st.number_input(
                "Energia Elétrica (kWh)",
                min_value=0.0,
                value=150.0,
                step=10.0,
                help="Consumo de energia elétrica na planta"
            )

            energia_termica = st.number_input(
                "Energia Térmica (MJ)",
                min_value=0.0,
                value=500.0,
                step=50.0,
                help="Consumo de energia térmica (secagem, aquecimento)"
            )

        with col2:
            agua = st.number_input(
                "Água (m³)",
                min_value=0.0,
                value=5.0,
                step=1.0,
                help="Consumo de água no processo"
            )

        dados_industrial = {
            'energia_eletrica_kwh': energia_eletrica,
            'energia_termica_mj': energia_termica,
            'agua_m3': agua
        }

    # Fase Distribuição
    with fase_tabs[2]:
        st.subheader("Fase Distribuição")
        st.markdown("*Transporte do produto final até o consumidor*")

        col1, col2 = st.columns(2)

        with col1:
            modal_transporte = st.selectbox(
                "Modal de Transporte",
                options=['rodoviario', 'maritimo', 'ferroviario'],
                format_func=lambda x: {
                    'rodoviario': '🚛 Rodoviário',
                    'maritimo': '🚢 Marítimo',
                    'ferroviario': '🚂 Ferroviário'
                }[x],
                help="Modo de transporte utilizado"
            )

        with col2:
            distancia_distribuicao = st.number_input(
                "Distância (km)",
                min_value=0.0,
                value=200.0,
                step=50.0,
                help="Distância até o consumidor final"
            )

        dados_distribuicao = {
            'modal_transporte': modal_transporte,
            'distancia_km': distancia_distribuicao
        }

    # Fase Uso
    with fase_tabs[3]:
        st.subheader("Fase Uso")
        st.markdown("*Combustão para geração de energia*")

        tipo_combustao = st.selectbox(
            "Tipo de Combustão",
            options=['caldeira', 'fornalha', 'outro'],
            format_func=lambda x: {
                'caldeira': '🔥 Caldeira',
                'fornalha': '🔥 Fornalha',
                'outro': '🔥 Outro'
            }[x],
            help="Tipo de equipamento de combustão"
        )

        st.info("ℹ️ As emissões biogênicas de CO₂ da combustão são consideradas neutras (CF=0) seguindo a metodologia RenovaCalc/IPCC.")

        dados_uso = {
            'tipo_combustao': tipo_combustao
        }

    # Botão Calcular
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("🧮 Calcular Intensidade de Carbono", type="primary", use_container_width=True):
            # Preparar dados de entrada
            dados_entrada = {
                'biomassa': biomassa,
                'fase_agricola': dados_agricola,
                'fase_industrial': dados_industrial,
                'fase_distribuicao': dados_distribuicao,
                'fase_uso': dados_uso
            }

            # Validar dados
            valido, erros = Validador.validar_completo(dados_entrada)

            if not valido:
                st.error("❌ Erros de validação encontrados:")
                for fase, lista_erros in erros.items():
                    st.error(f"**{fase}:**")
                    for erro in lista_erros:
                        st.write(f"  - {erro}")
            else:
                # Calcular
                with st.spinner("Calculando..."):
                    try:
                        resultados = st.session_state.calculadora.calcular_intensidade_carbono(dados_entrada)
                        st.session_state.resultados = resultados
                        st.session_state.dados_entrada = dados_entrada

                        # Adicionar ao histórico
                        if 'historico' not in st.session_state:
                            st.session_state.historico = []

                        from datetime import datetime
                        resultado_com_timestamp = resultados.copy()
                        resultado_com_timestamp['timestamp'] = datetime.now()
                        resultado_com_timestamp['dados_entrada'] = dados_entrada
                        st.session_state.historico.append(resultado_com_timestamp)

                        st.success("✅ Cálculo realizado com sucesso! Veja os resultados na aba 'Resultados'.")
                    except Exception as e:
                        st.error(f"❌ Erro ao calcular: {str(e)}")


def exibir_resultados():
    """Exibe os resultados dos cálculos"""

    if st.session_state.resultados is None:
        st.info("ℹ️ Nenhum cálculo realizado ainda. Preencha os dados na aba 'Entrada de Dados' e clique em 'Calcular'.")
        return

    resultados = st.session_state.resultados

    st.header("Resultados da Análise")

    # Métricas principais
    st.subheader("📊 Métricas Principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Intensidade de Carbono",
            value=f"{resultados['intensidade_carbono_g_co2_mj']:.2f}",
            delta=None,
            help="gCO₂/MJ"
        )
        st.caption("gCO₂/MJ")

    with col2:
        st.metric(
            label="NEEA",
            value=f"{resultados['neea']:.2f}",
            delta=None,
            help="Eficiência Energético-Ambiental"
        )
        st.caption("gCO₂/MJ")

    with col3:
        reducao = resultados['comparacao_fossil']['reducao_percentual']
        st.metric(
            label="Redução vs. Fóssil",
            value=f"{reducao:.1f}%",
            delta=f"{reducao:.1f}%",
            delta_color="normal"
        )
        st.caption("Comparado ao fóssil de referência")

    with col4:
        st.metric(
            label="Emissões Totais",
            value=f"{resultados['emissoes_totais_kg_co2']:.2f}",
            delta=None
        )
        st.caption("kg CO₂")

    st.divider()

    # Tabela de resultados por fase
    st.subheader("📋 Emissões por Fase")

    import pandas as pd

    dados_tabela = []
    for fase, dados in resultados['resultados_por_fase'].items():
        dados_tabela.append({
            'Fase': fase.capitalize(),
            'Emissões (kg CO₂)': round(dados['emissoes_kg_co2'], 2),
            'Percentual (%)': round(dados['percentual'], 1)
        })

    df_tabela = pd.DataFrame(dados_tabela)
    st.dataframe(df_tabela, use_container_width=True, hide_index=True)

    st.divider()

    # Comparação com fóssil
    st.subheader("⚖️ Comparação com Combustível Fóssil")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "CI Fóssil de Referência",
            f"{resultados['comparacao_fossil']['ci_fossil_referencia_g_co2_mj']:.2f} gCO₂/MJ"
        )

    with col2:
        st.metric(
            "CI Biocombustível",
            f"{resultados['comparacao_fossil']['ci_biocombustivel_g_co2_mj']:.2f} gCO₂/MJ"
        )

    st.success(f"✅ Redução de **{resultados['comparacao_fossil']['reducao_g_co2_mj']:.2f} gCO₂/MJ** "
               f"({resultados['comparacao_fossil']['reducao_percentual']:.1f}%) em relação ao combustível fóssil!")

    st.divider()

    # Gráficos
    st.subheader("📈 Visualizações")

    tab_graficos = st.tabs(["📊 Barras por Fase", "🥧 Distribuição", "⚖️ Comparação Fóssil", "📋 Dashboard Completo"])

    with tab_graficos[0]:
        st.markdown("**Emissões de GEE por Fase do Ciclo de Vida**")
        fig_barras = GeradorGraficos.grafico_barras_fases(resultados)
        st.pyplot(fig_barras)

        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""
            Este gráfico mostra as emissões de gases de efeito estufa (kg CO₂) de cada fase do ciclo de vida:
            - **Fase Agrícola**: Cultivo, colheita e transporte curto da biomassa
            - **Fase Industrial**: Processamento da biomassa em pellets/briquetes
            - **Fase Distribuição**: Transporte do produto final até o consumidor
            - **Fase Uso**: Combustão para geração de energia (normalmente zero por ser biogênico)

            Os percentuais indicam a contribuição de cada fase para o total de emissões.
            """)

    with tab_graficos[1]:
        st.markdown("**Distribuição Percentual de Emissões**")
        fig_pizza = GeradorGraficos.grafico_pizza_fases(resultados)
        st.pyplot(fig_pizza)

        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""
            Este gráfico de pizza mostra a distribuição percentual das emissões entre as diferentes fases.

            **Interpretação:**
            - Fatias maiores indicam fases com maior impacto ambiental
            - Identifique os "hotspots" de emissões para priorizar melhorias
            - Compare com outras biomassas para escolher a melhor opção
            """)

    with tab_graficos[2]:
        st.markdown("**Comparação com Combustível Fóssil de Referência**")
        fig_comparacao = GeradorGraficos.grafico_comparacao_fossil(resultados)
        st.pyplot(fig_comparacao)

        with st.expander("ℹ️ Sobre este gráfico"):
            st.markdown("""
            Este gráfico compara a intensidade de carbono (gCO₂/MJ) do biocombustível com um combustível fóssil de referência.

            **Métrica NEEA (Eficiência Energético-Ambiental):**
            - NEEA = CI_fóssil - CI_biocombustível
            - Valores positivos indicam redução de emissões
            - Quanto maior o NEEA, melhor o desempenho ambiental

            **Classificação:**
            - ⭐⭐⭐⭐⭐ Excelente: ≥ 80% de redução
            - ⭐⭐⭐⭐ Muito Bom: 60-79% de redução
            - ⭐⭐⭐ Bom: 40-59% de redução
            """)

    with tab_graficos[3]:
        st.markdown("**Dashboard Completo com Todas as Análises**")
        st.info("💡 Dica: Use o botão de fullscreen para melhor visualização")
        fig_dashboard = GeradorGraficos.grafico_completo(resultados)
        st.pyplot(fig_dashboard)

        # Botão para salvar dashboard
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("💾 Salvar Dashboard como Imagem", use_container_width=True):
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"dashboard_biocalc_{resultados['biomassa']}_{timestamp}.png"
                fig_dashboard.savefig(nome_arquivo, dpi=300, bbox_inches='tight', facecolor='white')
                st.success(f"✅ Dashboard salvo: {nome_arquivo}")

    st.divider()

    # Exportação
    st.subheader("💾 Exportar Resultados")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📄 Exportar CSV Resumido", use_container_width=True):
            nome_arquivo = Exportador.exportar_csv(resultados)
            st.success(f"✅ Arquivo exportado: {nome_arquivo}")

            # Download
            with open(nome_arquivo, 'rb') as f:
                st.download_button(
                    label="⬇️ Download CSV",
                    data=f,
                    file_name=nome_arquivo,
                    mime="text/csv"
                )

    with col2:
        if st.button("📄 Exportar CSV Detalhado", use_container_width=True):
            nome_arquivo = Exportador.exportar_detalhado_csv(resultados)
            st.success(f"✅ Arquivo exportado: {nome_arquivo}")

            # Download
            with open(nome_arquivo, 'rb') as f:
                st.download_button(
                    label="⬇️ Download CSV Detalhado",
                    data=f,
                    file_name=nome_arquivo,
                    mime="text/csv"
                )


def exibir_historico():
    """Exibe o histórico de cálculos realizados"""

    st.header("📚 Histórico de Cálculos")

    # Inicializar histórico se não existir
    if 'historico' not in st.session_state:
        st.session_state.historico = []

    if len(st.session_state.historico) == 0:
        st.info("ℹ️ Nenhum cálculo no histórico ainda. Realize cálculos na aba 'Entrada de Dados' para vê-los aqui.")
        return

    # Estatísticas gerais
    st.subheader("📊 Estatísticas Gerais")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total de Cálculos", len(st.session_state.historico))

    with col2:
        biomassas = [r['biomassa'] for r in st.session_state.historico]
        biomassa_mais_usada = max(set(biomassas), key=biomassas.count) if biomassas else "N/A"
        st.metric("Biomassa Mais Usada", biomassa_mais_usada.title())

    with col3:
        ci_medio = sum(r['intensidade_carbono_g_co2_mj'] for r in st.session_state.historico) / len(st.session_state.historico)
        st.metric("CI Médio", f"{ci_medio:.2f} gCO₂/MJ")

    st.divider()

    # Botões de ação
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🗑️ Limpar Todo Histórico", type="secondary"):
            st.session_state.historico = []
            st.rerun()

    st.divider()

    # Lista de cálculos (mais recentes primeiro)
    st.subheader("📋 Cálculos Realizados")

    for idx, resultado in enumerate(reversed(st.session_state.historico)):
        real_idx = len(st.session_state.historico) - 1 - idx

        with st.expander(
            f"🌱 {resultado['biomassa'].title()} - "
            f"{resultado['timestamp'].strftime('%d/%m/%Y %H:%M:%S')} - "
            f"CI: {resultado['intensidade_carbono_g_co2_mj']:.2f} gCO₂/MJ",
            expanded=False
        ):
            col1, col2 = st.columns([4, 1])

            with col1:
                # Informações principais
                st.markdown(f"""
                **Biomassa:** {resultado['biomassa'].title()}
                **Data/Hora:** {resultado['timestamp'].strftime('%d/%m/%Y às %H:%M:%S')}
                **Intensidade de Carbono:** {resultado['intensidade_carbono_g_co2_mj']:.2f} gCO₂/MJ
                **NEEA:** {resultado['neea']:.2f} gCO₂/MJ
                **Redução vs Fóssil:** {resultado['comparacao_fossil']['reducao_percentual']:.1f}%
                """)

                # Emissões por fase
                st.markdown("**Emissões por Fase:**")
                for fase, dados in resultado['resultados_por_fase'].items():
                    st.markdown(f"- **{fase.title()}:** {dados['emissoes_kg_co2']:.2f} kg CO₂ ({dados['percentual']:.1f}%)")

                # Dados de entrada
                with st.expander("Ver dados de entrada"):
                    st.json(resultado['dados_entrada'])

            with col2:
                # Botão para excluir este cálculo
                if st.button(f"🗑️ Excluir", key=f"delete_{real_idx}"):
                    st.session_state.historico.pop(real_idx)
                    st.rerun()

                # Botão para carregar este cálculo
                if st.button(f"📥 Carregar", key=f"load_{real_idx}"):
                    st.session_state.resultados = resultado
                    st.session_state.dados_entrada = resultado['dados_entrada']
                    st.success("✅ Cálculo carregado! Veja na aba 'Resultados'")


if __name__ == "__main__":
    main()
