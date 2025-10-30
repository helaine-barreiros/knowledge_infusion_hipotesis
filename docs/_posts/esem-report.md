# Domain Knowledge vs. Syntactic Precision: The Trade-off in Production-Viable Use Case Diagrams Generation
---
## Structured Abstract

### Background: 
The Software Engineering (SE) community has investigated Large Language Models (LLMs) for many artifact generation like code, documentation, requirements and modeling \cite{b1, b2}. However, LLMs struggle with artifacts due to limited domain-specific knowledge (DSK), a significant constraint since technical viable software artifact construction requires articulation of both domain and technical knowledge\cite{b3, b4}.

### Objective: 
This research evaluates the ability of both generalist LLM and LLM specialized in finance to generate production-viable use case diagrams from a software engineering perspective.

### Method: 
In a unifactorial controlled experiment design, 2000 use case diagrams were automated collected from both models and evaluated using a custom-developed measurement to quantify the modifications to achieve production-viable diagrams. Three citical dimensions was statisticaly analyzed: syntactic correctness, technical completeness, and tecnical-conceptual articulation.

### Results: 
Comparative analysis revealed that the Specialist LLM significantly outperformed the Generalist LLM in producing production-viable diagrams with balanced tecnical-conceptual articulation (p-value $>$ 0.05). However, an unexpected trade-off reveals that Specialist LLM exhibited more frequent syntactic violations, suggesting that enhanced vector domain knowledge compete with syntatic capacity in PlantUML.

### Limitations: 
This study was constrained by the absence of standardized experimental protocols, benchmarks and prompt engineering for complex technical instructions for LLM in SE context and convenience-based model selection.

### Conclusions: 
These findings empirically validate that DSK representations transform LLM's capability to generate production-viable use case diagrams while revealing a previously uncharactized inverse correlation bwtween DSK and syntatic knownledge specialization. Future work should focus on specialization architectural components that preserve syntatic knowledge alongside DSK specialization.

## Definicoes

Completude Técnica, no contexto a pesquisa representa a:

Capacidade do LLM de entender e aplicar uma instrução técnica clara, correta e completa para gerar um artefato de software que reflita fielmente os elementos esperados, sem exigir retrabalho técnico substancial.

É a tradução direta de:
📦 Prompt técnico → 🧠 Compreensão → 🛠 Artefato aderente

## Objetivo da metrica

Capturar a capacidade do modelo de receber uma instrucão técnica e usá-la para gerar um diagrama de casos de uso que reflita fielmente os elementos esperado e exiga baixo retrabalho técnico

## Dados candidatos

 1. Cobertura por componentes do diagrama: actors_coverage, usecases_coverage, relationships_coverage
    - Mede se cada tipo de componente foi entregue conforme o esperado no modelo de referencia
    - permite dizer qual componente o diagrama se sai melhor ou se é constante
    - não mede excesso em erros estruturais
    - corre o risco de um diagrama ter boa media mesmo errado, por exemplo, todos os atores
 
 2. Média simples das cobertudas por componentes: weighted_score
    - mostra o nivel de aerto proporcional em relacao ao modelo de referência de forma simples e transparente
    - não penaliza erros por excesso (medido pelos elementos extras apresentados)
    - pode gerar uma nota alta para artefatos incompletos e consistentes em apenas um tipo de componente (ex: atores)
  - 
 3. Média ponderada que incorpora penalidades por excesso e necessidades de edições: overall_weighted_score
   - Masi realista par auso prático pois reflete o esforço para tornar o artefato utilizavel
   - valoriza diagramas "prontos para uso"
   - o ponto negativo é que é mais complexa e pode esconder o modelo que entendeu mas errou detalhes
  
 4. Quantidade bruta de alteracoes necessarias para o diagrama se parecer com o de referência: total_edit_operations
   - Reflete diretamenteo quanto é preciso consertar e está mais alinhada com aplicabilidade do artefato mas de maneira bem mais grosseira
   - permite a analise de aplicabilidade mais simples
   - Não é padroniada e um diagrama com mais operacoes pode estar "menos ruim" do que outro com menos operacoes
   - Altamente dependente da complexidade do sistema modelado e pode ser injusta com sistemas maiores

## Abordagem escolhida
 Analisar a variavel dependente em duas perspectivas: 
 - Cobertura Técnica esperada: captura o quant o modelo entregou dos elementos esperados. Métricass principais: *_coverage e weighted_score
 - Retrabalho para aplicação: captura o quanto o artefato precisa ser corrigido para ser usável. Métricas principais: total_edit_operations e overall_wheited_score

Espero poder fazer analises como:
"O modelo entregou 90% dos elementos esperados, mas exigiu 50 operações de correção, um entendimento parcial da instrucoes tecnicas com sobregeracao de componentes
\text{CT}_\text{final} = \text{weighted_score} \times (1 - \text{normalized edit operations})

## Experimental Design

### 3.1 Hypotheses

#### 3.1.1 Syntactic Correctness (SC)

- **Hipótese Nula (H₀.CS01):** \[H_0: p_1 = p_2\]
  
*There is no statistically significant difference between the proportion of diagrams that compile correctly in PlantUML generated by the CED-specialized LLM model (\(p_1\)) and the non-specialized LLM model (\(p_2\)).*

- **Hipótese Alternativa (H₁.CS01):** \[H_1: p_1 \neq p_2\]

*There is a statistically significant difference between the proportions of diagrams that compile correctly in PlantUML generated by the CED-specialized LLM model (\(p_1\)) and the non-specialized LLM model (\(p_2\)).*


#### 3.1.2 Completude Técnica (TC)

- **Hipótese Nula (H₀.CT01)**: \[H_0: p_1 = p_2\]
  *A completude técnica média dos diagramas gerados por LLM especializados em CED é igual à dos diagramas gerados por LLM não especializado.*

- **Hipótese Alternativa (H₁.CT01)**:\[H_0: p_1 \neq p_2\]
  *A completude técnica média dos diagramas gerados por LLM especializados em CED é diferente da dos diagramas gerados por LLM não especializado.*


#### 3.1.3 Coerência Semântica com o Domínio (CSD)

- **H0.CSD01**: μ₁_coer = μ₂_coer*A média da coerência semântica com o domínio dos diagramas de casos de uso gerados por LLM especializado em CED é igual àquela gerada por LLM não especializado.*
- **H1.CSD02**: μ₁_coer > μ₂_coer
  *A média da coerência semântica com o domínio dos diagramas de casos de uso gerados por LLM especializado em CED é maior do que a gerada por LLM não especializado.*

#### 3.1.4 Articulação Técnico-Conceitual (ATC)

- **H0.ACT01**: μ₁_artic = μ₂_artic*A média da articulação técnico-conceitual dos diagramas de casos de uso gerados por LLM especializado em CED é igual àquela gerada por LLM não especializado.*
- **H1.ACT01**: μ₁_artic > μ₂_artic
  *A média da articulação técnico-conceitual dos diagramas de casos de uso gerados por LLM especializado em CED é maior do que a gerada por LLM não especializado.*

**Onde**:

- μ₁_* representa a média da variável * para o grupo com LLM especializado em CED;
- μ₂_* representa a média da variável * para o grupo com LLM não especializado;
- Todas as hipóteses assumem um **delineamento unifatorial com dois tratamentos independentes**: LLM especializado vs. LLM não especializado.

## Plan Definitions

### Analise estatistica de SC

### Análise estatistica de CT

#### Cobertura tecnica
Teste de normalidade: só deve ser aplicado nsa variáveis actors_coverage, usecases_coverage, relationships_coverage e weighted_score ← principal proxy de cobertura técnica

Testes estatísticos: Aplicaremos o Teste-t de médias (weighted_score), ou Mann-Whitney e Análise por componente (actors_coverage, usecases_coverage, relationships_coverage e weighted_score)

Teste de diferenças de médias por facetas:
- weighted_score (contínua) => t-test se normal, Mann-Whitney U se não
- actors_coverage (contínua) => t-test se normal, Mann-Whitney U se não

#### Retrabalho técnico
Teste de normalidade só deve ser aplicado nsa variaveis total_edit_operations, e overall_weighted_score ← principal proxy de retrabalho técnico

Testes estatísticos: Aplicaremos o Teste de médias (overall_weighted_score, edit_operations)



## Results

#### Syntactic Correctness (SC)

A especialização teve um impacto negativo na geração de código sintaticamente válido:

-  Z = -8.3188 => indica que a diferença observada está 8.3 desvios-padrão abaixo do esperado se as proporções fossem realmente iguais.
- (|Z| > 1.96 para 95% de confiança).
- O sinal negativo indica que a proporção de sucesso do grupo 1 é menor que a do grupo 2:
  - Grupo 1: LLM especializado | Grupo 2: LLM não especializado
  
- A especialização foi desfavorável a performance sintática do modelo na geração de diagramas de casos de uso na Linguagem PlantUML. A análise foi feita  observando a diferença entre os percentuais de sucesso dos modelos. Foi possível observar a diferença de 15.9 pontos percentuais a favor do modelo não especializado.
  - Sucessos => LLM especializado: 680 / 1000 → 68% comparado a LLM não especializado: 839 / 1000 → 83.9%












Calibração dos Parâmetros dos LLMs
Uma etapa fundamental da preparação experimental consistiu na calibração dos principais hiperparâmetros dos modelos, a saber:

temperature: controla o grau de aleatoriedade das respostas;

top_p: controla a diversidade do vocabulário gerado;

context length: define o tamanho máximo de tokens que podem ser processados na entrada;

output length (num_predict): limita o tamanho da resposta gerada.

Esta calibração foi necessária devido à inexistência, até o momento, de guidelines ou evidências na literatura de Engenharia de Software Empírica que orientem a configuração desses parâmetros para a tarefa específica de geração de artefatos técnicos, como diagramas de casos de uso.

Embora existam estudos que exploram o impacto de parâmetros como temperature e top_p em tarefas de geração textual geral (Brown et al., 2020), não foram encontrados trabalhos que discutam os efeitos destes parâmetros na produção de artefatos estruturados que exigem:

raciocínio técnico;

aplicação adequada de conceitos do domínio;

completude informacional;

organização estrutural.

Objetivo da Calibração
A calibração dos parâmetros buscou equilibrar a capacidade criativa dos modelos — essencial para lidar com variações no domínio — com a necessidade de garantir:

geração de artefatos válidos (com código PlantUML compilável);

ausência de alucinações graves;

redução de incompletudes;

uso adequado de conceitos e elementos técnicos da notação UML.

Dado o cenário de ausência de guidelines formais, a calibração foi conduzida de forma empírica (trial-and-error), por meio de iterações exploratórias com diferentes configurações dos parâmetros. Esse processo envolveu:

A geração de exemplos de diagramas a partir das instruções experimentais;

A análise do comportamento dos modelos em relação a erros sintáticos, inconsistências e inadequações semânticas;

A escolha dos valores de parâmetros que maximizassem a produção de diagramas válidos e interpretáveis.

Parâmetros Finalizados no Experimento
Após o processo de calibração, os seguintes valores foram adotados como padrão de execução para ambos os modelos:


Parâmetro	Valor Final Utilizado
temperature	0.4
top_p	0.8
context length	131072 tokens
num_predict	1024 tokens
Esses valores representaram o melhor equilíbrio identificado empiricamente entre controle de criatividade, consistência estrutural e completude dos diagramas de casos de uso gerados.