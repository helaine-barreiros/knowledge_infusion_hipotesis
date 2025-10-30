
import pandas as pd
import scipy.stats as stats
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.proportion import proportions_ztest
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

def create_contingency_table(df, model_col='model', compiled_col='compiled_diagram', output_dir='.'):
    contingency = pd.crosstab(df[model_col], df[compiled_col])
    now = datetime.now().strftime("%Y-%m-%d-%H%M")
    file_base = os.path.splitext("selected_data_cs_t4k.xlsx")[0]
    contingency_filename = f"{file_base}_contingency_{now}.xlsx"
    contingency.to_excel(os.path.join(output_dir, contingency_filename))
    return contingency, now, contingency_filename, df

def generate_heatmap(contingency):
    chi2, p, dof, expected = stats.chi2_contingency(contingency)
    df_expected = pd.DataFrame(expected, index=contingency.index, columns=contingency.columns)
    df_diff = contingency - df_expected

    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    sns.heatmap(contingency, annot=True, fmt=".0f", cmap="Blues", ax=axes[0])
    axes[0].set_title("Observed Frequencies")
    sns.heatmap(df_expected, annot=True, fmt=".1f", cmap="Greens", ax=axes[1])
    axes[1].set_title("Expected Frequencies (Under H₀)")
    sns.heatmap(df_diff, annot=True, fmt="+.1f", cmap="coolwarm", center=0, ax=axes[2])
    axes[2].set_title("Difference (Observed - Expected)")
    for ax in axes:
        ax.set_xlabel("Compiled?")
        ax.set_ylabel("Model")

    plt.tight_layout()
    heatmap_path = "heatmap_analysis.png"
    plt.savefig(heatmap_path)
    plt.close()
    return heatmap_path, df_expected, df_diff

def generate_pdf_report(contingency, df, timestamp, output_pdf):
    model_names = list(contingency.index)
    successes = contingency[True].values
    nobs = contingency.sum(axis=1).values
    stat, pval = proportions_ztest(successes, nobs, alternative='two-sided')
    prop_1 = successes[0] / nobs[0]
    prop_2 = successes[1] / nobs[1]
    chi2, chi2_p, _, chi2_expected = stats.chi2_contingency(contingency)
    heatmap_path, df_expected, df_diff = generate_heatmap(contingency)

    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_LEFT, fontName='Helvetica'))

    content = []

    # Hypotheses
    content.append(Paragraph("Statistical Analysis Report – Use Case Diagram Compilation", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("Hypotheses", styles['Heading2']))
    content.append(Paragraph("This study investigates whether the domain-specific specialization of a language model affects its ability to generate syntactically valid use case diagrams.", styles['Normal']))
    content.append(Paragraph("H₀ (Null Hypothesis): The proportion of compilable diagrams is the same for both the specialized and non-specialized models (p₁ = p₂).", styles['Normal']))
    content.append(Paragraph("H₁ (Alternative Hypothesis): There is a statistically significant difference in the proportion of compilable diagrams between the two models (p₁ ≠ p₂).", styles['Normal']))
    content.append(Spacer(1, 12))

    # Descriptive Statistics
    content.append(Paragraph("Descriptive Statistics", styles['Heading2']))
    content.append(Paragraph(f"Total number of diagrams analyzed: {len(df)}", styles['Normal']))
    content.append(Paragraph(f"Compiled successfully: {df['compiled_diagram'].sum()} diagrams", styles['Normal']))
    content.append(Paragraph(f"Failed to compile: {(~df['compiled_diagram']).sum()} diagrams", styles['Normal']))
    content.append(Paragraph("These values are essential to understand the baseline distribution before statistical comparison.", styles['Normal']))
    content.append(Spacer(1, 12))
    table_data = [['Model', 'Compiled', 'Total', 'Proportion']]
    for i in range(2):
        table_data.append([
            model_names[i], successes[i], nobs[i], f"{successes[i]/nobs[i]:.4f}"
        ])
    table = Table(table_data, hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                                ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    content.append(table)
    content.append(Spacer(1, 12))

    # Z-Test Result
    content.append(Paragraph("Z-Test Result", styles['Heading2']))
    content.append(Paragraph(f"Z statistic: {stat:.4f}", styles['Normal']))
    content.append(Paragraph(f"p-value: {pval:.4e}", styles['Normal']))
    if pval < 0.02:
        content.append(Paragraph("The result is statistically significant (p < 0.02), indicating that the specialization impacts the model’s performance in a measurable way.", styles['Normal']))
    else:
        content.append(Paragraph("No statistically significant difference detected (p ≥ 0.02), meaning the specialization may not influence the model’s ability to generate compilable diagrams.", styles['Normal']))
    content.append(Spacer(1, 12))

    # Heatmaps
    content.append(Paragraph("Visual Analysis of Frequencies", styles['Heading2']))
    content.append(Image(heatmap_path, width=480, height=180))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Interpretation of Visual Frequencies", styles['Heading3']))
    table_data2 = [["Model", "Observation", "Expected", "Difference"]]
    for i in range(2):
        for col in df_expected.columns:
            table_data2.append([
                f"{model_names[i]} - {col}",
                f"{contingency.loc[model_names[i], col]}",
                f"{df_expected.loc[model_names[i], col]:.1f}",
                f"{df_diff.loc[model_names[i], col]:+.1f}"
            ])
    table2 = Table(table_data2, hAlign='LEFT')
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    content.append(table2)
    content.append(Spacer(1, 12))
    content.append(Paragraph("Key observations reveal that the specialized model underperformed relative to expectations, while the non-specialized model exceeded expectations, suggesting a negative effect of specialization on syntactic validity.", styles['Normal']))
    content.append(Spacer(1, 12))

    # Chi-Square Result
    content.append(Paragraph("Chi-Square Test Result", styles['Heading2']))
    content.append(Paragraph(f"Chi² statistic: {chi2:.4f}", styles['Normal']))
    content.append(Paragraph(f"p-value: {chi2_p:.4e}", styles['Normal']))
    if chi2_p < 0.02:
        content.append(Paragraph("This test confirms a statistically significant association between the type of model and the likelihood of generating compilable diagrams. It reinforces the Z-Test result by highlighting the dependency between model type and syntax success.", styles['Normal']))
    else:
        content.append(Paragraph("No significant association was found between model type and compilation outcome. This weakens the argument that specialization influences performance.", styles['Normal']))
    content.append(Spacer(1, 12))

    # Final Conclusion
    content.append(Paragraph("Integrated Conclusion", styles['Heading2']))
    if prop_1 > prop_2:
        content.append(Paragraph(f"The specialized model ({model_names[0]}) showed superior syntactic correctness, suggesting that the domain knowledge contributed positively to performance.", styles['Normal']))
    elif prop_1 < prop_2:
        content.append(Paragraph(f"The non-specialized model ({model_names[1]}) compiled more diagrams correctly. This contradicts the expected advantage of specialization, suggesting that the added complexity may have introduced noise or rigid patterns.", styles['Normal']))
    else:
        content.append(Paragraph("Both models performed equally, indicating that specialization had no measurable impact in this experiment.", styles['Normal']))

    doc.build(content)

def main():
    df = pd.read_excel("selected_data_cs_test1.xlsx")
    contingency, timestamp, contingency_filename, df = create_contingency_table(df)
    pdf_filename = f"syntactical_analysis_report_{timestamp}_v3.pdf"
    generate_pdf_report(contingency, df, timestamp, pdf_filename)
    print(f"Final PDF report generated: {pdf_filename}")

if __name__ == "__main__":
    main()
