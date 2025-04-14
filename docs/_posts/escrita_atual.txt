---
layout: post
title:  "Investigação Inicial da Especialização de Qwen2.5-Code em Domínio Financeiro: Impacto na Geração de Diagramas de Casos de Uso"
date:   2025-04-08 16:00:00 -0300
categories: [pesquisa, LLM, engenharia-de-software]
tags: [qwen2.5, fine-tuning, especificação-técnica]
author: Helaine Barreiros
---

# Experimento 01: Investigação Inicial da Especialização de Qwen2.5-Code em Domínio Financeiro: Impacto na Geração de Diagramas de Casos de Uso

## 1. Definição do Experimento — GQM (Wohlin et al.)

| ||
|------------------|-------------------------------------|
| **Objetivo (Goal)** | Analisar a **especificação técnica de diagramas de casos de uso gerados por um Large Language Model (LLM)** |
| **Propósito** | Com o propósito de **avaliar a qualidade dos artefatos gerados** |
| **Foco na Qualidade** | Com relação à **articulação entre conhecimento técnico e conhecimento explícito de domínio** |
| **Perspectiva** | Do ponto de vista de **um engenheiro de software em um contexto de trabalho colaborativo** |
| **Contexto** | No contexto da **geração automática de artefatos técnicos com base em instruções textuais sobre um sistema de gerenciamento de finanças pessoais assistido por inteligência artificial (IA)** |
|||

## 2. Perspectivas do Foco de Qualidade

A qualidade da especificação técnica dos diagramas de casos de uso (DCUs) foi avaliada com o foco nas variáveis dependentes, conforme a tabela abaixo:


| **Código** | **Perspectiva**                    | **Descrição**                                                                                                                                                         |
|------------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **FC01**   | Correção Sintática                  | Avalia a conformidade do diagrama com a sintaxe da linguagem PlantUML. Inclui declaração correta dos elementos, ausência de erros e compilação sem falhas.           |
| **FC02**   | Completude Técnica                 | Verifica se o diagrama cobre os elementos mínimos esperados conforme a especificação funcional (nível C1): atores, casos de uso, relacionamentos, pacotes, etc.     |
| **FC03**   | Coerência Semântica com o CED       | Analisa se os nomes, funções e vínculos entre os elementos estão alinhados ao conhecimento explícito de domínio internalizado pelo modelo.                          |
| **FC04**   | Articulação Técnico-Conceitual      | Avalia o diagrama como um todo, considerando clareza estrutural, uso inteligente de abstrações (e.g., `include`, `extend`, herança) e plausibilidade da solução modelada. |

## 3. Desing Experimental

### 3.1 Hipóteses

#### 3.1.1 Correção Sintática (CS)

- **H.CS01**: μ₁_corr = μ₂_corr  
  *A média da correção sintática dos DCUs gerados por LLM especializado é igual à gerada por LLM não especializado.*

- **H1.CS01**: μ₁_corr > μ₂_corr  
  *A média da correção sintática dos DCUs gerados por LLM especializado é superior àquela gerada por LLM não especializado.*

#### 3.1.2 Completude Técnica (CT)

- **H0.CT01**: μ₁_comp = μ₂_comp  
  *A média da completude técnica dos diagramas de casos de uso gerados por LLM especializado em CED é igual àquela gerada por LLM não especializado.*

- **H1.CT01**: μ₁_comp > μ₂_comp  
  *A média da completude técnica dos diagramas de casos de uso gerados por LLM especializado em CED é maior do que a gerada por LLM não especializado.*

#### 3.1.3 Coerência Semântica com o Domínio (CSD)

- **H0.CSD01**: μ₁_coer = μ₂_coer  
  *A média da coerência semântica com o domínio dos diagramas de casos de uso gerados por LLM especializado em CED é igual àquela gerada por LLM não especializado.*

- **H1.CSD02**: μ₁_coer > μ₂_coer  
  *A média da coerência semântica com o domínio dos diagramas de casos de uso gerados por LLM especializado em CED é maior do que a gerada por LLM não especializado.*

#### 3.1.4 Articulação Técnico-Conceitual (ATC)

- **H0.ACT01**: μ₁_artic = μ₂_artic  
  *A média da articulação técnico-conceitual dos diagramas de casos de uso gerados por LLM especializado em CED é igual àquela gerada por LLM não especializado.*

- **H1.ACT01**: μ₁_artic > μ₂_artic  
  *A média da articulação técnico-conceitual dos diagramas de casos de uso gerados por LLM especializado em CED é maior do que a gerada por LLM não especializado.*

**Onde**:

- μ₁_* representa a média da variável * para o grupo com LLM especializado em CED;
- μ₂_* representa a média da variável * para o grupo com LLM não especializado;
- Todas as hipóteses assumem um **delineamento unifatorial com dois tratamentos independentes**: LLM especializado vs. LLM não especializado.


### 3.2 Parâmetros

| **Parâmetro**                   | **Descrição**                                                                                                               |
|--------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **Domínio de Aplicação**        | Sistema de gerenciamento de finanças pessoais assistido por inteligência artificial.                                      |
| **Tipo de Artefato Gerado**     | Diagrama de Casos de Uso (Use Case Diagram).                                                                               |
| **Linguagem de Modelagem**      | PlantUML.                                                                                                                  |
| **Formato de Saída Esperado**   | Código-fonte em PlantUML, utilizado para gerar visualizações e análises estruturadas.                                      |
| **Formato de Entrada**          | Instruções técnicas textuais derivadas da especificação funcional no nível C1 da especificação C4 model.                   |
| **Nível de Modelagem**          | C4 Model — Nível C1 (representação de escopo e responsabilidades de alto nível do sistema).                                |
| **Ambiente de Execução do LLM** | Execução local em servidor pessoal utilizando a plataforma Ollama.                                                         |
| **Modelos Avaliados**           | Dois modelos LLM com arquitetura base equivalente: um especializado em CED e outro não especializado (grupo de controle). |
| **Processo de Avaliação**       | Análise estruturada por especialistas humanos e parsing automatizado do código PlantUML para extração dos componentes.    |


### 3.3 Variáveis

#### 3.3.1 Variável Independente (fator de tratamento)

A variável independente é o nível de especialização do modelo de linguagem LLM em Conhecimento Explícito ed Domínio (CED). O CED foi o fator manipulado para avaliar o impacto na qualidade técica dos diagrams de cassos de uso gerados a partir de instruções técnicas.A variável é do tipo nominal binária com dois tratamentos distintos:
- 1. LLM não especializado: versão do modelo abase sem nenhuma adaptação de conhecimento específico de domínio em dados financeiros
- 2. LLM especializado em CED: versão do mesmo modelo base submetido a um processo de especialização do conhecimento explícito sobre o domínio específico em dados financeiros

A manipulação do fator de tratamento foi feita de forma controlada para isolar o efeito da especialização na geração do diagrama de casos de uso. Na instrumentação buscou-se manter a consistencia de parâmetros passíveis de influenciar a performance dos modelos na geração do diagrama: (i) temperature, (ii) top_p, (iii) context size, (iv) num_predict e (v) stop. Estes parâmetros foram definidos após uma fase exploratória de calibração com o objetivo de garantir que ambos os modelos operassem sob condições comparáveis de geração e com efeitos limitados de variabilidade estocástica do processo de geração dos diagramas. 

#### 3.3.2 Variáveis Dependentes

As variáveis dependentes são as que refletem a **qualidade técnica da especificação dos diagramas de casos de uso (DCUs)** gerados pode modelos LLM com e sem especialização em Conhecimento Explícito de Domínio (CED). A avaliação foi realizada a partir da análise técnica estruturada dos componentnes do diagrama: atores, casos de uso, relacionamentos e pacotes. Na tabela a seguir é possível observar as variaveis dependentes organizadas por compoente e contemplando quatro dimensões principais de qualidade.

**Tabela Variáveis 01: Variáveis de Avaliação de Diagramas PlantUML**

| Variável Dependente | Descrição |
|---------------------|-----------|
| **1. Correção Sintática** | Grau de conformidade do diagrama à sintaxe da linguagem PlantUML, considerando os elementos individuais. |
| **2. Completude Técnica** | Verifica se o diagrama cobre todos os elementos esperados com base na especificação funcional do sistema. |
| **3. Coerência Semântica com o CED** | Avalia se os nomes, funções e vínculos dos elementos estão alinhados com o conhecimento específico de domínio. |
| **4. Articulação Técnico-Conceitual** | Analisa o diagrama como um todo, observando clareza estrutural, uso inteligente de abstrações e reuso. |

*Variáveis 01 - Métricas para avaliação qualitativa de diagramas técnicos.*

##### **3.3.1 Correção sintática (CS)**

Avaliou a conformidade sintática do diagrama e de seus compoentes, referenciando a sintaxe estabelecina na linguagem PlantUML. Foi mensurada através da análise dos itens CS01, CS03 e CS03:

- **CS01:** Validação automática (diagrama compila e gera imagem);
- **CS02:** Correção de declaração de elementos (actor, usecase, -->, package);
- **CS03:** Ausência de elementos desconectados ou mal declarados.

##### **3.3.2 Completude técnica (CT)**

Avaliou se os componentes fundamentais à especificação do diagrama de casos de uso estão presentes e conectados adequadamente. Foi mensurado através da análise os itens CT01, CT02, CT03 e CT04.

- **CT01:** Mínimo de atores e casos de uso esperados observando o escopo funcional;
- **CT02:** Atores conectados a pelo menos um caso de uso ou ator;
- **CT03:** Casos de uso vinculados e referenciados;
- **CT04** Uso de pacotes e notas explicativas quando apropriado.

##### **3.3.3 Coerência Semântica com o CED (CS-CED)**

Avaliou a consistência conceitual dos componentes do diagrama de acordo com o conhecimento explícito do domínio modelado. Foi mensurado analisando :

- **CS01:** Nomeações técnicas corretas (ex: “Cliente PJ” em vez de “Pessoa”);
- **CS02:** Função coerente dos elementos (ex: “Negociar conteúdo” faz parte de um protocolo HTTP);
- **CS03:** Relacionamentos coerentes com os papéis funcionais do sistema.

##### **3.3.4 Articulação Técnico-Conceitual (ATC)**

Avaliou globalmente o diagrama e buscou avaliar:

- **ATC01:** Clareza estrutural do conjunto;
- **ATC02:** Uso inteligente de composição (include, extend, herança);
- **ATC03:** Modularização por pacotes;
- **ATC04:** Grau de reaproveitamento sem redundância;


### 3.4 Design do experimento

O experimento adotou um delineamento **unifatorial com dois tratamentos independentes** e foi estruturado com um **desenho entre sujeitos** (*between-subjects design*). O fator experimental que foi manipulado é a **especialização do modelo de linguagem (LLM) em Conhecimento Explícito de Domínio (CED)** em dois níveis:

- **LLM não especializado** em CED (grupo controle);
- **LLM especializado** em CED (grupo experimental).

No delineamento entre sujeitos, cada participante (avaliador especialista) foi alocado a um único grupo. Assim houve exposição dos sujeitos apenas a um dos grupos de artefatos gerados por cada um dos dois modelos. Essa estratégia buscou  mitigar: (i) potenciais efeitos de aprendizagem cruzada preservar, (ii) viés de comparação entre tratamentos e (iii) sobrecarga cognitiva.

A tabela abaixo apresenta a distribuição dos trtamentos entre os grupos experimentais.

| **Grupo** | **LLM Avaliado**               | **Número de Diagramas** | **Avaliadores Alocados**     |
|-----------|--------------------------------|--------------------------|-------------------------------|
| G1        | LLM **não especializado**      | *n* diagramas            | Especialistas A, B, C         |
| G2        | LLM **especializado em CED**   | *n* diagramas            | Especialistas D, E, F         |


### 3.5 Participantes (sujeitos)

São avaliadores humanos, especialistas em Engenharia de Software que atuam como juízes na avaliação da qualidade técnica de Diagramas de Casos de Uso gerados por modelos LLM. A amostragem foi intencional por conveniência, considerando siponibilidade e critérios explícitos de qualificação técnica:
- Experiência comprovada em modelagem de software
- Familiaridade com a notação UML na linguagem PlantUML
- COnhecimento técnico proficiente, superior a 5 anos em análise e design de software

Os participantes foram selecionados entre docentes da área de Engenharia de Software, profissionais atuantes em arquiteura e modelagem de software e avaliadores convidados com expertise comprovada na especificação e interpretação de modelos técnicos.

O experimento contou com quatro avaliadores, definidos com base na disponibilidade dos especialistas e no tempo necessário para avaliação de cada artefato. Embora o número seja restrito a expertise dos participantes e o uso de instrumentos estruturados de avaliação sustentam a validade interna da análise. O COnhecimento prévio sobre o domínio do sistema modelado foi mitigado pela entrega de material introdutório padronizado e disponibilização de modelagem do sistema no Modelo C4, a todos os avaliadores no momento do aceite do convite. A participação foi voluntária e não remunerada, os participantes aceitaram contribuir como parte de uma rede de colaboração científica para o avanço da engenharia de software. 


| ID do Participante | Perfil Profissional                               | Experiência em Modelagem | Familiaridade com UML/PlantUML | Conhecimento prévio no domínio | Treinamento introdutório recebido | Participação voluntária | Incentivo recebido |
|--------------------|---------------------------------------------------|---------------------------|-------------------------------|----------------------------------|----------------------------------|--------------------------|--------------------|
| P1                 | Professor de Engenharia de Software               | Alta                      | Sim                           | Não                              | Sim                              | Sim                      | Nenhum             |
| P2                 | Profissional atuante em arquitetura de software   | Alta                      | Sim                           | Não                              | Sim                              | Sim                      | Nenhum             |
| P3                 | Avaliador convidado com expertise comprovada      | Média                     | Sim                           | Não                              | Sim                              | Sim                      | Nenhum             |
| P4                 | Professor de Engenharia de Software               | Alta                      | Sim                           | Não                              | Sim                              | Sim                      | Nenhum             |


### 3.6 Objetos

Os objetos do experimento são diagramas de casos de uso escritos na linguagem plantuml, gerados automaticamente por LLMs na partir de uma mesmo conjunto de instruções técnicas. 

Cada objeto representa uma instância de Diagrama de Casos de Uso referente ao Sistema de Gerenciamento de Finanás Pessoais assitido por Inteligência Artificial, com escopo definido pela especificação de nível C1 no modelo C4.

A avaliação dos objetos mensura a qualidade da especificação técnica dos diagramas considerando quatro perspectiva: (i) correção sintática, (ii) completude técnica, (iii) coerência semântica com o domínio e articulação técnico-conceitual.

| **Característica**                       | **Descrição**                                                                                     |
|-----------------------------------------|---------------------------------------------------------------------------------------------------|
| **Origem dos objetos**                  | Artefatos gerados automaticamente por LLMs com base em uma mesma instrução técnica textual.       |
| **Tratamentos associados**              | Cada artefato é gerado por um dos dois modelos experimentais: (1) LLM não especializado (controle); (2) LLM especializado em CED (tratamento). |
| **Formato dos objetos**                 | Código-fonte textual em PlantUML, estruturado conforme a documentação oficial da linguagem.        |
| **Complexidade dos artefatos**          | Definida com base em uma única especificação funcional do sistema (nível C1).                     |
| **Número de artefatos**                 | Cada grupo experimental (controle e tratamento) é composto por um conjunto balanceado de artefatos. |
| **Tamanho e estrutura dos artefatos**   | Variável conforme a resposta do modelo, mas sempre contendo atores, casos de uso e relacionamentos. |
| **Instrumentação associada**            | O código PlantUML é analisado automaticamente para extrair os elementos estruturais do diagrama.  |
| **Papel no experimento**                | Cada participante avalia os artefatos de apenas um grupo (tratamento ou controle) com base nas variáveis dependentes. |


### 3.7 Instrumentação 

A instrumentação do experimento foi feita utilizando um conjunto articulado de componentes automatizados, arquivos de apoio e ferramentas de controle. Buscou controlar o impacto na qualidade dos dados coletados e na estruturação da avaliação realizada pelos participantes. Os instrumentos são apresentados, organizados em quatro eixos: (1) ambiente de geração controlada, (2) instrumentos de medição, (3) instrumentos avaliação e (4) diretrizes aos participantes.

#### 3.7.1 Eixo 1: Ambiente de geração controlado

Os modelos LLM foram executados em ambiente isolado e controlado, utilizando a plataforma Ollama instalada em um servidor local dedicado. A configuração buscou preservar a validade interna do experimento, mitigando o impacto de parâmetros dos modelos na capacidade de gerar respostas para a tarefa desejada no experimento. 

O processo de calibração foi exploratório, e analisou o impacto de diferentes combinações de temperatura (0 a 2) e top_p (0.8 a 1.0) que permitissem o envio de instruções estruturadas usadas no experimento para guiar o modelo a ser capaz de gerar diagramas de casos de uso. O objetivo foi encontrar os valores mínimos viáveis de criatividade de forma equilibrada para cada um dos modelos, no contexto do experimento, que permitissem:

1. Visto que o modelo base dos LLMs é comprovadamente capaz de gerar diagramas na linguagem PlantUML, buscamos observar se a configuração do modelo permitia a geração de diagramas sintaticamente válidos (que compilam e geram imagens) observando um percentual de ao menos 60% das amostras desejadas;
2. A recepção do conteúdo completo da instrução pelo modelo, incluindo a especificação funcional textual do nível C1;
3. A mitigação do efeito de alucinações graves ou incoerências estruturais, mediante a configuração do modelo, que inviabilizassem a coleta de dados e análise do diagrmas gerados pelos modelos.

A tabela abaixo apresenta a configuração foi aplicada de forma idêntica nos dois modelos LLM e os tratamentos foram aplicados sequencialmente, um por vez a cada coleta.

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `temperature` | 0.4 | Minimiza aleatoriedade mantendo capacidade mínima de recombinação. |
| `top_p` | 0.8 | Balanceia criatividade e consistência no nível do conteúdo esperado. |
| `num_ctx` | 131072 | Garante capacidade de processamento das instruções completas (nível C1). |
| `num_predict` | 1024 | Suficiente para gerar um código PlantUML completo, conforme diagrama de referência. |
| `repeat_penalty` | 1.2 | Evita redundância excessiva nas respostas. |
| `stop` | `<im_end` | |


#### 3.7.2 Eixo 2: Instrumentos de medição automatizados

Foi desenvolvido um programa na liguagem Python para realizar a coleta automática dos diagramas de casos de uso dos LLMs. A aplicação e conecta diretamente ao servidor que hospeda o Ollama e cria para cada coleta :

1. arquivo **.txt** contendo a resposta completa do modelo;
2. arquivo **.puml** com o código PlantUML extraído da resposta do LLM que está entre entre as tags @startuml e @enduml;
3. arquivo **.png** gerado pelo servidor local PlantUML, a partir do código .puml;
4. arquivo **.xlsx** com relatório estruturado dos componentes extraídos automaticamente do código (atores, casos de uso, relacionamentos, notas, pacotes etc.), de acordo com a especificação da linguagem PlantUML.

O arquivo *.xlsx* também contém uma aba específica com o instrumento de avaliação estruturado utilizado pelos participantes. Durante a coleta todos os artefatos são organizados e versionados em diretórios e com nomes de arquivos que codificam os metadados da coleta (modelo, data, hora, parâmetros, número da amostra, etc.). Posteriormente os arquivos são enviados para o repositório GitHub.

#### 3.7.3 Eixo 3: Instrumentos de avaliação

Foi desenvolvido um **instrumento sistemático para julgamento da qualidade técnica dos diagramas de casos de uso** baseado nos escores obtidos para cada uma das variáveis dependentes (ver Seção 3.1). O instrumento assistiu a **transformação dos escores técnicos avaliados por especialistas** em uma medida consolidada de **qualidade técnica útil do artefato (QTA)** observando o potencial de uso do artefato por engenheiros de software em contextos colaborativos. O objetivo foi **determinar uma medida de utilidade prática do artefato gerado pelo LLM**, considerando o esforço necessário do engenheiro de software para refinar, corrigir ou reespecificar o diagrama.

##### **3.7.3.1 Instrumento de avaliação**

O instrumento guiou o preenchimento e análise

---
###### **Componente: Ator**
---
| **Critério Avaliado** | **Variável Dependente** | **Tipo de Métrica** | **Identificado** | **Esperado** | **Linha no** `.puml` | **Observações** |
|------------------------|--------------------------|----------------------|-------------------|---------------|----------------------|------------------|
| Uso correto da notação `actor` | Correção Sintática | Binária | Sim | Sim | 3–4 | Correto |
| Quantidade de atores declarados | Completude Técnica | Numérico | 2 | ≥ 2 | 3–4 | Quantidade adequada |
| Todos os atores conectados a pelo menos um caso de uso | Completude Técnica | Binária | Sim | Sim | 49–52, 55–73 | Conexões completas |
| Representam entidades reais do domínio | Coerência com o CED | Ordinal | 5 | 5 | 3–4 | Alinhados ao domínio HTTP |
| Nomeação técnica e semântica apropriada | Coerência com o CED | Ordinal | 5 | 5 | 3–4 | Terminologia específica |
| Uso de especialização entre atores | Completude Técnica (extra) | Binária | Não | Sim (desejável) | — | Oportunidade de especialização |

**Totais - Atores**

| Variável                        | Pontuação |
|--------------------------------|-----------|
| Correção Sintática             | 1 / 1     |
| Completude Técnica             | 2 / 2     |
| Coerência com o CED            | 10 / 10   |

---
###### Componente: Casos de Uso
---


| **Critério Avaliado**                                                                                  | **Variável Dependente**     | **Tipo de Métrica** | **Identificado** | **Esperado** | **Linha no `.puml`** | **Observações**                                               |
|--------------------------------------------------------------------------------------------------------|------------------------------|----------------------|-------------------|----------------|----------------------|---------------------------------------------------------------|
| Uso correto da notação `usecase`                                                                        | Correção Sintática           | Binária              | Sim               | Sim            | 7–28                 | Sintaxe válida                                                  |
| Quantidade de casos de uso                                                                              | Completude Técnica           | Numérico             | 18                | ~20            | 7–28                 | Volume adequado com certa redundância                         |
| Todos conectados a atores                                                                               | Completude Técnica           | Binária              | Sim               | Sim            | 49–73                | Conexões completas                                              |
| Clareza semântica e alinhamento ao domínio                                                              | Coerência com o CED          | Ordinal              | 4                 | 5              | 7–28                 | Alguns nomes prolixos ou redundantes                          |
| Uso de composição (`include`, `extend`, herança)                                                        | Articulação Técnico-Conceitual | Binária (extra)    | Não               | Sim            | —                    | Oportunidade de abstração não explorada                       |

---
###### Componente: Relacionamentos
---

| **Critério Avaliado**                                                                                  | **Variável Dependente**     | **Tipo de Métrica** | **Identificado** | **Esperado** | **Linha no `.puml`** | **Observações**                          |
|--------------------------------------------------------------------------------------------------------|------------------------------|----------------------|-------------------|----------------|----------------------|------------------------------------------|
| Uso correto de setas e conectores (`-->`, etc.)                                                        | Correção Sintática           | Binária              | Sim               | Sim            | 49–73                | Correto                                  |
| Todos os elementos conectados                                                                          | Completude Técnica           | Binária              | Sim               | Sim            | 49–73                | Nenhum elemento isolado                  |
| Direcionalidade técnica adequada                                                                       | Correção Técnica             | Ordinal              | 5                 | 5              | 49–73                | Todos os fluxos coerentes                |
| Relações fazem sentido no contexto do domínio                                                          | Coerência com o CED          | Ordinal              | 4                 | 5              | 49–73                | Ligeiramente repetitivo                  |

---
###### Componente: Organização / Modularização
---

| **Critério Avaliado**                                                                                  | **Variável Dependente**     | **Tipo de Métrica** | **Identificado** | **Esperado** | **Linha no `.puml`** | **Observações**                                |
|--------------------------------------------------------------------------------------------------------|------------------------------|----------------------|-------------------|----------------|----------------------|------------------------------------------------|
| Uso de bloco `rectangle {}` como delimitação de sistema                                                | Correção Sintática           | Binária              | Sim               | Sim            | 6–28                 | Correto                                       |
| Agrupamento funcional coerente                                                                          | Coerência com o CED          | Ordinal              | 4                 | 5              | 6–28                 | Poderia haver divisão entre camadas ou aspectos |
| Nomeação do pacote condizente com o escopo do domínio                                                  | Coerência com o CED          | Ordinal              | 5                 | 5              | Linha 6              | "Sistema de Comunicação HTTP" é adequado        |

---
 ###### Diagrama completo
---

| **Critério Avaliado**                                                                                  | **Variável Dependente**            | **Tipo de Métrica** | **Identificado** | **Esperado** | **Linha no `.puml`** | **Observações**                                              |
|--------------------------------------------------------------------------------------------------------|------------------------------------|----------------------|-------------------|----------------|----------------------|--------------------------------------------------------------|
| Estrutura geral lógica e coesa                                                                          | Articulação Técnico-Conceitual     | Ordinal              | 4                 | 5              | Global               | Diagrama compreensível, porém extenso                        |
| Uso de abstrações de modelagem (`include`, `extend`, herança)                                          | Articulação Técnico-Conceitual     | Binária              | Não               | Sim            | —                    | Oportunidade não explorada para redução de redundância       |
| Viabilidade da modelagem como base para implementação                                                   | Articulação Técnico-Conceitual     | Ordinal              | 4                 | 5              | Global               | Coerente, mas excessivamente verborrágico                    |
| Integração entre aspectos técnicos e conceituais                                                        | Articulação Técnico-Conceitual     | Ordinal              | 3                 | 5              | Global               | Diagrama demonstra intenção correta, mas sem sofisticação    |

##### **3.7.3.2 Escala de interpretação**

A escala para interpretação da pontuação consolidada dos artefatos é apresentada na tabela abaixo:

| **Faixa de Pontuação (% do total possível)** | **Classificação** | **Interpretação Técnica**                                                                 | **Decisão do Engenheiro**                     |
|---------------------------------------------|--------------------|-------------------------------------------------------------------------------------------|-----------------------------------------------|
| **≥ 80%**                                    | Excelente           | O artefato é tecnicamente sólido e semanticamente adequado.                              | Usável com mínima ou nenhuma edição.          |
| **60% a < 80%**                              | Bom                 | Artefato tecnicamente coerente, requer apenas ajustes localizados.                       | Usável com edição moderada.                   |
| **50% a < 60%**                              | Razoável            | Artefato parcialmente útil, mas com lacunas significativas.                              | Usável com edição significativa.              |
| **30% a < 50%**                              | Fraco               | Exige retrabalho estrutural ou semântico extenso.                                         | Pouco valor prático.                          |
| **< 30%**                                     | Inutilizável        | Artefato inconsistente ou irrelevante para o domínio.                                     | Requer substituição completa.                 |


A construção foi realizada com base nos seguintes princípios empíricos: 

1. **Esforço evitado e critério mínimo de retrabalho:** Ferramentas de suporte à geração de artefatos devem ser avaliadas em função do esforço manual que evitam (Wohlin et al). Um diagrama de casos de uso que exige reescrita significativa acima de 50% perde sua efetividade como ferramenta de apoio (Kitchenham et al. [2002]). 
   
2. **Benefício do aproveitamento:** Artefatos parcialmente completos podem ser úteis ao engenheiro de software.Diagramas de caso de usos tecnicamente válidos e semanticamente adequados, mesmo que parcialemnte completos, podem ser úteis (*partial automation benefit*).

Por exemplo, para um diagrama de casos de uso que recebe um  escore total de 50 em 60 pontos, ou seja 83%, tem a classificação atribuída como **“Excelente”**, indicando que o engenheiro pode **utilizar o artefato com pouca edição** para apoiar atividades de análise ou projeto.

#### 3.7.4 Eixo 4: Diretrizes aos participantes.

  - introdução ao domínio do sistema modelado (finanças pessoais com IA);
  - modelagem técnica do sistema no modelo C4 nos níveis C1, C2 e C3 
  - exemplos ilustrativos do preenchimento do instrumento;
  - explicação dos critérios de avaliação (completude, correção sintática, coerência com o domínio, articulação técnico-conceitual);
  - procedimento de acesso aos arquivos e preenchimento das planilhas.

#### 3.7.5: Instrumento de coleta

<<Falar do sistema de coleta>>


### 3.8 Procedimento de coleta de dados
O procedimento de coleta dos dados foi dividido em duas etapas principais: (1) coleta automática dos artefatos gerados pelos modelos LLM e (2) coleta manual dos dados para validação e preparação dos artefatos a serem avaliados pelos participantes.

#### 3.8.1 Etapa 1 — Coleta Automática
A coleta automática foi conduzida por uma aplicação Python desenvolvida especificamente para o experimento, e executada em um servidor dedicado que hospeda a plataforma Ollama, responsável por executar localmente os modelos LLM. O processo foi realizado nesta sequência:

1. Criação de uma pasta dedicada para a coleta, no diretório definido na parametrização do sistema.
2. Envio das instruções técnicas ao modelo LLM via API local do servidor Ollama.
3. Recebimento da resposta textual do LLM, que é registrada com metadados descritivos: status da geração (sucesso ou falha), tipo de parada, número de tokens gerados, e parâmetros utilizados (temperatura e top_p).
4. Extração do código PlantUML contido entre as tags @startuml e @enduml, e salvamento do conteúdo em um arquivo .puml.
5. Geração da imagem visual do diagrama, utilizando um servidor PlantUML local, com base no código .puml extraído.
6. Análise sintática automática do código .puml, extraindo seus componentes estruturais (atores, casos de uso, relacionamentos, pacotes, notas, etc.) conforme a especificação oficial da linguagem PlantUML.
7. Geração do relatório estruturado em formato .xlsx, que inclui os elementos detectados e incorpora o instrumento de avaliação a ser usado pelos participantes.

* Todos os arquivos gerados (resposta textual, código .puml, imagem do diagrama e relatório .xlsx) são nomeados e organizados com base em metadados que identificam: modelo utilizado, número da coleta, data, hora, parâmetros aplicados (temperatura e top_p) e tempo total de execução. 
* O número de coletas realizadas por modelo é parametrizado e os tratamentos (LLM especializado e não especializado) são aplicados sequencialmente a cada iteração de coleta.

#### 3.8.2 Etapa 2 — Coleta Manual
A etapa manual foi conduzida por um pesquisador especialista em Engenharia de Software e modelagem com PlantUML, e inspecionou a integridade das coletas analisando:

1. Arquivo de texto contendo a resposta do LLM;
2. Arquivo .puml contendo o código do diagrama;
3. Imagem do diagrama gerada automaticamente;
4. Arquivo .xlsx com o relatório de componentes extraídos e o instrumento de coleta.

Durante a inspeção foi feita a validação cruzada entre o código .puml, a imagem gerada e o relatório de componentes com o instrumento de coleta. No caso de inconsistências serem identificadas o pesquisador realiza a correção para garantir as evidências geradas pelos LLMs. Todos os artefatos validados são versionados e armazenados em um repositório GitHub, garantindo rastreabilidade e acesso para fins de avaliação.

#### 3.8.3 Etapa 3 — Coleta da Avaliação dos Participantes

Após receber a autorização para coleta, os participantes realizaram a avaliação em sessões isoladas e padronizadas em duração, com acesso integral a todos os artefatos da coleta. Cada um deles foi orientado a utilizar a aba de instrumentação presente no relatório .xlsx para o registro de avaliação estruturada, seguindo os critérios das variáveis dependentes do experimento. Ao final de cada sessão de avaliação, os arquivos foram salvos novamente no repositório GitHub, contendo os dados coletados da análise.

#### 3.8.4  Representacao visual da coleta de dados
┌────────────────────────────────────────────────────────────────────┐
│                   ETAPA 1 — COLETA AUTOMÁTICA                      │
└────────────────────────────────────────────────────────────────────┘

          Entrada: Instruções técnicas textuais
                        ↓
        ┌──────────────────────────────────────┐
        │ [1] Criação de pasta de coleta       │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [2] Envio da instrução ao LLM via    │
        │     servidor Ollama                  │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [3] Recebimento da resposta textual  │
        │     + metadados                      │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [4] Extração do código @startuml     │
        │     e salvamento como .puml          │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [5] Geração da imagem via servidor   │
        │     PlantUML                         │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [6] Parsing do código .puml          │
        │     e extração de componentes        │
        └──────────────────────────────────────┘
                        ↓
        ┌──────────────────────────────────────┐
        │ [7] Geração do relatório .xlsx       │
        │     com componentes + instrumento    │
        └──────────────────────────────────────┘
                        ↓
       Saída: 
       ┌ resposta.txt
       ├ diagrama.puml
       ├ diagrama.png
       └ relatorio_componentes.xlsx

┌────────────────────────────────────────────────────────────────────┐
│                   ETAPA 2 — COLETA MANUAL                          │
└────────────────────────────────────────────────────────────────────┘

              Entrada: artefatos da etapa 1
                        ↓
        ┌────────────────────────────────────────────┐
        │ [1] Verificação da integridade dos arquivos│
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [2] Validação cruzada:                     │
        │     .puml ↔ imagem ↔ relatório .xlsx        │
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [3] Correções manuais (se necessárias)     │
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [4] Armazenamento dos artefatos no GitHub  │
        └────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│           ETAPA 3 — AVALIAÇÃO DOS PARTICIPANTES                   │
└────────────────────────────────────────────────────────────────────┘

 Entrada: artefatos validados armazenados no GitHub
                        ↓
        ┌────────────────────────────────────────────┐
        │ [0] Autorização e início da sessão         │
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [1] Participante acessa:                   │
        │     - resposta.txt                         │
        │     - .puml                                │
        │     - imagem                               │
        │     - relatorio_componentes.xlsx           │
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [2] Preenchimento da aba do instrumento    │
        │     dentro do .xlsx                        │
        └────────────────────────────────────────────┘
                        ↓
        ┌────────────────────────────────────────────┐
        │ [3] Salvamento da avaliação no GitHub      │
        └────────────────────────────────────────────┘

Notas:
- Todas as sessões de avaliação foram realizadas de forma isolada e com duração padronizada.
- Cada participante teve acesso completo aos artefatos da coleta.


### 3.9. Procedimentos de análise

A análise de dados foi planejada para verificar a existência de diferenças significativas entre LLm especializado e LLM não especializado em conhecimento explícito (grupos experimentais) em relação às variáveis dependentes CS, CT, CS-CED e ATC (seção 3.3.2) (Wohlin et al. [1], Jedlitschka et al. [2] e Kitchenham et al. [3]). A análise também contemplou a classificação da utilidade prática dos artefatos gerados.

#### 3.9.1 Análise descritiva

Para cada uma das variáveis dependentes foi realizada uma análise descritiva inicial apresentando (i) média, (ii) mediana, (iii) desvio padrão e (iv) valores mínimo e máximo. O intuito foi caracterizar o comportamento dos dados em cada grupo experimental

#### 3.9.2 Verificação de normalidade

Antes da aplicação dos testes de hipótese foi realizado o teste Shapiro-Wilk [4] para analisar a normalidade nos dados. O teste foi escolhido pela sua habilidade lidar com amostras pequenas e médias (Wohlin et al. [1]).

#### 3.9.3 Testes de Hipóteses

A comparação das médias dos escores obtidos para cada variável dependente considerou o delineamento entre os sujeitos em dois grupos independente. Considerando a anormalidade dos dados foi aplicado o teste de Mann-Witney U [1][4] com significância α = 0,05.

+> se for normal (teste t de Student para amostras independentes [1])

#### 3.9.4 Análise da Escala de Qualidade Técnica Útil (QTA)

Para cada diagrama de caso de uso avaliado foi calculado o percentual de pontuação obtido em relação ao valor máximo possível:

$QTA\% = \frac{Pontuação\ Obtida}{Pontuação\ Máxima} \times 100$

A classificação do diagrama foi realizado conforme a escala proposta na seção 7.2 considerando o prncípio do esforço evitado (Avoid Effort Principle) e o benefício de automação parcial (partial automation benefit) Kitchenham et al. [3] e Wohlin et al. [1],. A distribuição dos artefatos em cada nível da escala QTA foi analisada através da contagem absoluta e percentual dos diagramas avaliados.

#### 3.9.5 Teste de Associação para a Escala QTA

Para verificar se existir associação entre o grupo experimental entre LLM espcializados e LLM não especializado e a classificação dos artefatos na Escala QTA, foi aplicado o teste Qui-Quadrado de Person (4) para variáveis categóricas.

#### 3.9.6 Controle de variáveis externas

O experimento buscou mitigar eventuais viéses dos avaliadores que podoeriam influenciar a validade interna do experimento utilizando a seguinte abordagem( Kitchenham et al. [3]):

1. Controlando o efeito de aprendizado dos avaliadores com o delineamento entre sujeitos
2. Alocando os avaliadores balanceando a experiência em modelagem de software
3. Padronizando as instruções e artefatos utilizados pelos avaliadores


[1] C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and A. Wesslén, Experimentation in Software Engineering. Springer Science & Business Media, 2012.

[2] A. Jedlitschka, M. Ciolkowski, and D. Pfahl, “Reporting experiments in software engineering,” Empirical Software Engineering, vol. 13, no. 1, pp. 97–135, 2008.

[3] B. Kitchenham, S. Linkman, and D. Law, “Desmet’s methodology for evaluating software engineering methods and tools: a replicated experiment,” Empirical Software Engineering, vol. 7, no. 3, pp. 193–223, 2002.

[4] A. Field, Discovering Statistics Using IBM SPSS Statistics. Sage, 2017.






### 3.10. Avaliação da Validade

#### 3.10.1 Confiabilidade dos dados

Pra reduzir a influência de falhas humanas, trazer consistência na identificação dos componentes do diagrama e minimizar viéses de análise a coleta de dados do experumento foi automatizada através do desenvolvimento de uma aplicação. Desenvolvida em Python, a ferramenta realiza o parsing do código PlantUML gerado pelo LLM. O parser foi responsável por extrair os componentes dos diagramas e registrá-los em um relatório estruturado no formato xlsx.

Para mitigar qualquer inconsistência na identificação dos compontes foi implementado um processo de verificação manual dos dados extraídos pela ferramenta. O processo foi conduzido e revisado com conferência cruzada por dois pesquisadores especialista em modelagem de software em UML na linguagem PlantUML. No processo foram observadas quaisquer inconsistências e tomadas ações de correção manual para manter a acurácia da informação analisada.


#### 3.10.2 Viabilidade dos Materiais e Instrumentos

O instrumento de avaliação considerou a análise individual e conjunta de todos os componentes relevantes para a pesquisa observando a adequação à prática da engenharia de software assistida por LLMs. Também houve a preocupação de incentivar os participantes a registrar observações e justificativas que pudessem contribuir com o processo avaliativo ( (Jedlitschka et al., 2008).). Na construção do instrumento também foi pensada a proximidade entre a descrição do componente e sua localização no código `.puml` para reduzir a dispersão e riscos de erros do avaliador (Wohlin et al., 2012). 

#### 3.10.2 Treinamento dos avaliadores

Foi realizado um treinamento dos participantes baseado em exemplos práticos, para uniformizar a compreensão acerca do experimento, coleta e critérios de avaliação. Para mitigar viéses e transferência de conhecimento relativo ao domínio do sistema usado como modelo para o experimento o treinamento foi realizado utilizando exemplos em um dínio neutro: o protocolo HTTP. Durante o treinamento foram apresentados:

1. Nivelamento acerca do Modelo C4, sua estrutura, níveis e suporte ao processo de construção/modelagem de sistemas
2. Modelagem do nível C1 e sua relação com os requisitos funcionais, não funcionais e com a modelagem de diagramas de casos de uso
3. Detalhamento dos componentes do diagrama de casos de uso analisados pelo estudo
4. Apresentação dos dois modelos LLM utilizados na pesquisa
5. Apresentação do prompt eviado aos LLMs
6. Apresentação do diagrama de casos de uso referência, com o mínimo esperado para o diagrama produzido pelo LLM considerando as instruções e informações entregues
7. Discussões de um diagrama com deficiências técnicas e conceituais de diagramas de casos de uso
8. Discussões sobre critérios que caracterizam a qualidade técnica e semântica de um diagrama de casos de uso
9. Exemplo prático de aplicação do instrumento de avaliação com base no diagrama exemplo de deficiências técnicas e conceituais.
10. Orientações explícitas sobre o preenchimento e registro das avaliações.

#### 3.10.3 Controle e rastreabilidade dos dados

Todos os artefatos gerados no experimento foram organizados e versionados no GitHub usanddo nomenclatura padronizada e incluindo metadaos que indicam o modelo utilizado, data, hora, número da coleta e parâmetros de execução.


\bibitem{b1} C. Wohlin, P. Runeson, M. Höst, M. C. Ohlsson, B. Regnell, and A. Wesslén, Experimentation in Software Engineering. Springer Science & Business Media, 2012.

\bibitem{b2} A. Jedlitschka, M. Ciolkowski, and D. Pfahl, Reporting Guidelines for Controlled Experiments in Software Engineering, in Empirical Software Engineering, vol. 13, pp. 97–135, 2008.

\bibitem{b3} N. Juristo and A. Moreno, Basics of Software Engineering Experimentation. Springer Science & Business Media, 2001.

## 6. Execução

### 6 Amostragem

#### 6.1 Amostragem dos Participantes

Os participantes foram selecionados intencionalmente por conveniência utilizando a qualificação técnica como critério. A estratégia de amostragem buscou encontrar participantes que tivessem vivência prática e teórica que permitisse, avaliar e fundamentar criticamente os artefatos gerados pelos modelos LLM. Assim na seleção foi observado o conhecimento e experiência prática dos participantes em modelagem de software com as linguagens UML e PlantUML. O convite foi voluntário, sem qualquer incentivo financeiro ou material efrito em rede de colaboração científica e de pesquisa aplicada em ambientes empresariais.

Foi possível selecionar oito participantes candidatos, respeitando a disponibilidade dos especialistas e considerando o tempo demandado para o treinamento e avaliação de cada diagrama. Entretanto, mediante a impossibilidade de participação de um dos participantes, o treinamento e a execução do experimento prosseguiu com dois grupos de três especialistas. Apesar de ser sempre desejável um número maior de participantes, o número de participantes da pesquisa está em consonância com o cenário de estudos em Engenharia de Software que exigem análise qualitativa e de profundidade analítica de especialistas (Wohlin et al., 2012).

#### 6.2 Amostragem dos Diagramas de Caos de Uso

O número de amostras dos diagramas de casos de uso do experimento foi definida analisando critérios metodológicos clássicos da Engenharia de Software, estatísticos e particularidades dos mecanismos estocásticos dos  LLMs. Os diagramas analisados no experimento foram produzidos como respostas dos modelos LLMs a uma mesma instrução técnica textual dericada da especificação funcional (nível C1) do sistema em estudo. A quantidade de amostras coletadas por grupo experimental (LLM especializado e LLM não especializado) foi fundamentada observando o Teorema do Limite Central (TLC), natureza estocástica dos LLMs e viabilidade prática da avaliação humana.

##### **Critério 1: Teorema do Limite Central (TLC)**
---

O Teorema do Limite Central é um critério amplamente adotado em esperimentos controlados em Engenharia de software. É orientado se tenha ao menos o número mínimo de trinta amostras (n>=30) que a distribuição de uma população tenda a normalidade, independente da distribuição original da população (Kitchenham et al., 2002; Wohlin et al., 2012).

##### **Critério 2: Natureza Estocástica dos LLMs**
---

LLMs apresentam comportamento estocástico instrísceco e também de seus hiperparâmetros de execução (ex: `temperature` e `top_p`) e variam suas respostas mesmo que expostos ao mesmo prompt  (Brown et al., 2020).No contexto de Engenharia de Software, a geração de artefatos técnicos como diagramas UML demanda um equilíbrio delicado entre criatividade, consistência técnica e aderência ao domínio. Até o momento são escasos os estudos que guiem metdologico ou experimentalmente definindo o número adequado de amostras para avaliar a confiabilidade das respostas dos LLMs neste contexto específico.

##### **Critério 3: Natureza Estocástica dos LLMs**
---

O sistema de coleta automatizada tornou possível um alto volume de coletas, o que é positivo do ponto de vista da robustez estatística. Entretanto a avaliação manual detalhada dos diagramas coletados se contrapõe à limitação da capacidade humana dos participantes disponíveis para a experimentação. 

##### **Critério 4: Viabilidade de uso de LLMs em cenário prático**

Um modelo que exige um número elevado de iterações ou refinamentos sucessivos para gerar um artefato compromete significativamente sua adoção prática. Embora 30 coletas seja adequado do ponto de vista estatístico é considerado elevado do ponto de vista da experiência prática de uso de modelos para assitir o trabalho prático de um engenheiro de software. Realizar dezenas de interações com o LLM pra obter um artefato específico seria inviável ou desestimulante.

\bibitem{b1} C. Wohlin, et al., Experimentation in Software Engineering. Springer, 2012.
\bibitem{b2} B. Kitchenham, et al., Desmet’s methodology for evaluating software engineering methods and tools. Empirical Software Engineering, 2002.
\bibitem{b3} A. Jedlitschka, et al., Reporting Guidelines for Controlled Experiments in Software Engineering. Empirical Software Engineering, 2008.
\bibitem{b4} T. Brown, et al., Language Models are Few-Shot Learners. NeurIPS, 2020.

#### 6.2 Amostragem dos LLMs avaliados

Considerando que atividades na Engenharia de Software exigem raciocínio estruturado e aplicação de conhecimento expl;icito do domínio de negócio, buscou-se selecionar modelos capazes de representar adequadamente este fator experimental do estudo. Foi realizad auma busca exploratória no Google Scholar com ênfase em estudos publicados nos últimos dois anos que apresentassem experimentos ou aplicações práticas de LLMs especializados em conhecimento específico de domínio e técnico em engenharia de software. A restrição de tempo também buscou acompanhar o ritmo acelerado de divulgação de modelos na atualidade desta linha de pesquisa. Foram considerados os seguintes critérios principais:

1. Modelo especializado em raciocínio em conhecimento específico de domínio de negócio com cenário de aplicação real em contextos da prática de Engenharia de Software
2. Disponibilidade pública do modelo especializado e de seu modelo base correspondente com arquitetura e número de parâmetros equivalentes
3. Evidência empírica de que o modelo foi treinado com dados e cenários próximos da realidade da indústria de software
4. Modelos adequados para execução self-hosted utilizando a plataforma Ollama
5. Existência de documentação de suporte para a instrumentação experimental dos modelos

Fin-R1 é um LLM especializado desenvolvido por Zhang et al. (2025) a partir do fine-tuning do modelo Qwen2.5-7B-Instruct. Fin-R1 pontuou com performance SOTA (State of The Art) em raciocínio financeiro complexo, cenário bem realístico na prática de Engenharia de Software (Zhang et al. (2025)). O Qwen2.5-&b-Instruct de Ye et al. (2024) é é um modelo open-source, reconhecido por notório desempenho em atividades de desenvolvimento de software. Assim Fin-R1 e Qwen2.5-7B-Instruct se mostraram os modelos mais adequados e representativos para o experimento.


[1] Z. Zhang et al., "Testing Prompt Engineering Methods for Knowledge Extraction from Text," arXiv preprint arXiv:2503.16252, 2025. Available: https://arxiv.org/abs/2503.16252.

[2] X. Ye et al., "CodeQwen2: A High-Performance Code Language Model," arXiv preprint arXiv:2412.15115, 2024. Available: https://arxiv.org/abs/2412.15115.

### 6.2 Preparação

#### 6.2.1 Configuração de Ambiente e Execução dos LLMs

Os modelos Fin-R1 e Quen2.5-7B-Instruct foram executados integrados à plataforma Ollama, respeitando as configurações padrão recomendadas por seus desenvolvedores com adaptações específicas necessárias ao contexto da pesquisa. O ambiente de execução foi completamente controlado e dedicado à realização do experimento.

..incluir a parametrizacao dos modelos...


Esxiste uma lacuna de guidelines ou evidências na literatura de Engenharia de Software Empírica que oriente a configuração de hiperparâmetros para atividades de geração de artefatos como o desta pesquisa. Embora existam estudos que exploram o impacto de parâmetros como `temperature` e `top_p` em tarefas de geração textual geral, ainda são necessárias pesquisas que discutam os efeitos destes parâmetros na produção de artefatos estruturados que exijam raciocínio técnico.

Os modelos forram calibrados empiricamente para 

#### 6.2.2 Preparação dos Instrumentos de Coleta

Os intrumentos de coleta e avaliação foram desenvovidos conforme o planejado e de fato corroboraram para a redução da carga cognitiva dos participantes e para controlar vieses decorrentes da falta de familiaridade com a tarefa de avaliação. 



### 6.3 Coleta de dados

### 6.4 Procedimento de validação

## 7. Análise

### 7.1 Estatística descritiva

### 7.2 Redução do conjunto de dados com foco na analise

### 7.3 Testes de Hipóteses

## 8. Interpretação

### 8.1 Avaliação dos resultados e implicações

### 8.2 Limitações do estudo

### 8.3 Inferências

### 8.4 Lições aprendidas

## 9. Conclusões e Trabalhos Futuros

### 9.1 Relação com a evidência existente

### 9.2 Impacto

### 9.3 Limitações

### 9.4 Trabalhos futuros

## 10. Agradecimentos

## 11. Referências

## 12. Apêndices















### Seleção do Modelo

 O Qwen2.5-Code foi selecionado com base nos seguintes critérios:

1. Arquitetura open-source bom bom desempenho na geração de artefatos de software
2. Modelo com desempenho superior em benchmarks de compreensão técnica
3. Modelo com capacidade comprovada no processamento de linguagens de programação
4. Modelo com flexibilidade para fine-tuning em domínios específicos

### Tratamento 1: LLM com Fine-tunning em Domínio Financeiro

- Fin-R1 A Large Language Model for Financial Reasoning through Reinforcement Learning ()
- Primeira etapa: Fine-tunning do modelo Quen2.5-7B-Instruct com datasets financeiros:
  - Utilização dos datasets ConvFinQA e FinQA
  - Objetivo: Desenvolver capacidade de raciocínio em domínio financeiro
- Segunda etapa: Aplicação do algoritmo GRPO (Generative Reinforcement Policy Optimization): 
  - Otimização do formato e acurácia de saída
  - Uso do Quen2.5-Max para mitigar potenciais vieses de recompensa
  - 
### Grupo de controle: Quen2.5-7b-Instruct

- Modelo base da especialização do Fin-R1

### Contexto do Sistema para Geração dos Casos de Uso

- Contexto: sistema de gerenciamento de financas pessoais baseado em IA
- Especificação C4 do sistema do nível C1 ao C3
- Documentação em markdown e linguagem plantuml

#### Artefato em avaliação

- Diagrama de casos de uso. 
- Exige compreensão do domínio de negócio e da especificação de nível C1 do sistema.


### Medição das variáveis

Cada componente do diagrama é uma *unidade semântica e estrutural* que pode fornecer evidências para avaliar mais de uma variável dependente, pois:

1. A forma como o componente é escrito fornece informações sintáticas (ex: se há erro de notação);
2. A presença ou ausência do componente informa sobre completude;
3. Os tipos de componentes (nomes, relações, agrupamentos) revela coerência semântica da epecificação técnica com o conhecimento explícito do domínio;
4. A escolha de termos e estruturação conceitual dos componentes do diagrama reflete a articulação técnico-conceitual.

#### Mapeamento entre Componentes do Diagrama e Variáveis

| Elemento | PlantUML | Correção Sintática | Completude Técnica | Coerência com o Domínio | Articulação Técnico-Conceitual |
|----------|----------|-------------------|-------------------|------------------------|------------------------------|
| Atores | ✅ | ✅ | ✅ | ✅ |
| Casos de Uso | ✅ | ✅ | ✅ | ✅ |
| Relacionamentos | ✅ | ✅ | ✅ | ✅ |
| Notas explicativas | ✅ (estrutura) | ✅ (detalhamento) | ✅ | ✅ |
| Pacotes | ✅ (estrutura) | ✅ (agrupamento) | ✅ | ✅ |
| Estereótipos | ✅ (notação) | Opcional | ✅ | ✅ |


#### Mapeamento entre os Componentes do Diagrama e Sintaxe PlantUML

| Elemento | Sintaxe em PlantUML | Descrição | Relevância para as Variáveis Dependentes |
|---------|-------------------|-----------|----------------------------------------|
| **Ator** | `actor NomeDoAtor` ou `:NomeDoAtor:` | Representa uma entidade externa (usuário ou sistema) que interage com o sistema. | **Completude** (presença dos atores esperados)<br>**Coerência** (nomes alinhados ao domínio)<br>**Articulação** (clareza conceitual dos papéis)<br>**Sintaxe** (uso correto) |
| **Caso de Uso** | `(NomeDoCasoDeUso)` ou `usecase Nome` | Representa uma funcionalidade específica que o sistema oferece a um ator. | **Completude** (cobertura funcional)<br>**Coerência** (semântica alinhada ao domínio)<br>**Articulação** (expressão precisa de intenções)<br>**Sintaxe** (formatação correta) |
| **Relacionamento** | `Ator --> CasoDeUso`, `CasoDeUso --> CasoDeUso` | Define interações e dependências entre atores e casos de uso, incluindo extensão (`<<extend>>`) e inclusão (`<<include>>`). | |
| **Nota** | `note right of Ator : texto` ou `note over CasoDeUso : texto` | Adiciona informações explicativas, restrições ou observações a atores ou casos de uso. | **Completude** (explicitação de detalhes)<br>**Coerência** (relevância do conteúdo)<br>**Articulação** (clareza na linguagem usada)<br>**Sintaxe** (estrutura correta) |
| **Pacote** | `package NomeDoPacote { ... }` | Agrupa casos de uso relacionados em uma estrutura hierárquica ou modular. | **Completude** (organização funcional)<br>**Articulação** (clareza de escopo e agrupamentos)<br>**Sintaxe** (uso correto da estrutura) |
| **Estereótipos** | `<<include>>`, `<<extend>>`, `<<stereotype>>` | Extensões semânticas para casos de uso, indicando comportamentos adicionais ou dependências. | **Coerência** (uso de padrões corretos)<br>**Articulação** (clareza da lógica de composição entre casos de uso)<br>**Sintaxe** (aplicação correta da anotação) |
| **Limite do Sistema** | `rectangle Sistema { ... }` | Representa visualmente o escopo do sistema que está sendo modelado. | **Completude** (delimitação do que está ou não no sistema)<br>**Articulação** (clareza conceitual do escopo)<br>**Sintaxe** (uso da estrutura de retângulo no código) |


**Nota:** Este é um relatório preliminary de pesquisa. Resultados completos serão publicados em trabalhos futuros.

### Referências 

1. Wang, S., et al. (2023). Challenges in Large Language Models for Software Engineering.
2. Vaithilingam, P., et al. (2022). Bridging Domain Knowledge in Software Artifact Generation.
3. Liu, J., et al. (2023). Limitations of LLMs in Technical Specification.
4. Moreno, L., & Jhoof, M. (2022). Ontology and Domain Patterns in Language Models.
5. Terragni, V., et al. (2024). Specialized Models in Software Engineering.
6. Zhao, W.X., et al. (2023). Reasoning and Knowledge Application in LLMs.
7. Brachman, R., & Levesque, H. (2004). Knowledge Representation and Reasoning.