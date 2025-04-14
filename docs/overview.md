
Overview da Pesquisa: Avaliar a Relação de Causa e Efeito entre a Infusão de Conhecimento Específico em LLMs E q qualidade de artefatos de software

# 1 Introdução

Realizar uma serie de experimentos para investigar o a relação de causa e efeito entre a especializacao de conhecimento espeifico de dominio e a qualidade da especificacao tecnica de artegatos gerados por modelos de linguagem (LLMs).  A perspectiva será sempre do engenheiro de software com o foco na adocao desta tecnologia no processo de desenvolvimento de software. Mais especificamente no desenvolvimento orientado ao modelo C4 Model para especificacao, modelagem e implementacao das funcionalidades do sistema.


# 4  Metodologia

## Etapa 1

### Definições

Investigar e quantificar a relação  entre a infusão de conhecimento e a qualidade técnica dos artefatos de software gerados por Large Language Models (LLMs).

**1. Infusão de conhecimento e estratégias associadas ao LLM**
- Infusão de conhecimento: processo de incorporar conhecimento explicito sobre domínio de negócio.
- Técnicas: Fine Tunning, Retrieval-Augmented Generation (RAG), Prompt Engineering, Few-shot Learning

**2. Análise do diagrama de Máquina de Estados** 
- Qualidade técnica: a qualidade técnica será discutida com base na precisão, completude, conformidade e interpretação das restrições apresentadas nos diagramas em gerados em função do conhecimento de domínio fusionado.
- Elementos observados: Estados (incluindo estados iniciais, finais e compostos), Transições (incluindo eventos, guardas e ações), Ações de entrada, saída e internas, Pseudo-estados (como pontos de decisão e histórico) e Regiões concorrentes (se aplicável) e coerência com as normas estabelecidas no domínio fusionado
- Comparação: será feita entre os diagramas gerados pelo LLM sem infusão de conhecimento (baseline) e os gerados pelo LLM com a infusão. A comparação permite quantificar o impacto da infusão na qualidade técnica dos diagramas gerados.

**3. Contexto de aplicação**
- Cenário específico que utilizem regras de negócio, normas ou regras de um domínio específico
- No caso do estudo escolhemos os Padrões de telecomunicação ITU-T ou 3GPP (GSM, LTE, 5G) apenas como um exemplo baseado em norma. O foco será nos cenários de ferenciamento de energia, handover, e estabelecimento de conexão.

**4. As métricas de valiação**
- Precisão dos elementos do diagrama
- Completude do diagrama em relação a um padrão de referência
- Conformidade com as especificações técnicas do padrão de telecomunicação
- Complexidade estrutural do diagrama
- Coerência com as informações impostas pelo domínio de negócio

**5. A análise de correlação**
- Examina a relação entre cada a infusão de conhecimento e a presença/qualidade dos elementos técnicos no diagrama
- Examina a relação entre cada técnica de infusão de conhecimento e a presença/qualidade dos elementos técnicos no diagrama
- Analisa os efeitos da infusão de conhecimento e o impacto nos elementos técnicos do diagrama
- Analisa os impacto relativo de cada técnica de infusão de conhecimento nos elementos técnicos do diagrama

### Escopo

- O experimento é concentrado apenas em diagramas de máquina de estados UML, excluindo outros tipos de diagramas UML
- A avaliação é limitada a cenários específicos de telecomunicações, não abrangendo todos os aspectos possíveis  mas sendo expansível a outros cenários
- O estudo não visa a otimização de desempenho computacional das técnicas de infusão de conhecimento

### Objetivo

**Objetivo principal:** Investigar o impacto da infusão de conhecimento na geração de diagramas de máquina de estados

### Resultados esperados (meta)

- Analisa se existe correlação entre a infusão de conhecimento os reflexos nos elementos técnicos do diagrama gerados pelos LLMs
- Identifica e quantifica o impacto da infusão de conhecimento nos elementos específicos dos diagramasgerados pelos LLMs
- Analisa como diferentes aspectos do conhecimento infundido impactam a geração de elementos técnicos específicos da modelagem gerada pelos LLMs.
=> Avalia a precisão e a completude dos diagramas, padrões de erro comuns e possíveis limitações de cada técnica.

### Questões de pesquisa

1. Como a infusão de conhecimento afeta a qualidade dos diagramas gerados?
2. Qual técnica oferece os melhores resultados em termos de precisão e conformidade com o conhecimento fusionado? 
3. Quais os principais erros cometidos pelos LLMs ao gerar os diagramas?

#. Qual a influência da infusão de conhecimento na geração do diagrama de máquina de estados?
#. Qual das técnicas de infusão de conhecimento gera o diagrama mais fiel aos padrões ITU-T e 3GPP?
#. Como o LLM interpreta e organiza a relação entre conhecimento e elementos do diagrama de máquina de estados?

### Limitaçoẽs 

1. Este estudo é uma exploração inicial para fundamentar uma avaliação posterior aprofundada da tese principal, onde cada técnica de infusão de conhecimento se alinhará a um nível específico de conhecimento.
2. A generalização dos achados ainda necessita de mais explorações pois o escopo do experimento é restrito apenas a diagramas de máquina de estados UML e a cenários específicos do domínio de negócio de telecomunicações.
3. Foi utilizado um número limitado de diagramas e cenários avaliados e por este motivo ainda é necessário uma apliação desde cenário e tamanho de amostra
4. A validação foi submetida a um número limitado de especialistas é muito importante que isto seja expandido
5. Possiveis variações nos resultados mediante atualizações não puderam ser controladas, bem como as diferenças de performances entre os difererntes modelos LLMs.
6. O domínio escolhido pode não repreesentar todos os desafios de outras possibilidades de domínios em mediante a complexidade inerente da tematica escolhida.

### Inovação e contribuição 

1. Investigar como a inserção de contexto de domínio impacta a geração de artefatos de software por LLMs contribui com oportunidades de pesquisa identificadas em estudos anteriores sobre o uso de LLMs na engenharia de software. O foco da linha de pesquisa é alinhado com princípios do Domain-Driven Design (DDD) que enfatizam a importância do conhecimento profundo do domínio na construção de software.

## Etapa 2

### 2.1 Configuração do contexto

#### 2.1.1 Caracterização
- Offline: Em ambiente controlado, garantindo o controle total sobre variáveis.
- Simulado: Baseado em cenários comuns de telecomunicações, utilizando dados fictícios mas realistas.
- Específico: Focado em diagramas UML de máquina de estados para redes de telecomunicações.
- Considerações eticas e tecnológicas: Alinhamento com práticas éticas de IA, documentando uso e justificativa para cada técnica. Estrutura tecnológica que facilite a repetição e verificação do experimento.
- Replicabilidade: Descrição e disponibilização completa de cada procedimento e configuração

#### 2.1.2 Elementos
- Objeto de estudo: Diagrama UML de máquina de estados gerado pelo LLM em PlantUML.
- Indivíduos: LLMs
- Tratamentos: Técnicas de infusão de conhecimento
- Artefatos: Diagramas UML de Máquina de Estados
- Controle de variáveis:
 * Parametrização do LLM
 * Estrutura de prompt
 * Conhecimento de domínio

#### 2.1.3 Classificação 
 * Tipo: Experimento controlado
 * Objetivo: análise do impacto da infusão de conhecimento em LLMs
 * Perspectiva: Pesquisadores em Engenharia de Software e Telecomunicações
 * Domínio: Telecomunicações com o foco em padrões ITU-T e 3GPP

### 2.2 Definição das hipóteses

#### 2.2.1 Premissas 

1. Os LLMs são capazes de gerar diagramas UML de máquina de estados em formato PlantUML.
2. A qualidade dos diagramas gerados pode ser medida objetivamente através de métricas predefinidas.
3. A infusão de conhecimento de domínio pode influenciar a qualidade dos diagramas gerados.
4. As diferentes técnicas de infusão de conhecimento (RAG, Prompt Engineering, Few-shot Learning) podem ter efeitos variados na qualidade dos diagramas.

#### 2.2.2 Hipóteses
- **Hipótese Nula (H0):**  Não há diferença significativa na qualidade dos diagramas UML de máquina de estados gerados por LLMs com e sem infusão de conhecimento de domínio.
- **Hipótese Alternativa (H1):** Há diferença na qualidade dos diagramas UML de máquina de estados gerados por LLMs com infusão de conhecimento de domínio em comparação com aqueles sem infusão.

### 2.3 Itens de coleta

 Abaixo são os itens de coleta juntamente com suas caracterizações, informações relevantes e decisões estabelecidas para a realização do experimento.

#### 2.3.1 Respostas do LLM 
**Caracterização**
- resposta bruta gerada
- diagrama PlantUML gerado
- técnica utilizada
- cenário 

#### 2.3.2 Diagrama de máquina de estados

O diagrama será coletado através da obtenção da imagem gerada através da compilação do código PlantUML extraído da resposta gerada pelo LLM. Ele será caracterizado em função da apresentação dos elementos presentes no diagrama de máquina de estados: estados, pseudoestados, ações, eventos, (**TODO:** detalhar todos os elementos)

#### 2.3.3 Métricas quantitativas

As métricas serão contabilizadas a partir da aplicação de checklists baseados em um modelo de referência criado com base nos padrões ITU-T e 3GPP para mitigar subjetividade, falta de padronização e favorecer a replicabilidade do experimento (Lindland et al. (1994), Mohagheghi et al. (2009)). Os itens do checklist avaliam de maneira binária e clara elementos que podem ser objetivamente quantificados(ex: numero de estados, tipos de transicoes, presença de elementos obrigatórios, etc). O valor da métrica será calculado como uma porcentagem dos itens atendidos. Um comitê(3 -5 membros) validará e aplicará os checklists em um conjunto comum de diagramas antes da coleta para o alinhamento das interpretações e gerarão orientações para mitigar possíveis riscos durante a coleta.

**Conformidade de negócio (aderência dos elementos do diagrama às especificações técnicas e formais da norma):** Valor percentual obtido através de aplicação de checklist que avalia a sintaxe do diagrama gerado em relação regras e convenções estabelecidas na norma ITU-3GPP. 

- Os critérios são derivados da CONSTRUÇÃO SINTÁTICA dos elementos do diagrama e medem se as regras e convenções estabelecidas no padrão ITU-3GPP foram atendidas (ex: as transicoes estao rotuladas de acordo com a nomenclatura definida na seção X.XXX da norma)
- Será necessário definir todas as regras de modelagem a serem atendidas conforme a norma. (ex: nomenclatura)

**Completude (aderência do conteúdo semântico do diagrama em relação às especificações técnicas e formais da norma):** Valor percentual obtido através de aplicação de checklist que avalia a semântica do diagrama gerado em relação aos requisitos estabelecidos pela norma ITU-3GPP. 

- Os critérios são derivados da CONSTRUÇÃO SEMÂNTICA do diagrama em relação aos requisitos funcionais e de negócio determinados pela norma ITU-3GPP
- Verifica se todos os conceitos necessários estão presentes independentemente de como são representados

#### 2.3.4 Métricas qualitativas

As métricas qualitativas serão derivada em função das quantitativas para mitigar riscos de viés, overfiting e de captura de compreensibilidade estabelecendo um equilíbrio entre objetividade quantitativa e insights qualitativos. A derivação da métrica qualitativa será aplicada em função dos valores das métricas de completude e conformidade. Considerando que do ponto de vista prático de um engenheiro de software um dagrama semanticamente consistente e correto é mais valioso do que um apenas sintaticamente correto a completude terá um peso de 70% e a conformidade 30%, definindo o cálculo da pontuação quantitativa: Pontuacao Qualitativa = (Pontuacao de Completude * 0,7) + (Pontuação de conformidade * 0,3). Será aplicada uma escala Likert  de três pontos para medir a "adequação geral" do diagrama: 1)Inadequado (0% a 50% - atendem a menos de 2/3 - conformidade sintatica com baixa completude semântica), 2)Adequado (51 a 80% - boa completude semântica mas com falhas sintáticas que necessitam de revisão) e 3) Excelente (81% a 100% - capturam a essencia estabelecida na norma entretanto aspectos sintáticos podem receber correções opcionais).

- Inadequado: diagramas que apresenta modelagem com deficiencias semânticas significativas. Contém erros conceituais graves ou omissões relevantes que comprometem a utilidade do diagrama, mesmo que alguns aspectos sintáticos estejam corretos
- Adequado: diagramas que apresentam modelagem que captura a maioria dos elementos semânticos essenciais do negócio, proporcionando uma compreensão marjoritariamente correta. Pode apresentar  imprecisões sintáticas ou desvios menores do contexto de negócio mas que não comprometem significativamente o entendimento ou utilidade do diagrama.
- Excelente: diagramas que apresentam modelagem semanticamente rica e precisa do negócio que captura quase todos os elementos essenciais. A estrutura geral e conceitos-chave são representados de forma clara e correta. Pequenas imperfeições sintáticas ou melhorias estão presentes mas não são relevantes em comparação a força d representação semântica.

Esta abordagem aplica uma relevância maior na corretude semântica e na utilidade prática do diagrama para engenheiros de software e permite avaliar mais precisamente o impacto da infusão de conhecimento na geração dos diagramas de máquinas de estados.

#### 2.3.5 Metadados experimentais
- técnica de infusão
- data e hora
- executor
- parametros do modelo

### 3. Definição das variáveis

#### 3.1 Variável dependente

A variável dependente no experimento é a qualidade do diagrama que será medida através das métricas quantitativas e qualitativas e variam em função da técnica de infusão de conhecimento. 

É importante ressaltar que como o objetivo do estudo não é medir a capacidade do LLM de produzir código sintaticamente correto e por isso serão consideradas como amostras apenas as gerações de diagramas que compilam (remoção de ruídos). Esta decisão permite focar no que é relevante para a hipótese e garantir que o experimento seja concentrado na análise da influência do conhecimento de domínio e sua relação com a qualidade semântica e estrutural dos diagramas.

#### 3.2 Variável independente

A variável independente é a técnica de infusão de conhecimento que será controlada e modificada durante o experimento, para investigar a qualidade dos diagramas de máquinas de estado gerados pelos LLMs no contexto específico do domínio das normas ITU-3GP. A hipótese nula (H0) afirma que a manipulação desta variável não terá efeito significativo na qualidade dos diagramas de máquina de estados gerados. Por sua vez a hipótese alternativa (H1) sugere que a manipulação desta variável resultará em diferença observável na qualidade dos diagramas gerados. A comparação entre os diagramas gerados com e sem infusão de conhecimento permite avaliar o impacto direto na variável dependente.

### 4. Definição dos sujeitos

#### 4.1 Premissas

1. Os LLMs são capazes de gerar código na linguagem PlantUML
2. Os LLMs não serão retreinados para inserção de conhecimento
3. É relevante discutir característica da natureza probailistica na geração de respostas que são inerentes aos LLMs. Esta característica contribui para a mitigação do viés sa seleção dos sujeitos.   - Aleatorização: Execuções múltiplas para cada combinação de técnica e LLM para evitar efeito de aprendizado. Variar o momento das execuções para controlar potenciais influencias externas e aumentar a segurança da análise.
4. O prompt é o estímulo e a resposta é o comportamento do LLM que estamos observando
5. Nosso objetivo é entender como diferentes técnicas de infusão de conhecimento afetam o desempenho do LLM na geracao de diagrams UML . Sendo assim o LLM é o arot principal neste cenário
6. Os objetos em que o experimento são executados são chamados unidades experimentais ou objetos experimentais (pacientes são unidades experimentais em experimentos médicos da mesma forma que pedacos de terra sao em experimentos agriculturais). No nosso caso a unidade experimental é o LLM
7. A unidade experimental é quem aplica o tratamento e é chamado de subject experimental no caso é o prompt: veículo de aplicação do tratamento

#### 4.2 Sujeito

As unidades epeximentais são os objetos que recebem o tratamento, no nosso caso são os LLMs. Os sujeito são os que aplicam o tratamento e no nosso caso temos os prompts, eles levam o tratamento a ser aplicado

Os sujeitos do experimento são os LLMs que irão aplicar o tratamento da infusão de conhecimento para aplicar na unidade experimental que no nosso experimento é o LLM, aquele que recebe o tratamento. As unidades experimentais serão caracterizados através do: 1) Tamanho do modelo(quantidade de parâmetros), 2) Arquitetura, 3) Conjunto de dados de treinamento, 4) Capacidades conhecidas em geração de código e compreensão de diagramas**


 produzir o insumo de avaliação para análise que são os diagramas UML de máquina de estados em formato PlantUML

### 5. Escolha do desenho experimental

#### 5.1 Randomização

#### 5.2 Bloqueio

#### 5.3 Balanceameno

#### 5.4 Design experimental

 O design experimental é um fator com quatro tratamentos:
 
 * Fator: Técnica de infusão de conhecimento
 * Tratamentos: Sem infusão (controle), RAG (Retrieval-Augmented Generation), Prompt Engineering, Few-shot Learning

### 6. Instrumentação

#### 6.1 LLMs

#### 6.2 Especificações

#### 6.3 Prompts

#### 6.4 Armazenamento da coleta

#### 6.5 Análise
- taxonomia de classificação

### 7. Validação

#### 7.1 De conclusão

#### 7.2 Interna

#### 7.3 De constructo

#### 7.4 Externa










  * Controle: Geração sem infusão de conhecimento.
 * RAG (Retrieval-Augmented Generation): Técnica com recuperação de dados externos.
 * Prompt Engineering: Ajuste e customização dos prompts.
 * Few-shot Learning: Exposição a exemplos durante o prompt.




- Métricas de avaliação (Variáveis dependentes)
 * Precisão: correspondência entre os elementos do diagrama e o padrão esperado
 * Completude: o quão proximo o diagrama está do modelo de refer6encia
 * Conformidade técnica: grau de alinhamento com as especificacoes impostas pela norma
 * Complexidade estrutural: análise da complexidade e quantidade de elementos do diagrama
- Análise:
 * Quantitativa através dos testes estatísticos
 * Qualitativa através da análise dos especialistas