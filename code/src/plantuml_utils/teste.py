import subprocess
import json
import os
import tempfile

from src.plantuml_utils.plantuml_parser_use_case import PlantUMLUseCaseParser

def parse_plantuml(plantuml_text):
    # Descobrir o caminho do módulo plantuml-parser global
    try:
        # Obter o caminho do módulo global
        process = subprocess.Popen(
            ['npm', 'root', '-g'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(f"Erro ao obter o caminho global do npm: {stderr.decode()}")

        global_modules_path = stdout.decode().strip()
        module_path = os.path.join(global_modules_path, 'plantuml-parser-hsl')

        # Criar um arquivo temporário para o script Node.js
        with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w') as f:
            js_file = f.name
            f.write(f'''
            const {{ parse }} = require('{module_path}');

            const data = process.argv[2];
            const options = {{ f: 'usecase_structured' }};
            try {{
                const result = parse(data, options);
                console.log(JSON.stringify(result));
            }} catch (error) {{
                console.error(JSON.stringify({{error: error.message}}));
                process.exit(1);
            }}
            ''')

        # Executar o script Node.js com o texto PlantUML como argumento
        process = subprocess.Popen(
            ['node', js_file, plantuml_text],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            if stderr:
                try:
                    error_json = json.loads(stderr.decode())
                    raise Exception(f"Erro ao analisar PlantUML: {error_json.get('error', 'Erro desconhecido')}")
                except json.JSONDecodeError:
                    raise Exception(f"Erro ao analisar PlantUML: {stderr.decode()}")
            else:
                raise Exception("Erro desconhecido ao analisar PlantUML")

        # Converter o resultado JSON para um objeto Python
        result = json.loads(stdout.decode())
        return result
    finally:
        # Limpar arquivo temporário
        if 'js_file' in locals():
            try:
                os.unlink(js_file)
            except:
                pass


def run_plantuml_parser(fullname_plantuml_file: str) -> dict:
    result = []

    command = ['plantuml-parser-hsl', '-i', fullname_plantuml_file, '-f', "usecase_structured"]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return json.loads(result.stdout)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error executing  parser:\n{e.stderr}") from e

    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid output (is not JSON): {e}\nOutput:\n{result.stdout}") from e

    return result

def extract_components_from_plantuml_json(parsed_data):
    """
    Extrai componentes de um diagrama de caso de uso PlantUML parseado,
    classificando os elementos pela estrutura de atributos no JSON.
    """
    result = {
        'actors': [],         # Lista de atores 
        'usecases': [],       # Lista de casos de uso
        'packages': [],       # Lista de pacotes
        'rectangles': [],     # Lista de retângulos (contêineres)
        'relationships': [],  # Lista de relacionamentos
        'comments': []        # Lista de comentários
    }
    
    # Conjunto para rastrear IDs já processados e evitar duplicação
    processed_ids = set()
    
    # Função para classificar e processar elementos
    def process_elements(elements_list, parent=None):
        for element in elements_list:
            # Verifica se é um retângulo
            if (isinstance(element, dict) and 
                'name' in element and 
                'title' in element and 
                'type' in element and 
                element['type'] == 'rectangle' and 
                'elements' in element):
                
                rectangle_id = element['name']
                if rectangle_id not in processed_ids:
                    rectangle_info = {
                        'id': rectangle_id,
                        'name': element['title'],
                        'container': parent,
                        'elements': []  # IDs dos elementos contidos
                    }
                    result['rectangles'].append(rectangle_info)
                    processed_ids.add(rectangle_id)
                
                # Processa elementos dentro do retângulo
                process_elements(element['elements'], rectangle_id)
            
            # Verifica se é um pacote
            elif (isinstance(element, dict) and 
                  'name' in element and 
                  'title' in element and 
                  'type' in element and 
                  element['type'] == 'package' and 
                  'elements' in element):
                
                package_id = element['name']
                if package_id not in processed_ids:
                    package_info = {
                        'id': package_id,
                        'name': element['title'],
                        'container': parent,
                        'elements': []  # IDs dos elementos contidos
                    }
                    result['packages'].append(package_info)
                    processed_ids.add(package_id)
                
                # Processa elementos dentro do pacote
                process_elements(element['elements'], package_id)
            
            # Verifica se é um caso de uso
            elif (isinstance(element, dict) and 
                  'name' in element and 
                  'title' in element and 
                  'type' not in element):
                
                usecase_id = element['name']
                if usecase_id not in processed_ids:
                    usecase_info = {
                        'id': usecase_id,
                        'name': element['title'],
                        'container': parent
                    }
                    result['usecases'].append(usecase_info)
                    processed_ids.add(usecase_id)
                    
                    # Adiciona ao elemento pai (pacote ou retângulo)
                    if parent:
                        for container in result['packages'] + result['rectangles']:
                            if container['id'] == parent:
                                container['elements'].append(usecase_id)
                                break
            
            # Verifica se é um relacionamento
            elif (isinstance(element, dict) and 
                  'left' in element and 
                  'right' in element and
                  'leftArrowHead' in element and
                  'rightArrowHead' in element and
                  'leftArrowBody' in element and
                  'rightArrowBody' in element):
                
                # Determina o tipo de relacionamento com base nas setas
                rel_type = 'association'
                if element['leftArrowHead'] == '<|':
                    rel_type = 'inheritance'
                elif element['rightArrowHead'] == '<|':
                    rel_type = 'inheritance'
                elif element['leftArrowHead'] == '<' and element['rightArrowHead'] == '>':
                    rel_type = 'bidirectional'
                elif element['leftArrowHead'] == '<':
                    rel_type = 'association_reverse'
                elif element['rightArrowHead'] == '>':
                    rel_type = 'association'
                
                relationship = {
                    'from': element['left'],
                    'to': element['right'],
                    'type': rel_type,
                    'leftArrowHead': element['leftArrowHead'],
                    'rightArrowHead': element['rightArrowHead'],
                    'leftArrowBody': element['leftArrowBody'],
                    'rightArrowBody': element['rightArrowBody']
                }
                result['relationships'].append(relationship)
            
            # Verifica se é um comentário
            elif isinstance(element, dict) and 'comment' in element:
                comment_info = {
                    'text': element['comment']
                }
                result['comments'].append(comment_info)
    
    # Começa pelo nível raiz
    if parsed_data and len(parsed_data) > 0:
        main_element = parsed_data[0]
        if 'elements' in main_element:
            process_elements(main_element['elements'])
    
    # Identifica atores: elementos que aparecem nos relacionamentos mas não são casos de uso
    usecase_ids = {usecase['id'] for usecase in result['usecases']}
    actor_ids = set()
    
    for relationship in result['relationships']:
        for endpoint in [relationship['from'], relationship['to']]:
            if endpoint not in usecase_ids and endpoint not in actor_ids:
                actor_info = {
                    'id': endpoint,
                    'name': endpoint,
                }
                result['actors'].append(actor_info)
                actor_ids.add(endpoint)
    
    return result


def extract_elements(json_data):
    """
    Extracts and categorizes elements from PlantUML JSON structure
    
    Args:
        json_data (list): Parsed JSON data from PlantUML
        
    Returns:
        dict: Categorized elements in specified structure
    """
    result = {
        'actors': [],
        'usecases': [],
        'packages': [],
        'rectangles': [],
        'relationships': []
    }
    
    # Set to track use case IDs to help identify actors
    usecase_ids = set()
    
    def process_element(element):
        # Process Rectangle
        if isinstance(element, dict) and element.get('type') == 'rectangle':
            rect_info = {
                'id': element['name'],
                'name': element['title'],
                'elements': []  # Store nested elements IDs
            }
            result['rectangles'].append(rect_info)
            
            # Process nested elements
            if 'elements' in element:
                for nested in element['elements']:
                    process_element(nested)
                    # If nested element is a use case, add its ID to rectangle's elements
                    if 'name' in nested and 'type' not in nested:
                        rect_info['elements'].append(nested['name'])
        
        # Process Package
        elif isinstance(element, dict) and element.get('type') == 'package':
            pkg_info = {
                'id': element['name'],
                'name': element['title'],
                'elements': []  # Store nested elements IDs
            }
            result['packages'].append(pkg_info)
            
            # Process nested elements
            if 'elements' in element:
                for nested in element['elements']:
                    process_element(nested)
                    # If nested element is a use case, add its ID to package's elements
                    if 'name' in nested and 'type' not in nested:
                        pkg_info['elements'].append(nested['name'])
        
        # Process Use Case
        elif isinstance(element, dict) and 'name' in element and 'title' in element and 'type' not in element:
            usecase_info = {
                'id': element['name'],
                'name': element['title']
            }
            result['usecases'].append(usecase_info)
            usecase_ids.add(element['name'])
        
        # Process Relationship
        elif (isinstance(element, dict) and 
            'left' in element and 
            'right' in element and
            'leftArrowHead' in element and
            'rightArrowHead' in element and
            'leftArrowBody' in element and
            'rightArrowBody' in element):
            
            # Determine relationship type using the new method
            rel_type = _determine_relationship_type(element)
            
            # Create relationship object
            relationship = {
                'source': element['left'],
                'target': element['right'],
                'type': rel_type,
                'label': element.get('label', ''),
                'leftArrowHead': element['leftArrowHead'],
                'rightArrowHead': element['rightArrowHead'],
                'leftArrowBody': element['leftArrowBody'],
                'rightArrowBody': element['rightArrowBody']
            }
            result['relationships'].append(relationship)
    
    # Process root elements
    if json_data and len(json_data) > 0:
        main_element = json_data[0]
        if 'elements' in main_element:
            for element in main_element['elements']:
                process_element(element)
    
    # Identify actors from relationships
    actor_ids = set()
    for rel in result['relationships']:
        for endpoint in [rel['source'], rel['target']]:
            if endpoint not in usecase_ids and endpoint not in actor_ids:
                actor_info = {
                    'id': endpoint,
                    'name': endpoint
                }
                result['actors'].append(actor_info)
                actor_ids.add(endpoint)
    
    return result


def _determine_relationship_type(element: dict) -> str:
    """
    Determines the relationship type based on labels and arrow notations.
    
    Args:
        element (dict): Relationship element containing arrow and label information
        
    Returns:
        str: The determined relationship type
    """
    # Check label-based relationships first
    if 'label' in element and element['label']:
        label_lower = element['label'].lower()
        if '<<include>>' in label_lower:
            return 'include'
        elif '<<extend>>' in label_lower:
            return 'extend'
    
    # Check arrow-based relationships
    left_head = element['leftArrowHead']
    right_head = element['rightArrowHead']
    left_body = element['leftArrowBody']
    right_body = element['rightArrowBody']
    
    # Define relationship patterns
    ARROW_PATTERNS = {
        'generalization': lambda: left_head == '<|' or right_head == '<|',
        'dependency': lambda: left_body == '.' or right_body == '.',
        'bidirectional': lambda: left_head == '<' and right_head == '>',
        'association_reverse': lambda: left_head == '<' and right_head != '>',
        'association': lambda: right_head == '>' and left_head != '<'
    }
    
    # Check patterns in order of specificity
    for rel_type, check_pattern in ARROW_PATTERNS.items():
        if check_pattern():
            return rel_type
            
    return 'association'  # Default relationship type


# Seu código PlantUML (já fornecido)
plantuml_text = '''
@startuml
left to right direction

title Use Case Diagram for AI-Powered Analysis & Insights System

actor Client as C1
actor SysAdmin as SA
actor FinancialAdvisor as FA
system Syst : "System"

rectangle "Client" {
  usecase "CFR001: View Financial Insights Dashboard" as CFR001
  usecase "CFR002: Receive Alerts for Anomalous Transactions" as CFR002
  usecase "CFR003: View Financial Predictions Based on Historical Data and Market Trends" as CFR003
  usecase "CFR004: Get Personalized Recommendations Aligned with Financial Profile" as CFR004
  usecase "CFR005: Manage Preferences for Personalized Recommendations" as CFR005
  usecase "CFR006: View Spending Limit Alerts Exceeding Predefined Thresholds" as CFR006
  usecase "CFR007: Access Investment Opportunities Based on Risk Profile (MiFID II)" as CFR007
  usecase "CFR008: View News Related to Portfolio" as CFR008
  usecase "CFR009: Manage Relationship with Financial Advisors Including Data Sharing Permissions" as CFR009

}

rectangle "System Administrator" {
  usecase "SAFR001: Manage Analysis Parameters for AI System" as SAFR001
  
}
  
rectangle "Financial Advisor" {
  usecase "FAFR001: Manage Client Mentoring Sessions Based on Insights" as FAFR001
  usecase "FAFR002: View Client Intervention Alerts from System" as FAFR002
  usecase "FAFR003: View Predictive Analytics for Clients' Financial Situations" as FAFR003
  usecase "FAFR004: Configure Analysis Parameters by Client Segment" as FAFR004
  
}

rectangle "System (Syst)" {
  usecase "SFR001: Deliver Alerts Through Notification Channels" as SFR001
  usecase "SFR002: Provide Personalized Recommendations Based on Profiles" as SFR002
  usecase "SFR003: Request Financial Predictions from AI Component" as SFR003
  usecase "SFR004: Request Personalized Recommendations From AI Component" as SFR004
  usecase "SFR005: Request Spending Limit Alerts When Exceeding Thresholds" as SFR005
  usecase "SFR006: Request Investment Opportunity Analysis Based on Risk Profile" as SFR006
  usecase "SFR007: Find Specific Investments Matching User Criteria and ESG Preferences" as SFR007
  usecase "SFR008: Detect Anomaly Transaction Alerts for Fraud Prevention (AML)" as SFR008
  usecase "SFR009: Extract Contextualized News Relevant to Portfolio" as SFR009
  usecase "SFR010: Generate Client Dashboards with Financial Information" as SFR010
  usecase "SFR011: Process Contextualized News Insights for Users' Portfolios" as SFR011
  usecase "SFR012: Request Predictive Intervention Analyses from AI Component" as SFR012
  usecase "SFR013: Track Financial Goals and Progress" as SFR013
  usecase "SFR014: Maintain Historical Record of Insights for Trend Analysis" as SFR014
  usecase "SFR015: Manage User Feedback to Improve System Quality" as SFR015

}

rectangle "AI Component (AIFR)" {
  usecase "AIFR001: Generate Financial Predictions Based on Historical Data and Market Trends" as AIFR001
  usecase "AIFR002: Provide Personalized Recommendations Aligning with User Profiles" as AIFR002
  usecase "AIFR003: Identify Spending Limit Alerts for Unusual Activity" as AIFR003
  usecase "AIFR004: Evaluate Investment Opportunities Against Risk Profiles and Goals" as AIFR004
  usecase "AIFR005: Select Investments Aligning with User Strategies (MPT)" as AIFR005
  usecase "AIFR006: Detect Anomalous Transactions in Compliance with FinCEN Rules" as AIFR006
  usecase "AIFR007: Correlate Financial News with Portfolios for Relevant Insights" as AIFR007
  usecase "AIFR008: Recommend Timing of Intervention Based on Client Patterns" as AIFR008
  usecase "AIFR009: Provide Forward-Looking Analysis to Enhance Financial Planning" as AIFR009
  
}

C1 --> CFR001 : "View financial insights dashboard"
C1 --> CFR002 : "Receive alerts for anomalous transactions"
C1 --> CFR003 : "View financial predictions based on historical data and market trends"
C1 --> CFR004 : "Get personalized recommendations aligned with profile"
C1 --> CFR005 : "Manage preferences for personalized recommendations"
C1 --> CFR006 : "View spending limit alerts exceeding thresholds"
C1 --> CFR007 : "Access investment opportunities based on risk profile (MiFID II)"
C1 --> CFR008 : "View news related to portfolio"
C1 --> CFR009 : "Manage relationship with financial advisors, including data sharing"

SA --> SAFR001 : "Manage analysis parameters for AI system"

FA --> FAFR001 : "Manage client mentoring sessions based on insights"
FA --> FAFR002 : "View client intervention alerts from system"
FA --> FAFR003 : "View predictive analytics about clients' financial situations"
FA --> FAFR004 : "Configure analysis parameters by client segment"

Syst <|-- SFR001
Syst <|-- SFR002
Syst <|-- SFR003
Syst <|-- SFR004
Syst <|-- SFR005
Syst <|-- SFR006
Syst <|-- SFR007
Syst <|-- SFR008
Syst <|-- SFR009
Syst <|-- SFR010
Syst <|-- SFR011
Syst <|-- SFR012
Syst <|-- SFR013
Syst <|-- SFR014
Syst <|-- SFR015

AIFR <|-- AIFR001
AIFR <|-- AIFR002
AIFR <|-- AIFR003
AIFR <|-- AIFR004
AIFR <|-- AIFR005
AIFR <|-- AIFR006
AIFR <|-- AIFR007
AIFR <|-- AIFR008
AIFR <|-- AIFR009

@enduml
'''

# Analisar e extrair
parsed_uml = run_plantuml_parser("./output/test/ollama-Fin-R1-c1-latest-temp0.4-collect-2.puml")
# Imprimir resultados formatados
print(json.dumps(parsed_uml, indent=2))

#components = extract_components_from_plantuml_json(parsed_uml)
#print(json.dumps(components, indent=2))

#converted = PlantUMLUseCaseParser(plantuml_text).parse()
#print(json.dumps(converted, indent=2))
#print(f"atores: {len(converted['actors'])} casos de uso: {len(converted['use_cases'])}  packages: {len(converted['packages'])}  rectangles: {len(converted['rectangles'])}  relationships: {len(converted['relationships'])}")

#converted = extract_elements(parsed_uml)
#print(f"atores: {len(converted['actors'])} casos de uso: {len(converted['usecases'])}  packages: {len(converted['packages'])}  rectangles: {len(converted['rectangles'])}  relationships: {len(converted['relationships'])}")
# print(json.dumps(converted, indent=2))
