
Overview do Experimento: Avaliação da Infusão de Conhecimento em LLMs para Geração de Diagramas de Máquina de Estados

# 1 Introdução

O experimento investiga o impacto da infusão de conhecimento em modelos de linguagem (LLMs) na geração de artefatos (diagramas UML de máquina de estados). O cenário utilizado será o da norma técnica que define os padrões ITU-T e 3GPP (GSM, LTE, 5G).


# 4  Metodologia

## Etapa 1

### Definições

Investigar e quantificar a correlação entre a infusão de conhecimento e a qualidade técnica dos diagramas UML de máquina de estados gerados por Large Language Models (LLMs).

* 1. Infusão de conhecimento e estratégias associadas ao LLM*
- Infusão de conhecimento: processo de incorporar informações específicas do domínio através de prompts ou base de conhecimento com o objetivo de melhorar o conhecimento de domínio.
- Técnicas: Retrieval-Augmented Generation (RAG), Prompt Engineering, Few-shot Learning

* 2. Análise do diagrama de Máquina de Estados* 
- Qualidade técnica: a qualidade técnica será discutida com base na precisão, completude, conformidade e interpretação das restrições apresentadas nos diagramas em gerados em função do conhecimento de domínio fusionado.
- Elementos observados: Estados (incluindo estados iniciais, finais e compostos), Transições (incluindo eventos, guardas e ações), Ações de entrada, saída e internas, Pseudo-estados (como pontos de decisão e histórico) e Regiões concorrentes (se aplicável) e coerência com as normas estabelecidas no domínio fusionado
- Comparação: será feita entre os diagramas gerados pelo LLM sem infusão de conhecimento (baseline) e os gerados pelo LLM com a infusão. A comparação permite quantificar o impacto da infusão na qualidade técnica dos diagramas gerados.

* 3. Contexto de aplicação *
- Cenário específico que utilizem regras de negócio, normas ou regras de um domínio específico
- No caso do estudo escolhemos os Padrões de telecomunicação ITU-T ou 3GPP (GSM, LTE, 5G) apenas como um exemplo baseado em norma. O foco será nos cenários de ferenciamento de energia, handover, e estabelecimento de conexão.

* 4. As métricas de valiação *
- Precisão dos elementos do diagrama
- Completude do diagrama em relação a um padrão de referência
- Conformidade com as especificações técnicas do padrão de telecomunicação
- Complexidade estrutural do diagrama
- Coerência com as informações impostas pelo domínio de negócio

* 5. A análise de correlação *
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

### Configuração do contexto

#### Caracterização
- Offline: Em ambiente controlado, garantindo o controle total sobre variáveis.
- Simulado: Baseado em cenários comuns de telecomunicações, utilizando dados fictícios mas realistas.
- Específico: Focado em diagramas UML de máquina de estados para redes de telecomunicações.
- Considerações eticas e tecnológicas: Alinhamento com práticas éticas de IA, documentando uso e justificativa para cada técnica. Estrutura tecnológica que facilite a repetição e verificação do experimento.
- Replicabilidade: Descrição e disponibilização completa de cada procedimento e configuração

#### Elementos
- Objeto de estudo: Diagrama UML de máquina de estados gerado pelo LLM em PlantUML.
- Indivíduos: LLMs
- Tratamentos: Técnicas de infusão de conhecimento
- Artefatos: Diagramas UML de Máquina de Estados
- Controle de variáveis:
 * Parametrização do LLM
 * Estrutura de prompt
 * Conhecimento de domínio

#### Classificação 
 * Tipo: Experimento controlado
 * Objetivo: análise do impacto da infusão de conhecimento em LLMs
 * Perspectiva: Pesquisadores em Engenharia de Software e Telecomunicações
 * Domínio: Telecomunicações com o foco em padrões ITU-T e 3GPP

### Definição das hipóteses

#### Premissas 

1. Os LLMs são capazes de gerar diagramas UML de máquina de estados em formato PlantUML.
2. A qualidade dos diagramas gerados pode ser medida objetivamente através de métricas predefinidas.
3. A infusão de conhecimento de domínio pode influenciar a qualidade dos diagramas gerados.
4. As diferentes técnicas de infusão de conhecimento (RAG, Prompt Engineering, Few-shot Learning) podem ter efeitos variados na qualidade dos diagramas.

#### Hipóteses
- * Hipótese Nula (H0):*  Não há diferença significativa na qualidade dos diagramas UML de máquina de estados gerados por LLMs com e sem infusão de conhecimento de domínio.
- * Hipótese Alternativa (H1):* Há diferença na qualidade dos diagramas UML de máquina de estados gerados por LLMs com infusão de conhecimento de domínio em comparação com aqueles sem infusão.

#### Itens de coleta

1. Respostas do LLM 
- resposta bruta gerada
- diagrama PlantUML gerado
- técnica utilizada
- cenário 

2. Características do diagrama

As características abaixo foram elegidas por serem diretamente influenciadas pelo conhecimento de domínio e na aplicação apropriada deste conhecimento.

* Conhecimento do domínio: *
- conformidade de negócio (35%): conformidade dos elementos do diagrama em funcao das especificações e padrões ITU-3GPP 
- completude (30%): contabilização de elementos que correspondem ao modelo esperado 

* Aplicação apropriada do conhecimento do domínio: *
- consistência interna (20%): avalia a coerência lógica e estrutural do diagrama, indicador da qualidade do raciocínio do LLM sobre o domínio (Referência: Lindland et al. (1994))
- uso apropriado dos elementos UML (15%):  avalia se os elementos são utilizados corretamente e de forma apropriada co contexto (Referência: Genero et al. (2011) em "A controlled experiment to assess the impact of structural complexity on the understandability of UML statechart diagrams)

3. Métricas quantitativas
* Conformidade de negócio *

Será coletada através de checklist criado em conformidade com a especificação da norma. O checklist será validado pelo especialista do domínio e permite a participação de especialistas de diferentes níveis de conhecimento no domínio. Será realizada uma sessão de calibração onde os avaliadpres aplicarão uma lista de verificação em um conjunto comum de diagramas e discutirão suas avaliações para o alinhamento das interpretações.

- Para mitigar a subjetividade do especialista, a falta de padronização e replicabilidade consideramos a criacao de uma lista de verificacao baseada diretamente nos documentos de padroes ITU-T e 3GPP relevantes.
- Cada item da lista é uma afirmação clara e verificável minimizando possibilidades de interpretação do especialista (ex: o diagrama inclui um estado 'idle' conforme especificado na seção X.XX do padrão ITU-T Y.XXX' )
- Será atribuída uma pontuação binária pnde será adotado 1 para conformidade e 2 para não conformidade
- A conformidade será calculada como uma porcentagem dos itens atendidos

- Completude: será medido através de um checklist (Lindland et al. (1994) sugerem o uso de checklists para avaliar a completude de modelos conceituais. Mohagheghi et al. (2009) recomendam a comparação com um modelo de referência para avaliar a completude.)

4. Métricas qualitativas
- avaliaçao: pontuacao de qualidade para cada diagrama com base nos criterios de conformidade e precisão
- classificação de erros: identificacao dos erros comuns e categoriação conforme a taxonomia estabelecida

5. Metadados experimentais
- técnica de infusão
- data e hora
- executor
- parametros do modelo

### Definição das variáveis

#### Variável dependente

A qualidade do diagrama será tratada como a variável dependente e será medida através de um índice composto a partir das métricas abaixo: 
- correção sintática (20%)
- completude em relacao aos requisitos do domínio (25%)

É importante ressaltar que como o objetivo do estudo não é medir a capacidade do LLM de produzir código sintaticamente correto serão consideradas como amostras apenas os códigos gerados que compilam (remoção de ruídos). Esta decisão permite focar no que é relevante para a hipótese e garantir que o experimento seja concentrado na análise da influência do conhecimento de domínio e sua relação com a qualidade semântica e estrutural dos diagramas.


#### Variável independente


### Definição dos sujeitos

#### Premissas

#### Sujeito


### Escolha do desenho experimental

#### Randomização

#### Bloqueio

#### Balanceameno

#### Design experimental

 O design experimental é um fator com quatro tratamentos:
 
 * Fator: Técnica de infusão de conhecimento
 * Tratamentos: Sem infusão (controle), RAG (Retrieval-Augmented Generation), Prompt Engineering, Few-shot Learning

### Instrumentação

#### LLMs

#### Especificações

#### Prompts

#### Armazenamento da coleta

#### Análise
- taxonomia de classificação

### Validação

#### De conclusão

#### Interna

#### De constructo

#### Externa

  * Controle: Geração sem infusão de conhecimento.
 * RAG (Retrieval-Augmented Generation): Técnica com recuperação de dados externos.
 * Prompt Engineering: Ajuste e customização dos prompts.
 * Few-shot Learning: Exposição a exemplos durante o prompt.



- Aleatorização: Execuções múltiplas para cada combinação de técnica e LLM para evitar efeito de aprendizado. Variar o momento das execuções para controlar potenciais influencias externas e aumentar a segurança da análise.
- Métricas de avaliação (Variáveis dependentes)
 * Precisão: correspondência entre os elementos do diagrama e o padrão esperado
 * Completude: o quão proximo o diagrama está do modelo de refer6encia
 * Conformidade técnica: grau de alinhamento com as especificacoes impostas pela norma
 * Complexidade estrutural: análise da complexidade e quantidade de elementos do diagrama
- Análise:
 * Quantitativa através dos testes estatísticos
 * Qualitativa através da análise dos especialistas