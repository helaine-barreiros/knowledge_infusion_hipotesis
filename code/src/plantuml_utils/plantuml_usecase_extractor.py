import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Relation:
    source: str
    target: str
    relation_type: str  # "association", "generalization", "include", "extend"
    direction: str  # "-->", "<--", "-|>", "<|-", "..>", "<.."
    label: Optional[str] = None


@dataclass
class Actor:
    name: str
    alias: Optional[str] = None
    stereotypes: List[str] = field(default_factory=list)
    package: Optional[str] = None
    color: Optional[str] = None
    relations: List[Relation] = field(default_factory=list)
    

@dataclass
class UseCase:
    name: str
    alias: Optional[str] = None
    stereotypes: List[str] = field(default_factory=list)
    package: Optional[str] = None
    color: Optional[str] = None


@dataclass
class Package:
    name: str
    content: List[str] = field(default_factory=list)


class PlantUMLUseCaseParser:
    def __init__(self, plantuml_text: str):
        self.original_text = plantuml_text
        self.clean_text = ""
        self.actors = {}  # Dict[str, Actor]
        self.use_cases = {}  # Dict[str, UseCase]
        self.packages = {}  # Dict[str, Package]
        
        # Expressões regulares para identificar componentes
        self.actor_regex = re.compile(r':([^:]+):(?:\s+as\s+([A-Za-z0-9_]+))?|actor\s+"?([^"]+)"?(?:\s+as\s+([A-Za-z0-9_]+))?')
        self.usecase_regex = re.compile(r'\(([^)]+)\)(?:\s+as\s+([A-Za-z0-9_]+))?|usecase\s+"?([^"]+)"?(?:\s+as\s+([A-Za-z0-9_]+))?')
        self.stereotype_regex = re.compile(r'<<([^>]+)>>')
        self.relation_regex = re.compile(r'([A-Za-z0-9_:()]+)\s*([-\.><|]+[lrud]?[-\.><|]*)\s*([A-Za-z0-9_:()]+)(?:\s*:\s*(.+))?')
        self.package_start_regex = re.compile(r'package\s+"([^"]+)"(?:\s+([A-Za-z0-9_#]+))?\s*\{')
        self.package_end_regex = re.compile(r'\}')
        
        # Expressões para relações específicas
        self.generalization_regex = re.compile(r'-\|>')
        self.include_regex = re.compile(r'\.\.>\s*.*<<include>>')
        self.extend_regex = re.compile(r'\.\.>\s*.*<<extend>>')
        
        # Atributos para rastreamento do estado do parser
        self.current_package = None
        
        self.parse_all_components

    def remove_accessory_info(self):
        """Remove informações acessórias do diagrama."""
        # Lista de padrões a serem removidos
        patterns_to_remove = [
            r'@startuml.*\n',
            r'@enduml.*\n?',
            r'skinparam\s+.*\n',
            r'(?:left\s+to\s+right|top\s+to\s+bottom)\s+direction.*\n',
            r'==.*==\n',
            r'!.*\n',  # Comentários e diretivas
            r'\n\s*\n'  # Linhas vazias extras
        ]
        
        # Aplica a remoção
        clean_text = self.original_text
        for pattern in patterns_to_remove:
            clean_text = re.sub(pattern, '\n', clean_text)
        
        # Remove espaços em branco extras
        clean_text = re.sub(r'\n+', '\n', clean_text).strip()
        
        self.clean_text = clean_text
        return self.clean_text
    
    def parse_all_components(self):
        """Identifica todos os atores no diagrama e seus relacionamentos."""
        # Primeiro limpa o texto
        if not self.clean_text:
            self.remove_accessory_info()
            
        # Analisa linhas para identificar pacotes
        self._parse_packages()
        
        # Analisa linhas para identificar atores
        self._parse_all_actors()
        
        # Analisa linhas para identificar casos de uso
        self._parse_all_use_cases()
        
        # Analisa linhas para identificar relações
        self._parse_all_relations()
        
        return self.actors
    
    def _parse_packages(self):
        """Identifica todos os pacotes no diagrama."""
        lines = self.clean_text.split('\n')
        stack = []  # Pilha para rastrear pacotes aninhados
        
        for line in lines:
            # Verifica se é o início de um pacote
            package_match = self.package_start_regex.search(line)
            if package_match:
                package_name = package_match.group(1)
                package_color = package_match.group(2) if package_match.group(2) else None
                package = Package(name=package_name)
                self.packages[package_name] = package
                stack.append(package_name)
                self.current_package = package_name
                continue
                
            # Verifica se é o fim de um pacote
            if self.package_end_regex.search(line):
                if stack:
                    stack.pop()
                    self.current_package = stack[-1] if stack else None
                continue
                
            # Adiciona a linha ao conteúdo do pacote atual, se houver
            if self.current_package:
                self.packages[self.current_package].content.append(line)
    
    def _parse_all_actors(self):
        """Identifica todos os atores no diagrama."""
        lines = self.clean_text.split('\n')
        current_package = None
        
        for line in lines:
            # Verifica se é o início de um pacote
            package_match = self.package_start_regex.search(line)
            if package_match:
                current_package = package_match.group(1)
                continue
                
            # Verifica se é o fim de um pacote
            if self.package_end_regex.search(line):
                current_package = None
                continue
            
            # Busca por atores na linha
            actor_matches = self.actor_regex.finditer(line)
            for match in actor_matches:
                # Extrai as informações do ator
                if match.group(1):  # Formato :Nome:
                    actor_name = match.group(1)
                    actor_alias = match.group(2)
                else:  # Formato actor "Nome"
                    actor_name = match.group(3)
                    actor_alias = match.group(4)
                
                # Verifica o identificador real a ser usado (nome ou alias)
                actor_id = actor_alias if actor_alias else actor_name
                
                # Busca por estereótipos (já um tipo de relacionamento)
                stereotypes = []
                stereotype_matches = self.stereotype_regex.finditer(line)
                for s_match in stereotype_matches:
                    stereotypes.append(s_match.group(1))
                
                # Busca por cor (simplificada)
                color_match = re.search(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', line)
                color = color_match.group(0) if color_match else None
                
                # Cria o objeto do ator
                actor = Actor(
                    name=actor_name,
                    alias=actor_alias,
                    stereotypes=stereotypes,
                    package=current_package,
                    color=color
                )
                
                # Adiciona o ator ao dicionário
                self.actors[actor_id] = actor
    
    def _parse_all_use_cases(self):
        """Identifica todos os casos de uso no diagrama."""
        lines = self.clean_text.split('\n')
        current_package = None
        
        for line in lines:
            # Verifica se é o início de um pacote
            package_match = self.package_start_regex.search(line)
            if package_match:
                current_package = package_match.group(1)
                continue
                
            # Verifica se é o fim de um pacote
            if self.package_end_regex.search(line):
                current_package = None
                continue
            
            # Busca por casos de uso na linha
            usecase_matches = self.usecase_regex.finditer(line)
            for match in usecase_matches:
                # Extrai as informações do caso de uso
                if match.group(1):  # Formato (Nome)
                    usecase_name = match.group(1)
                    usecase_alias = match.group(2)
                else:  # Formato usecase "Nome"
                    usecase_name = match.group(3)
                    usecase_alias = match.group(4)
                
                # Verifica o identificador real a ser usado (nome ou alias)
                usecase_id = usecase_alias if usecase_alias else usecase_name
                
                # Busca por estereótipos
                stereotypes = []
                stereotype_matches = self.stereotype_regex.finditer(line)
                for s_match in stereotype_matches:
                    stereotypes.append(s_match.group(1))
                
                # Busca por cor (simplificada)
                color_match = re.search(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', line)
                color = color_match.group(0) if color_match else None
                
                # Cria o objeto do caso de uso
                usecase = UseCase(
                    name=usecase_name,
                    alias=usecase_alias,
                    stereotypes=stereotypes,
                    package=current_package,
                    color=color
                )
                
                # Adiciona o caso de uso ao dicionário
                self.use_cases[usecase_id] = usecase
    
    def _parse_all_relations(self):
        """Identifica todas as relações no diagrama."""
        lines = self.clean_text.split('\n')
        
        for line in lines:
            # Busca por relações na linha
            relation_matches = self.relation_regex.finditer(line)
            for match in relation_matches:
                source = match.group(1)
                arrow = match.group(2)
                target = match.group(3)
                label = match.group(4)
                
                # Determina o tipo de relação
                relation_type = "association"  # Padrão
                
                if self.generalization_regex.search(arrow):
                    relation_type = "generalization"
                elif self.include_regex.search(line):
                    relation_type = "include"
                elif self.extend_regex.search(line):
                    relation_type = "extend"
                
                # Cria o objeto da relação
                relation = Relation(
                    source=source,
                    target=target,
                    relation_type=relation_type,
                    direction=arrow,
                    label=label
                )
                
                # Adiciona a relação ao ator correspondente (se for ator)
                if source in self.actors:
                    self.actors[source].relations.append(relation)
                
                # Se o target for um ator e a relação for bidirecional,
                # adicione também a relação inversa
                if target in self.actors and "<->" in arrow:
                    inverse_relation = Relation(
                        source=target,
                        target=source,
                        relation_type=relation_type,
                        direction=arrow,  # Mantém a mesma seta para indicar bidirecionalidade
                        label=label
                    )
                    self.actors[target].relations.append(inverse_relation)
    
    def get_actor_details(self, actor_id):
        """Retorna detalhes completos de um ator específico."""
        if actor_id not in self.actors:
            return None
            
        actor = self.actors[actor_id]
        
        # Identifica casos de uso relacionados
        related_usecases = []
        for relation in actor.relations:
            if relation.target in self.use_cases:
                related_usecases.append({
                    "usecase": self.use_cases[relation.target],
                    "relation_type": relation.relation_type,
                    "direction": relation.direction,
                    "label": relation.label
                })
        
        # Identifica atores relacionados
        related_actors = []
        for relation in actor.relations:
            if relation.target in self.actors:
                related_actors.append({
                    "actor": self.actors[relation.target],
                    "relation_type": relation.relation_type,
                    "direction": relation.direction,
                    "label": relation.label
                })
        
        return {
            "actor": actor,
            "related_usecases": related_usecases,
            "related_actors": related_actors,
            "package": self.packages.get(actor.package) if actor.package else None
        }
    
    def get_all_actors_details(self):
        """Retorna detalhes completos de todos os atores."""
        result = {}
        for actor_id in self.actors:
            result[actor_id] = self.get_actor_details(actor_id)
        return result


# Exemplo de uso:
if __name__ == "__main__":
    # Exemplo de diagrama PlantUML
    plantuml_text = """
    @startuml
    left to right direction
    
    actor "Cliente" as cliente
    actor :Vendedor: as vendedor
    actor :Administrador: as admin
    
    package "Sistema de Vendas" {
      (Efetuar Compra) as UC1
      (Consultar Produto) as UC2
      (Processar Pagamento) as UC3
      (Gerenciar Estoque) as UC4
    }
    
    cliente --> UC1
    cliente --> UC2
    UC1 ..> UC3 : <<include>>
    vendedor --> UC3
    admin -|> vendedor
    admin --> UC4
    
    note right of UC3: Requer autenticação
    
    @enduml
    """
    
    parser = PlantUMLUseCaseParser(plantuml_text)
    
    atores = parser.parse_all_components()
    
    # Obtém detalhes de todos os atores
    actors_details = parser.get_all_actors_details()
    
    # Imprime detalhes de um ator específico
    if "cliente" in actors_details:
        client = actors_details["cliente"]["actor"]
        print(f"Ator: {client.name}")
        print(f"Relacionamentos: {len(client.relations)}")
        
        for relation in client.relations:
            print(f"  - Relacionamento com: {relation.target}")
            print(f"    Tipo: {relation.relation_type}")
            print(f"    Direção: {relation.direction}")
            if relation.label:
                print(f"    Rótulo: {relation.label}")