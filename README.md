# BioCalc - Calculadora de Intensidade de Carbono para Biocombustíveis Sólidos

Aplicação local em Python que calcula a intensidade de carbono (gCO₂e/MJ) de biocombustíveis sólidos (pellets e briquetes) ao longo de 4 fases da cadeia produtiva: agrícola, industrial, distribuição e uso.

## 🎯 Objetivos

Transformar a planilha Excel BioCalc_EngS.xlsx em um software funcional com:
- Entrada guiada e validada de dados
- Motor de cálculo centralizado
- Resultados padronizados (tabela, gráfico, export CSV)
- Reprodutibilidade com fatores versionados

## 📋 Funcionalidades

- ✅ Seleção de 3 biomassas preset (amendoim, pinus, eucalipto)
- ✅ Entrada de dados por fase (agrícola, industrial, distribuição, uso)
- ✅ Cálculo de intensidade de carbono (gCO₂e/MJ)
- ✅ Cálculo de NEEA (Eficiência Energético-Ambiental)
- ✅ Comparação com combustível fóssil de referência
- ✅ Tabela de resultados por fase
- ✅ Gráfico de barras comparativo
- ✅ Exportação para CSV

## 🏗️ Arquitetura

```
BioCalc/
├── data/
│   ├── fatores.csv                 # Fatores de emissão
│   └── biomasses_preset.json       # Dados das biomassas
├── src/
│   ├── core/                       # Motor de cálculo
│   ├── utils/                      # Utilit\u00e1rios
│   └── extractor/                  # Extração de dados
├── tests/                          # Testes
├── app.py                          # Aplicação Streamlit
└── requirements.txt                # Dependências
```

## 📦 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 🚀 Como Executar

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no seu navegador padrão em `http://localhost:8501`

## 📚 Como Usar

### 1. Seleção de Biomassa
- Escolha uma das 3 biomassas preset: amendoim, pinus ou eucalipto
- Visualize o PCI (Poder Calorífico Inferior) da biomassa selecionada

### 2. Entrada de Dados

**Fase Agrícola:**
- Quantidade de biomassa (kg)
- Distância de transporte (km)
- Uso de fertilizantes (kg)
- Uso de pesticidas (kg)
- LUC/dLUC opcional (kg CO₂) - campo agregado opcional

**Fase Industrial:**
- Energia elétrica (kWh)
- Energia térmica (MJ)
- Água (m³)

**Fase Distribuição:**
- Modal de transporte (rodoviário, marítimo, ferroviário)
- Distância (km)

**Fase Uso:**
- Tipo de combustão (caldeira, fornalha, outro)

### 3. Visualização de Resultados

- Tabela com emissões por fase e percentuais
- Intensidade de carbono total (gCO₂e/MJ)
- NEEA e comparação com fóssil
- Gráfico de barras por fase
- Botão para exportar resultados em CSV

## 🧪 Testes

Execute os testes unitários:

```bash
pytest tests/
```

## 📊 Metodologia

- **Abordagem:** ACV (Avaliação do Ciclo de Vida) atribucional cradle-to-grave
- **Métrica:** NEEA (Eficiência Energético-Ambiental)
- **Padrão:** IPCC/RenovaCalc (GWP100)
- **Sistema de fronteira:** 4 fases (agrícola, industrial, distribuição, uso)

### Fórmulas Principais

**Intensidade de Carbono (CI):**
```
CI = (Σ Emissões_todas_fases) / (Biomassa_kg × PCI)  [gCO₂e/MJ]
```

**NEEA:**
```
NEEA = CI_fossil_referencia - CI_biocombustível  [gCO₂e/MJ]
```

## 🔬 Dados e Fatores

### Biomassas Preset

| Biomassa | PCI (MJ/kg) | Densidade (kg/m³) | Tipo |
|----------|-------------|-------------------|------|
| Amendoim | 17.8 | 600 | Resíduo agrícola |
| Pinus | 18.5 | 550 | Resíduo florestal |
| Eucalipto | 18.2 | 580 | Resíduo florestal |

### Fatores de Emissão

Todos os fatores estão documentados em `data/fatores.csv`, incluindo:
- Eletricidade (gCO₂/kWh)
- Combustíveis (gCO₂/L ou gCO₂/m³)
- Transporte (gCO₂/tkm)
- Insumos agrícolas (gCO₂/kg)

## 🚫 Fora do Escopo

Esta versão **NÃO** inclui:
- Comparação de múltiplos cenários simultaneamente
- Dashboards avançados
- Sistema de login/multiusuário
- Banco de dados persistente
- Geração automática de PDF
- Integrações com APIs externas
- Modelagem espacial de LUC/dLUC (campo agregado opcional)

## 📖 Referências

- **Artigo BioCalc:** Farrapo et al. (2025). BioCalc: a novel life cycle-based tool for quantifying the carbon credits of solid biofuels in Brazil. *Biomass and Bioenergy*.
- **RenovaCalc:** Metodologia de cálculo de intensidade de carbono do Programa RenovaBio
- **IPCC:** Sixth Assessment Report (GWP100)

## 👥 Equipe

- Bruna Scarpelli
- Gustavo Sanches Martins Kis
- Livia Thomaz Noritake
- Ricardo Yugo Suzuki

## 📝 Licença

Este projeto foi desenvolvido como parte da disciplina de Engenharia de Software.

## ⚠️ Status

**Versão:** 1.0.0 (MVP)
**Status:** Em desenvolvimento

### Próximas Etapas:
- [ ] Implementar motor de cálculo (Semana 2)
- [ ] Desenvolver interface Streamlit (Semana 3)
- [ ] Adicionar gráficos (Semana 4)
- [ ] Criar testes de integração (Semana 5)
- [ ] Finalizar documentação (Semana 6)

---

**Última atualização:** Dezembro 2025
