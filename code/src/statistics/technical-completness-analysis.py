
from scipy.stats import shapiro, normaltest, anderson, ttest_ind, mannwhitneyu
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from datetime import datetime

import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import os
import pandas as pd


def create_prepared_data():
    # Leitura da planilha original
    df = pd.read_excel("selected_data_cs_test1.xlsx")

    # Seleção das colunas relevantes conforme o dicionário de dados (Completude Técnica)
    cols_to_keep = [
        "model", "actors_coverage", "usecases_coverage", "relationships_coverage",
        "actors_expected_qtd", "actors_detected_qtd",
        "usecases_expected_qtd", "usecases_detected_qtd",
        "relationships_expected_qtd", "relationships_detected_qtd",
        "elements_to_add", "elements_to_delete", "total_edit_operations",
        "weighted_score", "overall_weighted_score"
    ]

    # Garante que as colunas existam antes de tentar extrair
    available_cols = [col for col in cols_to_keep if col in df.columns]
    prepared_df = df[available_cols].copy()

    # Gerar nome do novo arquivo
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    new_filename = f"selected_data_cs_test1_completeness_{timestamp}.xlsx"

    # Salvar nova planilha
    prepared_df.to_excel(new_filename, index=False)
    print(f"Prepared data saved to: {new_filename}")

    return prepared_df, timestamp, new_filename


def apply_normality_tests(df):
    columns_to_test = [
        "weighted_score", "actors_coverage", "usecases_coverage",
        "relationships_coverage", "total_edit_operations",
        "overall_weighted_score"
    ]

    results = {}

    for col in columns_to_test:
        data = df[col].dropna()
        interpretation = {}

        # Shapiro-Wilk Test
        try:
            shapiro_stat, shapiro_p = shapiro(data)
            interpretation['shapiro'] = {
                'stat': round(shapiro_stat, 4),
                'p_value': round(shapiro_p, 4),
                'interpretation': "Data likely normal" if shapiro_p >= 0.05 else "Data not normal"
            }
        except Exception as e:
            interpretation['shapiro'] = {
                'error': str(e)
            }

        # D’Agostino and Pearson’s test
        try:
            dagostino_stat, dagostino_p = normaltest(data)
            interpretation['dagostino'] = {
                'stat': round(dagostino_stat, 4),
                'p_value': round(dagostino_p, 4),
                'interpretation': "Data likely normal" if dagostino_p >= 0.05 else "Data not normal"
            }
        except Exception as e:
            interpretation['dagostino'] = {
                'error': str(e)
            }

        # Anderson-Darling Test
        try:
            anderson_result = anderson(data, dist='norm')
            interpretation['anderson'] = {
                'stat': round(anderson_result.statistic, 4),
                'critical_values': anderson_result.critical_values.tolist(),
                'significance_levels': anderson_result.significance_level.tolist(),
                'interpretation': "Data not normal" if anderson_result.statistic > anderson_result.critical_values[2] else "Data likely normal"
            }
        except Exception as e:
            interpretation['anderson'] = {
                'error': str(e)
            }

        results[col] = interpretation

    return results


def choose_statistical_test(normality_results):
    analysis = {}

    for variable, tests in normality_results.items():
        details = {}
        justification = []

        # Inicialização dos indicadores
        shapiro_is_normal = False
        dagostino_is_normal = False
        anderson_is_normal = False

        # Verificar p-valor do Shapiro
        if 'shapiro' in tests and 'p_value' in tests['shapiro']:
            shapiro_p = tests['shapiro']['p_value']
            shapiro_is_normal = shapiro_p >= 0.05
            justification.append(f"Shapiro-Wilk p = {shapiro_p:.4f} ⇒ {'normal' if shapiro_is_normal else 'not normal'}")

        # Verificar p-valor do D’Agostino
        if 'dagostino' in tests and 'p_value' in tests['dagostino']:
            dagostino_p = tests['dagostino']['p_value']
            dagostino_is_normal = dagostino_p >= 0.05
            justification.append(f"D’Agostino p = {dagostino_p:.4f} ⇒ {'normal' if dagostino_is_normal else 'not normal'}")

        # Verificar resultado do Anderson
        if 'anderson' in tests and 'stat' in tests['anderson']:
            anderson_stat = tests['anderson']['stat']
            anderson_crit = tests['anderson']['critical_values'][2]  # 5% nível
            anderson_is_normal = anderson_stat < anderson_crit
            justification.append(f"Anderson stat = {anderson_stat:.4f} < critical (5%) = {anderson_crit:.4f} ⇒ {'normal' if anderson_is_normal else 'not normal'}")

        # Decisão com base na maioria dos testes
        normal_votes = sum([shapiro_is_normal, dagostino_is_normal, anderson_is_normal])
        majority_normal = normal_votes >= 2

        if majority_normal:
            chosen_test = "t-test (parametric)"
            justification.append("Majority of normality tests suggest normal distribution. Parametric test is appropriate.")
        else:
            chosen_test = "Mann-Whitney U test (non-parametric)"
            justification.append("Majority of normality tests suggest non-normal distribution. Non-parametric test is appropriate.")

        # Construção da estrutura de retorno
        details['variable'] = variable
        details['normality_summary'] = {
            "shapiro": tests.get("shapiro", {}),
            "dagostino": tests.get("dagostino", {}),
            "anderson": tests.get("anderson", {})
        }
        details['recommended_test'] = chosen_test
        details['justification'] = justification

        analysis[variable] = details

    return analysis


def apply_statistical_tests(df, test_selection_object):
    results = {}

    for variable, analysis in test_selection_object.items():
        test_type = analysis["recommended_test"]
        col_data = df[[variable, "model"]].dropna()

        # Grupos de comparação
        groups = col_data.groupby("model")[variable]
        group_names = list(groups.groups.keys())

        if len(group_names) != 2:
            results[variable] = {
                "error": "Expected exactly two model groups for comparison"
            }
            continue

        group1_data = groups.get_group(group_names[0])
        group2_data = groups.get_group(group_names[1])

        # Aplicação do teste
        if "t-test" in test_type.lower():
            stat, p_value = ttest_ind(group1_data, group2_data, equal_var=False)
        elif "mann-whitney" in test_type.lower():
            stat, p_value = mannwhitneyu(group1_data, group2_data, alternative='two-sided')
        else:
            stat, p_value = None, None

        # Interpretação do p-valor
        interpretation = "Significant difference (p < 0.05)" if p_value < 0.05 else "No significant difference (p ≥ 0.05)"

        # Estrutura do resultado
        results[variable] = {
            "variable": variable,
            "test_applied": test_type,
            "group_1": group_names[0],
            "group_2": group_names[1],
            "group_1_mean": round(group1_data.mean(), 4),
            "group_2_mean": round(group2_data.mean(), 4),
            "group_1_std": round(group1_data.std(), 4),
            "group_2_std": round(group2_data.std(), 4),
            "statistic": round(stat, 4),
            "p_value": round(p_value, 4),
            "interpretation": interpretation
        }

    return results


def generate_visualizations_for_tests(df, statistical_test_results, output_dir="visualizations"):
    os.makedirs(output_dir, exist_ok=True)
    visualizations = {}

    for variable, result in statistical_test_results.items():
        if "error" in result:
            continue

        var_data = df[[variable, "model"]].dropna()
        model_col = "model"
        var_name = variable
        group_1 = result["group_1"]
        group_2 = result["group_2"]

        images = {}

        # Boxplot
        plt.figure(figsize=(10, 6))

        sns.boxplot(data=df, x="model", y=variable, palette="Set2", fliersize=0)
        sns.stripplot(data=df, x="model", y=variable, color="black", alpha=0.5, jitter=0.2, size=3)

        plt.title(f"Technical Completeness ({variable.replace('_', ' ').title()}) by Model")
        plt.ylabel("Weighted Score (0 to 1)")
        plt.xlabel("LLM Model")

        boxplot_path = os.path.join(output_dir, f"{variable}_boxplot_styled.png")
        plt.tight_layout()
        plt.savefig(boxplot_path)
        plt.close()
        images["boxplot"] = boxplot_path

        # Histograma + KDE
        plt.figure(figsize=(7, 5))
        sns.histplot(data=var_data, x=var_name, hue=model_col, kde=True, stat="density", common_norm=False, bins=20)
        plt.title(f"Histogram and KDE - {var_name}")
        hist_path = os.path.join(output_dir, f"{var_name}_histogram_kde.png")
        plt.savefig(hist_path)
        plt.close()
        images["histogram_kde"] = hist_path

        # QQ-plot
        plt.figure(figsize=(7, 5))
        for label, data in var_data.groupby("model")[variable]:
            stats.probplot(data, dist="norm", plot=plt)
            plt.title(f"QQ-Plot ({label}) - {var_name}")
            qq_path = os.path.join(output_dir, f"{var_name}_qqplot_{label}.png")
            plt.savefig(qq_path)
            plt.close()
            if "qqplots" not in images:
                images["qqplots"] = {}
            images["qqplots"][label] = qq_path

        visualizations[variable] = {
            "variable": variable,
            "test_applied": result["test_applied"],
            "group_1": group_1,
            "group_2": group_2,
            "images": images
        }

    return visualizations


def generate_statistical_analysis_report(
    prepared_data_df,
    normality_results,
    test_selection_results,
    statistical_test_results,
    visualizations_dict,
    output_filename="statistical_analysis_report.pdf"
):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT, fontName='Helvetica', leading=14))

    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    content = []

    # 1. Introdução
    content.append(Paragraph("Statistical Report – Completude Técnica", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("This report analyzes whether domain-specific specialization of a Large Language Model (LLM) affects its ability to correctly interpret technical prompts and generate complete and usable software artifacts, in this case, Use Case Diagrams.", styles['Justify']))
    content.append(Spacer(1, 12))

    # 2. Variáveis Dependentes e Facetas
    content.append(Paragraph("1. Variables and Facets", styles['Heading2']))
    content.append(Paragraph("Completude Técnica is analyzed as a composed construct with two analytical facets:", styles['Justify']))
    content.append(Paragraph("• Coverage of Expected Technical Elements – represented by weighted_score and its components (actors_coverage, usecases_coverage, relationships_coverage).", styles['Justify']))
    content.append(Paragraph("• Technical Rework – measured by total_edit_operations and overall_weighted_score.", styles['Justify']))
    content.append(Spacer(1, 12))

    # 3. Testes de Normalidade
    content.append(Paragraph("2. Normality Tests", styles['Heading2']))
    for var, res in normality_results.items():
        content.append(Paragraph(f"<b>{var}</b>", styles['Heading3']))
        for test_name, values in res.items():
            if "p_value" in values:
                interp = values.get("interpretation", "")
                content.append(Paragraph(f"{test_name.title()}: stat = {values['stat']:.4f}, p = {values['p_value']:.4f} → {interp}", styles['Justify']))
            elif "stat" in values:
                interp = values.get("interpretation", "")
                content.append(Paragraph(f"{test_name.title()}: stat = {values['stat']:.4f} → {interp}", styles['Justify']))
        content.append(Spacer(1, 6))
    content.append(PageBreak())

    # 4. Escolha dos Testes
    content.append(Paragraph("3. Test Selection Based on Normality", styles['Heading2']))
    for var, details in test_selection_results.items():
        content.append(Paragraph(f"<b>{var}</b>: Recommended test → {details['recommended_test']}", styles['Heading3']))
        for line in details['justification']:
            content.append(Paragraph(line, styles['Justify']))
        content.append(Spacer(1, 8))

    # 5. Resultados Estatísticos
    content.append(Paragraph("4. Statistical Test Results", styles['Heading2']))
    for var, res in statistical_test_results.items():
        if "error" in res:
            content.append(Paragraph(f"<b>{var}</b>: Error – {res['error']}", styles['Justify']))
        else:
            content.append(Paragraph(f"<b>{var}</b>", styles['Heading3']))
            content.append(Paragraph(f"Test: {res['test_applied']}", styles['Justify']))
            content.append(Paragraph(f"{res['group_1']}: Mean = {res['group_1_mean']}, SD = {res['group_1_std']}", styles['Justify']))
            content.append(Paragraph(f"{res['group_2']}: Mean = {res['group_2_mean']}, SD = {res['group_2_std']}", styles['Justify']))
            content.append(Paragraph(f"Statistic = {res['statistic']}, p = {res['p_value']}", styles['Justify']))
            content.append(Paragraph(f"Interpretation: {res['interpretation']}", styles['Justify']))
            content.append(Spacer(1, 10))

    content.append(PageBreak())

    # 6. Visualizações
    content.append(Paragraph("5. Data Visualizations", styles['Heading2']))
    for var, imgs in visualizations_dict.items():
        content.append(Paragraph(f"<b>{var}</b>", styles['Heading3']))
        if "boxplot" in imgs["images"]:
            content.append(Paragraph("Boxplot:", styles['Normal']))
            content.append(Image(imgs["images"]["boxplot"], width=400, height=200))
        if "histogram_kde" in imgs["images"]:
            content.append(Paragraph("Histogram + KDE:", styles['Normal']))
            content.append(Image(imgs["images"]["histogram_kde"], width=400, height=200))
        if "qqplots" in imgs["images"]:
            for model_name, path in imgs["images"]["qqplots"].items():
                content.append(Paragraph(f"QQ-Plot for {model_name}:", styles['Normal']))
                content.append(Image(path, width=400, height=200))
        content.append(PageBreak())

    # 7. Discussão Integrada
    content.append(Paragraph("6. Integrated Discussion", styles['Heading2']))
    content.append(Paragraph("The combination of statistical results and visual diagnostics suggests whether the domain-specific specialization of the LLM improved its ability to interpret and apply software engineering instructions in the generation of Use Case Diagrams.", styles['Justify']))
    content.append(Paragraph("Special attention should be given to variables such as weighted_score and total_edit_operations, which represent the effectiveness and the practical usability of the generated artifacts respectively.", styles['Justify']))
    content.append(Spacer(1, 12))

    # 8. Conclusão Final
    content.append(Paragraph("7. Final Conclusion", styles['Heading2']))
    content.append(Paragraph("Statistical evidence points to...", styles['Justify']))  # aqui você pode customizar conforme os resultados
    content.append(Paragraph("Future work may explore...", styles['Justify']))

    doc.build(content)
    print(f"Report saved to: {output_filename}")


def main():
    df, timestamp, new_filename = create_prepared_data()

    normality_tests_results = apply_normality_tests(df)
    choosed_statistical_tests = choose_statistical_test(normality_tests_results)
    statystical_testes_results = apply_statistical_tests(df, choosed_statistical_tests)
    visualizations_dict = generate_visualizations_for_tests(df, statystical_testes_results)

    generate_statistical_analysis_report(df, normality_tests_results, choosed_statistical_tests, statystical_testes_results, visualizations_dict)

if __name__ == "__main__":
    main()
