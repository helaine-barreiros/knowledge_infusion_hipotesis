# Análise Dos Dados Coletados

- "actors_expected_qtd": representa a quantidade de atores que foram identificados no diagrama de referênca
- "actors_detected_qtd": representa a quantidade de agores que foram identificados no diagrama gerado pelos LLMs
- "actors_balance_qtd": Representa a diferença entre o quantitativo de atores esperados substraido do quantitativo de atores identificados pelo LLM. Se o valor for zero significa que o LLM identificou todos os atores esperados. Se positivo representa o quantitativo de atores que o LLM não identificou e se form negativo indica que o LLM gerou mais atores do que o esperado.
- "actors_coverage": medida em percentual que é calculada pela divisão direta do quantiativo de atores identificados pelo LLM e o quatitativo de atores esperado pelo diagrama de referência.  
- "actors_not_detected_qtd": representa o quantitativo de atores que não foram especificados pelo diagrama gerado pelo LLM.
- "actors_extra_detected_qtd": representa o quantitativo de atores que o LLM especificou além do esperado pelo diagrama de referência,
- "actors_expected_detail": apresenta uma lista dos nomes dos atores considerando a similaridade aplicada. Serve como referência para analisar a sensibilidade da similaridade ,
- "actors_missing_detail": lista que apresenta o nome dos atores que não foram identificados no diagrama gerado pelo LLM,
- "actors_extra_detail": lista que apresenta o nome dos atores que foram cirados pelo LLM e que não eram esperados no modelo de referência,,

- "usecases_expected_qtd": representa a quantidade de casos de uso que foram identificados no diagrama de referênca,
- "usecases_detected_qtd": representa a quantidade de casos de uso que foram identificados no diagrama gerado pelos LLMs,
- "usecases_balance_qtd": Representa a diferença entre o quantitativo de casos de uso esperados substraido do quantitativo de casos de uso identificados pelo LLM. Se o valor for zero significa que o LLM identificou todos os casos de uso esperados. Se positivo representa o quantitativo de casos de uso que o LLM não identificou e se for negativo indica que o LLM gerou mais casos de uso do que o esperado,
- "usecases_coverage": medida em percentual que é calculada pela divisão direta do quantiativo de casos de uso identificados pelo LLM e o quantitativo de casos de uso esperado pelo modelo de referência.  ,
- "usecases_not_detected_qtd": representa o quantitativo de casos de uso que não foram especificados pelo diagrama gerado pelo LLM.,
- "usecases_extra_detected_qtd": representa o quantitativo de casos de uso que o LLM especificou além do esperado pelo diagrama de referência,
- "usecases_expected_detail": apresenta uma lista dos nomes dos casos de uso considerando a similaridade aplicada. Serve como referência para analisar a sensibilidade da similaridade,
- "usecases_missing_detail": lista que apresenta o nome dos casos de uso que não foram identificados no diagrama gerado pelo LLM,
- "usecases_extra_detail": lista que apresenta o nome dos casos de uso que foram criados pelo LLM e que não eram esperados no modelo de referência,

- "relationships_expected_qtd": representa a quantidade de relacionamentos que foram identificados no diagrama de referênca,
- "relationships_detected_qtd": representa a quantidade de relacionamentos que foram identificados no diagrama gerado pelos LLMs,
- "relationships_balance_qtd": Representa a diferença entre o quantitativo de relacionamentos esperados substraido do quantitativo de relacionamentos identificados pelo LLM. Se o valor for zero significa que o LLM identificou todos os relacionamentos esperados. Se positivo representa o quantitativo de relacionamentos que o LLM não identificou e se for negativo indica que o LLM gerou mais relacionamentos do que o esperado,
- "relationships_coverage": medida em percentual que é calculada pela divisão direta do quantiativo de relacionamentos identificados pelo LLM e o quantitativo de relacionamentos esperado pelo modelo de referência,
- "relationships_not_detected_qtd": representa o quantitativo de relacionamentos que não foram especificados pelo diagrama gerado pelo LLM,
- "relationships_extra_detected_qtd": representa o quantitativo de relacionamentos que o LLM especificou além do esperado pelo diagrama de referência,
- "relationships_expected_detail": apresenta uma lista dos nomes dos relacionamentos considerando a similaridade aplicada. Serve como referência para analisar a sensibilidade da similaridade,
- "relationships_missing_detail": lista que apresenta o nome dos relacionamentos que não foram identificados no diagrama gerado pelo LLM,
- "relationships_extra_detail": lista que apresenta o nome dos relacionamentos que foram criados pelo LLM e que não eram esperados no modelo de referência,

- "elements_expected": {"actors": 0, "use_cases": 0, "relationships": 0} apresenta os quantitativos de atores, casos de uso e relacionamentos no diagrama de referência,
- "elements_to_add": {"actors": 0, "use_cases": 0, "relationships": 0} apresenta os quantitativos de atores, casos de uso e relacionamentos que não foram identificados pelos LLM e precisariam de intervenção do engenheiro de software para acrescentar no diagrama gerado. Uma das partes que dimensiona o quantitativo do retrabalho, no caso para acrescentar itens que não foram identificados.,
- "elements_to_delete": {"actors": 0, "use_cases": 0, "relationships": 0} apresenta os quantitativos de atores, casos de uso e relacionamentos que precisariam ser analisados pelo engenheiro para saber se seriam removidos (por não fazerem sentido) ou se deveriam ser acrescentados (caso em que o LLM teria identificado atores, casos de uso ou relacionamentos que façam sentido e não foram especificados pelo diagrama de referência. Um caso onde por exemplo o LLM fez um bom raciocinio sobre o conhecimento especifico do domínio ou de conhecimento técnico),
- "total_add_operations": somatorio do quantitativos de atores, casos de uso e relacionamentos que precisam ser adicionados ao diagrama gerado pelo LLM,
- "total_delete_operations": somatorio do quantitativo de atores, casos de uso e relacionamentos que divergem do diagrama de referencia e precisam ser analisados pelo engenheiro de software para saber se precisam ser removidos ou adicionados, a depende da analise.
- "total_edit_operations": um somatorio das ediçoes/análises que precisam ser feitas pelo engenheiro de software para deixar o diagrama gerado pelo LLM conforme o diagrama de referência.,

- "weighted_score": Faz uma média simples do retrabalho necessário pelo engenheiro para adequar o diagrama gerado pelo LLM ao diagrama de referência. É calculada assim: arithimetic_avg_for_detected_components = (detected_actor_coverage + detected_usecase_coverage + detected_relationships_coverage) / 3
- "overall_weighted_score": calculo ponderado do retrabalho necessário pelo engenheiro para adequar o diagrama gerado pelo LLM ao diagrama de referência. Para chegar neste valor considerei uma distrubuição ponderada do esforço para fazer isto. EU considerei uma estrutura de pesos assim:
weights = {
    "add_actor": 0.67,
    "add_usecase": 1.0,
    "delete_actor": 0.53,
    "delete_usecase": 0.8,
    "add_relationship": 0.87,
    "delete_relationship": 0.67
}

O cálculo foi feito da seguinte forma:

weighted_raw_score = (
    weights["add_actor"] * elements_to_add["actors"] +
    weights["add_usecase"] * elements_to_add["use_cases"] +
    weights["add_relationship"] * elements_to_add["relationships"] +
    weights["delete_actor"] * elements_to_delete["actors"] +
    weights["delete_usecase"] * elements_to_delete["use_cases"] +
    weights["delete_relationship"] * elements_to_delete["relationships"]
)

normalized_score = weighted_raw_score / max(total_elements_reference, 1) 

return min(normalized_score, 1.0)

A tabela de interpretação de valores foi definida dessa forma:
   Score | Interpretação prática
    0.00 - 0.20 | Can be used directly
    0.21 - 0.40 | Requires some light adjustments
    0.41 - 0.60 | Requires moderate rework, still viable
    0.61 - 0.80 | Requires heavy rework, reevaluate reuse
    0.81 - 1.00 | Better to start from scratch,
- "code_similarity": faz uma análise de similaridade textual entre dois códigos plantuml usando sentence transformer .