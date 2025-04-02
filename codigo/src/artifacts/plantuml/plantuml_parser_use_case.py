import re
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any, Union


class PlantUMLUseCaseParser:
    """
    Parser interno para diagramas de casos de uso PlantUML.
    Esta classe realiza a análise detalhada do código PlantUML.
    """
    def __init__(self):
        self.elements = defaultdict(list)
        self.counts = {
            'atores': 0,
            'casos_de_uso': 0,
            'relacionamentos': 0, 
            'notas': 0,
            'retangulos': 0
        }
        self.title = None
        
    def parse(self, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Analisa o código PlantUML e extrai os elementos do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML a ser analisado
            
        Returns:
            Tuple: (elementos extraídos, contagem de elementos)
        """
        # Converte múltiplas linhas para uma única linha se o código estiver compactado
        if '\n' not in plantuml_code and len(plantuml_code.strip()) > 100:
            plantuml_code = plantuml_code.replace('@startuml', '@startuml\n')
            plantuml_code = plantuml_code.replace('@enduml', '\n@enduml')
            plantuml_code = re.sub(r'([^\s])\s*rectangle', r'\1\nrectangle', plantuml_code)
            plantuml_code = re.sub(r'}\s*([^\s])', r'}\n\1', plantuml_code)
            plantuml_code = re.sub(r'(actor|usecase|note|rectangle)(\s+)', r'\n\1\2', plantuml_code)
        
        # Limpa o código removendo linhas de configuração
        cleaned_lines = []
        for line in plantuml_code.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('@startuml') and not line.startswith('@enduml'):
                cleaned_lines.append(line)
        
        # Extrai o título se existir
        self.title = None
        for line in cleaned_lines:
            if line.startswith('title '):
                self.title = line[6:].strip()
                break
        
        # Reseta os elementos e contagens antes de iniciar a análise
        self._reset()
        
        # Analisa os atores
        self._parse_actors(cleaned_lines)
        
        # Analisa casos de uso
        self._parse_use_cases(cleaned_lines)
        
        # Analisa retângulos (sistemas/pacotes)
        self._parse_rectangles(cleaned_lines)
        
        # Analisa relacionamentos
        self._parse_relationships(cleaned_lines)
        
        # Analisa notas
        self._parse_notes(cleaned_lines)
        
        return self.elements, self.counts
    
    def _reset(self) -> None:
        """Reseta o estado do parser para uma nova análise."""
        self.elements = defaultdict(list)
        self.counts = {
            'atores': 0,
            'casos_de_uso': 0,
            'relacionamentos': 0, 
            'notas': 0,
            'retangulos': 0
        }
    
    def _parse_actors(self, lines: List[str]) -> None:
        """
        Extrai atores do diagrama.
        
        Args:
            lines (List[str]): Linhas de código PlantUML limpo
        """
        # Padrão para atores definidos diretamente
        actor_pattern = re.compile(r'actor\s+:?([^:]+?)(?::\s*as\s+([^\s]+)|$)')
        # Padrão para atores em relações de herança
        inheritance_pattern = re.compile(r'([^\s]+)\s+<\|--\s+([^\s]+)')
        
        for line in lines:
            # Procura definições diretas de atores
            match = actor_pattern.search(line)
            if match:
                actor_name = match.group(1).strip()
                actor_alias = match.group(2) if match.group(2) else actor_name
                
                # Para atores com formato especial como ":Nome:"
                if actor_name.startswith(':') and actor_name.endswith(':'):
                    actor_name = actor_name[1:-1].strip()
                
                self.elements['atores'].append({'nome': actor_name, 'alias': actor_alias})
                self.counts['atores'] += 1
        
        # Segunda passagem para identificar atores em relações de herança que não foram definidos explicitamente
        for line in lines:
            if '<|--' in line:
                match = inheritance_pattern.search(line)
                if match:
                    parent = match.group(1).strip()
                    child = match.group(2).strip()
                    
                    # Verifica se os atores já estão na lista
                    parent_exists = False
                    child_exists = False
                    
                    for actor in self.elements['atores']:
                        if actor['alias'] == parent:
                            parent_exists = True
                        if actor['alias'] == child:
                            child_exists = True
                    
                    # Adiciona atores à lista se não estiverem presentes
                    if not parent_exists:
                        self.elements['atores'].append({'nome': parent, 'alias': parent})
                        self.counts['atores'] += 1
                    
                    if not child_exists:
                        self.elements['atores'].append({'nome': child, 'alias': child})
                        self.counts['atores'] += 1
    
    def _parse_use_cases(self, lines: List[str]) -> None:
        """
        Extrai casos de uso do diagrama.
        
        Args:
            lines (List[str]): Linhas de código PlantUML limpo
        """
        # Padrão para casos de uso definidos diretamente
        usecase_pattern1 = re.compile(r'\(([^)]+)\)(?:\s+as\s+([^\s]+))?')
        usecase_pattern2 = re.compile(r'usecase\s+"([^"]+)"(?:\s+as\s+([^\s]+))?')
        
        # Padrão para casos de uso em relações
        relation_usecase_pattern = re.compile(r'\(([^)]+)\)\s+\.>\s+')
        
        # Primeiro, procura casos de uso definidos diretamente
        for line in lines:
            # Ignora linhas que são claramente relacionamentos
            if ('<|--' in line) or ('-->' in line and '(' not in line) or ('->' in line and '(' not in line):
                continue
                
            # Procura casos de uso em formato (Nome do Caso)
            for match in usecase_pattern1.finditer(line):
                usecase_name = match.group(1).strip()
                usecase_alias = match.group(2) if match.group(2) else usecase_name
                
                # Verifica se este caso de uso já foi adicionado
                if not any(uc['nome'] == usecase_name for uc in self.elements['casos_de_uso']):
                    self.elements['casos_de_uso'].append({'nome': usecase_name, 'alias': usecase_alias})
                    self.counts['casos_de_uso'] += 1
            
            # Procura casos de uso em formato usecase "Nome do Caso"
            for match in usecase_pattern2.finditer(line):
                usecase_name = match.group(1).strip()
                usecase_alias = match.group(2) if match.group(2) else usecase_name
                
                if not any(uc['nome'] == usecase_name for uc in self.elements['casos_de_uso']):
                    self.elements['casos_de_uso'].append({'nome': usecase_name, 'alias': usecase_alias})
                    self.counts['casos_de_uso'] += 1
        
        # Agora, procura casos de uso em relações de extensão/inclusão
        for line in lines:
            if '.>' in line and '(' in line:
                match = relation_usecase_pattern.search(line)
                if match:
                    usecase_name = match.group(1).strip()
                    
                    # Verifica se este caso de uso já foi adicionado
                    if not any(uc['nome'] == usecase_name for uc in self.elements['casos_de_uso']):
                        self.elements['casos_de_uso'].append({'nome': usecase_name, 'alias': usecase_name})
                        self.counts['casos_de_uso'] += 1
    
    def _parse_rectangles(self, lines: List[str]) -> None:
        """
        Extrai retângulos (sistemas/pacotes) do diagrama.
        
        Args:
            lines (List[str]): Linhas de código PlantUML limpo
        """
        in_rectangle = False
        rectangle_name = ""
        rectangle_content = []
        open_braces = 0
        
        for i, line in enumerate(lines):
            # Detecta o início de um retângulo
            if 'rectangle ' in line and '{' in line:
                in_rectangle = True
                open_braces = 1
                rectangle_name = line.split('rectangle ')[1].split(' {')[0].strip()
                continue
            
            # Acompanha abertura e fechamento de chaves para lidar com retângulos aninhados
            if in_rectangle:
                if '{' in line:
                    open_braces += line.count('{')
                if '}' in line:
                    open_braces -= line.count('}')
                
                # Quando todas as chaves estão fechadas, termina o retângulo
                if open_braces == 0:
                    self.elements['retangulos'].append({
                        'nome': rectangle_name,
                        'conteudo': rectangle_content
                    })
                    self.counts['retangulos'] += 1
                    in_rectangle = False
                    rectangle_name = ""
                    rectangle_content = []
                else:
                    # Adiciona a linha ao conteúdo do retângulo se não for a linha de fechamento
                    if not line.strip() == '}':
                        rectangle_content.append(line)
    
    def _parse_relationships(self, lines: List[str]) -> None:
        """
        Extrai relacionamentos do diagrama.
        
        Args:
            lines (List[str]): Linhas de código PlantUML limpo
        """
        # Padrões para diferentes tipos de relacionamentos
        extend_pattern = re.compile(r'\(([^)]+)\)\s+\.+>\s+\(?([^)\s:]+).*?:\s*extends?')
        include_pattern = re.compile(r'\(([^)]+)\)\s+\.+>\s+\(?([^)\s:]+).*?:\s*includes?')
        association_pattern1 = re.compile(r'([^\s(]+)\s+-->\s+\(?([^)\s:]+)')
        association_pattern2 = re.compile(r'([^\s(]+)\s+->\s+\(?([^)\s:]+)')
        association_pattern3 = re.compile(r'([^\s(]+)\s+--\s+\(?([^)\s:]+)')
        association_pattern4 = re.compile(r'\(([^)]+)\)\s+-->\s+([^\s:]+)')
        association_pattern5 = re.compile(r'\(([^)]+)\)\s+->\s+([^\s:]+)')
        association_pattern6 = re.compile(r'\(([^)]+)\)\s+--\s+([^\s:]+)')
        generalization_pattern = re.compile(r'([^\s]+)\s+<\|--\s+([^\s]+)')
        
        for line in lines:
            # Processa extensões
            for match in extend_pattern.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parênteses se houver
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'extensão'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa inclusões
            for match in include_pattern.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parênteses se houver
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'inclusão'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 1
            for match in association_pattern1.finditer(line):
                if '.>' in line and ':' in line:  # Ignora se for uma relação de extend/include
                    continue
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parênteses se houver
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 2
            for match in association_pattern2.finditer(line):
                if '.>' in line and ':' in line:  # Ignora se for uma relação de extend/include
                    continue
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parênteses se houver
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 3
            for match in association_pattern3.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parênteses se houver
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 4
            for match in association_pattern4.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 5
            for match in association_pattern5.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa associações - padrão 6
            for match in association_pattern6.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relacionamentos'].append({
                    'origem': source,
                    'destino': target,
                    'tipo': 'associação'
                })
                self.counts['relacionamentos'] += 1
            
            # Processa generalizações
            for match in generalization_pattern.finditer(line):
                parent = match.group(1).strip()
                child = match.group(2).strip()
                
                self.elements['relacionamentos'].append({
                    'origem': parent,
                    'destino': child,
                    'tipo': 'generalização'
                })
                self.counts['relacionamentos'] += 1
    
    def _parse_notes(self, lines: List[str]) -> None:
        """
        Extrai notas do diagrama.
        
        Args:
            lines (List[str]): Linhas de código PlantUML limpo
        """
        in_note = False
        note_content = []
        note_target = ""
        
        for i, line in enumerate(lines):
            # Detecta o início de uma nota
            if line.startswith('note ') and 'of ' in line:
                in_note = True
                parts = line.split('of ')
                if len(parts) >= 2:
                    note_target = parts[1].strip()
                continue
            
            # Detecta o fim de uma nota
            if in_note and line == 'end note':
                self.elements['notas'].append({
                    'alvo': note_target,
                    'conteudo': '\n'.join(note_content)
                })
                self.counts['notas'] += 1
                in_note = False
                note_content = []
                note_target = ""
                continue
            
            # Adiciona conteúdo à nota
            if in_note:
                note_content.append(line)
    
    def get_summary_text(self) -> str:
        """
        Gera um texto resumido dos componentes do diagrama.
        
        Returns:
            str: Texto resumido
        """
        total = sum(self.counts.values())
        
        lines = []
        lines.append("\n=== ANÁLISE DO DIAGRAMA DE CASOS DE USO ===\n")
        
        # Tabela de contagem
        lines.append("CONTAGEM DE ELEMENTOS:")
        lines.append("-" * 30)
        lines.append(f"| {'Elemento':<15} | {'Quantidade':<10} |")
        lines.append("-" * 30)
        for element, count in self.counts.items():
            lines.append(f"| {element.replace('_', ' ').title():<15} | {count:<10} |")
        lines.append("-" * 30)
        lines.append(f"| {'Total':<15} | {total:<10} |")
        lines.append("-" * 30)
        
        # Detalhes dos elementos
        lines.append("\nDETALHES DOS ELEMENTOS:")
        
        if self.elements['atores']:
            lines.append("\nATORES:")
            for i, actor in enumerate(self.elements['atores'], 1):
                if actor['alias'] != actor['nome']:
                    lines.append(f"  {i}. {actor['nome']} (alias: {actor['alias']})")
                else:
                    lines.append(f"  {i}. {actor['nome']}")
        
        if self.elements['casos_de_uso']:
            lines.append("\nCASOS DE USO:")
            for i, usecase in enumerate(self.elements['casos_de_uso'], 1):
                if usecase['alias'] != usecase['nome']:
                    lines.append(f"  {i}. {usecase['nome']} (alias: {usecase['alias']})")
                else:
                    lines.append(f"  {i}. {usecase['nome']}")
        
        if self.elements['relacionamentos']:
            lines.append("\nRELACIONAMENTOS:")
            for i, rel in enumerate(self.elements['relacionamentos'], 1):
                lines.append(f"  {i}. {rel['origem']} --> {rel['destino']} [{rel['tipo']}]")
        
        if self.elements['notas']:
            lines.append("\nNOTAS:")
            for i, note in enumerate(self.elements['notas'], 1):
                lines.append(f"  {i}. Nota para {note['alvo']}:")
                for line in note['conteudo'].split('\n'):
                    lines.append(f"     {line}")
        
        if self.elements['retangulos']:
            lines.append("\nSISTEMAS/PACOTES:")
            for i, rect in enumerate(self.elements['retangulos'], 1):
                lines.append(f"  {i}. {rect['nome']}")
        
        if self.title:
            lines.append(f"\nTÍTULO DO DIAGRAMA: {self.title}")
            
        return '\n'.join(lines)
    
    def print_summary(self) -> None:
        """Imprime o resumo do diagrama."""
        print(self.get_summary_text())


class PlantUMLUseCase:
    """
    Fachada para extração de componentes de diagramas de casos de uso PlantUML.
    Fornece uma API simplificada para análise de diagramas.
    """
    _last_code = None
    _last_elements = None
    _last_counts = None
    
    @classmethod
    def _get_parsed_data(cls, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Retorna os dados analisados, usando cache quando possível.
        
        Args:
            plantuml_code (str): Código PlantUML a ser analisado
            
        Returns:
            Tuple: (elementos extraídos, contagem de elementos)
        """
        # Usa cache se o código for o mesmo da última vez
        if cls._last_code == plantuml_code and cls._last_elements and cls._last_counts:
            return cls._last_elements, cls._last_counts
        
        # Caso contrário, executa o parser
        parser = PlantUMLUseCaseParser()
        elements, counts = parser.parse(plantuml_code)
        
        # Atualiza o cache
        cls._last_code = plantuml_code
        cls._last_elements = elements
        cls._last_counts = counts
        
        return elements, counts
    
    @classmethod
    def validate_code(cls, plantuml_code: str) -> bool:
        """
        Valida se o código PlantUML é um diagrama de casos de uso válido.
        
        Args:
            plantuml_code (str): Código PlantUML a ser validado
            
        Returns:
            bool: True se o código for válido, False caso contrário
        """
        # Verifica se o código tem as marcações obrigatórias
        if '@startuml' not in plantuml_code or '@enduml' not in plantuml_code:
            return False
            
        # Verifica se há pelo menos um ator ou caso de uso
        _, counts = cls._get_parsed_data(plantuml_code)
        return counts['atores'] > 0 or counts['casos_de_uso'] > 0
    
    @classmethod
    def extract_components(cls, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Extrai todos os componentes do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            Tuple: (elementos extraídos, contagem de elementos)
        """
        return cls._get_parsed_data(plantuml_code)
    
    @classmethod
    def extract_actors(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extrai apenas os atores do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            List[Dict[str, str]]: Lista de atores no formato [{'nome': nome, 'alias': alias}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['atores']
    
    @classmethod
    def extract_use_cases(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extrai apenas os casos de uso do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            List[Dict[str, str]]: Lista de casos de uso no formato [{'nome': nome, 'alias': alias}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['casos_de_uso']
    
    @classmethod
    def extract_relationships(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extrai apenas os relacionamentos do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            List[Dict[str, str]]: Lista de relacionamentos no formato 
                                 [{'origem': origem, 'destino': destino, 'tipo': tipo}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['relacionamentos']
    
    @classmethod
    def extract_systems(cls, plantuml_code: str) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Extrai apenas os sistemas/pacotes (retângulos) do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            List[Dict[str, Union[str, List[str]]]]: Lista de sistemas/pacotes no formato 
                                                  [{'nome': nome, 'conteudo': [conteudo]}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['retangulos']
    
    @classmethod
    def extract_notes(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extrai apenas as notas do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            List[Dict[str, str]]: Lista de notas no formato [{'alvo': alvo, 'conteudo': conteudo}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['notas']
    
    @classmethod
    def extract_title(cls, plantuml_code: str) -> Optional[str]:
        """
        Extrai o título do diagrama, se houver.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            Optional[str]: Título do diagrama ou None se não houver
        """
        parser = PlantUMLUseCaseParser()
        parser.parse(plantuml_code)
        return parser.title
    
    @classmethod
    def get_summary(cls, plantuml_code: str) -> str:
        """
        Gera um resumo em texto dos componentes do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
            
        Returns:
            str: Resumo formatado dos componentes do diagrama
        """
        parser = PlantUMLUseCaseParser()
        parser.parse(plantuml_code)
        return parser.get_summary_text()
    
    @classmethod
    def print_summary(cls, plantuml_code: str) -> None:
        """
        Imprime um resumo dos componentes do diagrama.
        
        Args:
            plantuml_code (str): Código PlantUML do diagrama de casos de uso
        """
        print(cls.get_summary(plantuml_code))


# Função legada para compatibilidade com código existente
def analyze_plantuml_use_case(plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
    """
    Analisa um diagrama de casos de uso PlantUML e imprime um resumo.
    
    Args:
        plantuml_code (str): Código PlantUML do diagrama de casos de uso
        
    Returns:
        Tuple: (elementos extraídos, contagem de elementos)
    """
    PlantUMLUseCase.print_summary(plantuml_code)
    return PlantUMLUseCase.extract_components(plantuml_code)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo simples de um diagrama de casos de uso
    exemplo_plantuml = """
@startuml
left to right direction
actor Cliente
actor Funcionário
rectangle "Sistema de Reservas" {
    (Fazer Reserva) as FR
    (Cancelar Reserva) as CR
    (Modificar Reserva) as MR
    (Verificar Disponibilidade) as VD
    (Emitir Comprovante) as EC
    
    FR --> VD : include
    CR --> FR : extends
    MR --> FR : extends
    FR --> EC : include
}

Cliente --> FR
Cliente --> CR
Cliente --> MR
Funcionário --> FR
Funcionário --> CR
Funcionário --> MR
Funcionário --> VD

note right of Funcionário : Funcionários possuem acesso a todas as funcionalidades

@enduml
"""

    # Exemplos de uso da nova API
    print("\n===== EXEMPLO USANDO A NOVA API =====\n")
    
    # Validar o código
    if PlantUMLUseCase.validate_code(exemplo_plantuml):
        print("O código PlantUML é válido.")
    else:
        print("O código PlantUML é inválido.")
    
    print("\n-- Extraindo atores --")
    atores = PlantUMLUseCase.extract_actors(exemplo_plantuml)
    for ator in atores:
        print(f"Ator: {ator['nome']}")
    
    print("\n-- Extraindo casos de uso --")
    casos_uso = PlantUMLUseCase.extract_use_cases(exemplo_plantuml)
    for caso in casos_uso:
        print(f"Caso de uso: {caso['nome']}")
    
    print("\n-- Extraindo relacionamentos --")
    relacionamentos = PlantUMLUseCase.extract_relationships(exemplo_plantuml)
    for rel in relacionamentos:
        print(f"Relação: {rel['origem']} -> {rel['destino']} ({rel['tipo']})")
    
    print("\n-- Extraindo sistemas/pacotes --")
    sistemas = PlantUMLUseCase.extract_systems(exemplo_plantuml)
    for sistema in sistemas:
        print(f"Sistema: {sistema['nome']}")
    
    print("\n-- Extraindo notas --")
    notas = PlantUMLUseCase.extract_notes(exemplo_plantuml)
    for nota in notas:
        print(f"Nota para {nota['alvo']}: {nota['conteudo']}")
    
    print("\n-- Resumo completo do diagrama --")
    print(PlantUMLUseCase.get_summary(exemplo_plantuml))
    
    # Exemplo usando a função legada para compatibilidade
    print("\n===== EXEMPLO USANDO A FUNÇÃO LEGADA =====\n")
    elementos, contagens = analyze_plantuml_use_case(exemplo_plantuml)