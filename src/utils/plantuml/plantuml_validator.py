import re


class PlantUMLValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.error_count = {
            'atores': 0,
            'casos_de_uso': 0,
            'relacionamentos': 0,
            'sistema': 0,
            'notas': 0,
            'outros': 0
        }
        
    def validate(self, plantuml_code):
        # Normaliza o código
        if '\n' not in plantuml_code and len(plantuml_code.strip()) > 100:
            plantuml_code = plantuml_code.replace('@startuml', '@startuml\n')
            plantuml_code = plantuml_code.replace('@enduml', '\n@enduml')
            plantuml_code = re.sub(r'([^\s])\s*rectangle', r'\1\nrectangle', plantuml_code)
            plantuml_code = re.sub(r'}\s*([^\s])', r'}\n\1', plantuml_code)
            plantuml_code = re.sub(r'(actor|usecase|note|rectangle)(\s+)', r'\n\1\2', plantuml_code)
        
        # Separa as linhas
        lines = [line.strip() for line in plantuml_code.strip().split('\n') if line.strip()]
        
        # Valida início e fim do diagrama
        self._validate_start_end(lines)
        
        # Valida atores
        self._validate_actors(lines)
        
        # Valida casos de uso
        self._validate_use_cases(lines)
        
        # Valida relacionamentos
        self._validate_relationships(lines)
        
        # Valida sistema (retângulo)
        self._validate_system(lines)
        
        # Valida notas
        self._validate_notes(lines)
        
        return self.errors, self.warnings, self.error_count
    
    def _validate_start_end(self, lines):
        if not lines[0].startswith('@startuml'):
            self.errors.append({
                'tipo': 'outros',
                'linha': '1',
                'mensagem': 'Diagrama deve começar com @startuml',
                'severidade': 'erro'
            })
            self.error_count['outros'] += 1
        
        if not lines[-1].startswith('@enduml'):
            self.errors.append({
                'tipo': 'outros',
                'linha': str(len(lines)),
                'mensagem': 'Diagrama deve terminar com @enduml',
                'severidade': 'erro'
            })
            self.error_count['outros'] += 1
    
    def _validate_actors(self, lines):
        for i, line in enumerate(lines, 1):
            # Verifica sintaxe dos atores
            if line.startswith('actor '):
                # Verifica se tem "as" sem alias
                if ' as ' in line and line.split(' as ')[1].strip() == '':
                    self.errors.append({
                        'tipo': 'atores',
                        'linha': str(i),
                        'mensagem': 'Ator com "as" deve ter um alias',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['atores'] += 1
                
                # Verifica formato especial incorreto
                if ':' in line and not (line.count(':') >= 2 or ' as ' in line):
                    self.errors.append({
                        'tipo': 'atores',
                        'linha': str(i),
                        'mensagem': 'Formato especial de ator incorreto. Use :Nome: ou Nome as alias',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['atores'] += 1
    
    def _validate_use_cases(self, lines):
        for i, line in enumerate(lines, 1):
            # Ignora linhas de relacionamento e outras definições
            if '-->' in line or '->' in line or '.>' in line or '<|--' in line or line.startswith('actor ') or line.startswith('note '):
                continue
            
            # Verifica casos de uso com aspas em vez de parênteses
            if '"' in line and not (line.startswith('note') or line.startswith('title')):
                if 'as (' in line or 'as(' in line:
                    self.warnings.append({
                        'tipo': 'casos_de_uso',
                        'linha': str(i),
                        'mensagem': 'Caso de uso definido com aspas em vez de parênteses',
                        'severidade': 'aviso',
                        'conteudo': line
                    })
                    # Não incrementa count para avisos
            
            # Verifica casos de uso sem parênteses ou sem fechamento correto
            if ('(' in line and ')' not in line) or (')' in line and '(' not in line):
                if not line.startswith('note') and not '->' in line and not '--' in line:
                    self.errors.append({
                        'tipo': 'casos_de_uso',
                        'linha': str(i),
                        'mensagem': 'Caso de uso com parênteses incompletos',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['casos_de_uso'] += 1
            
            # Verifica "as" sem alias
            if ' as ' in line and not line.startswith('actor '):
                parts = line.split(' as ')
                if len(parts) > 1 and parts[1].strip() == '':
                    self.errors.append({
                        'tipo': 'casos_de_uso',
                        'linha': str(i),
                        'mensagem': 'Caso de uso com "as" deve ter um alias',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['casos_de_uso'] += 1
    
    def _validate_relationships(self, lines):
        includes_extends_pattern = re.compile(r'.*?\s*[<\.]\s*[\.>]\s*.*?\s*:\s*([a-zA-Z]+)')
        
        actor_names = []
        use_case_names = []
        
        # Primeiro, coleta nomes de atores e casos de uso
        for line in lines:
            if line.startswith('actor '):
                parts = line.split(' as ')
                if len(parts) > 1:
                    alias = parts[1].strip()
                    actor_names.append(alias)
                else:
                    name = line.replace('actor ', '').strip()
                    if ':' in name:
                        name = name.replace(':', '').strip()
                    actor_names.append(name)
            
            usecase_match = re.search(r'\(([^)]+)\)(?:\s+as\s+([^\s]+))?', line)
            if usecase_match and not ('-->' in line or '->' in line or '.>' in line or '<.' in line):
                name = usecase_match.group(1).strip()
                alias = usecase_match.group(2) if usecase_match.group(2) else name
                use_case_names.append(alias)
        
        for i, line in enumerate(lines, 1):
            # Verifica generalização incorreta entre casos de uso
            if '<|--' in line:
                parts = line.split('<|--')
                left = parts[0].strip()
                right = parts[1].strip() if len(parts) > 1 else ""
                
                # Verifica se é uma generalização entre casos de uso (não entre atores)
                if (left.startswith('(') or right.startswith('(')) or (left in use_case_names or right in use_case_names):
                    self.errors.append({
                        'tipo': 'relacionamentos',
                        'linha': str(i),
                        'mensagem': 'Generalização incorreta entre casos de uso. Use (filho) --|> (pai)',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['relacionamentos'] += 1
            
            # Verifica relacionamentos de inclusão/extensão
            match = includes_extends_pattern.search(line)
            if match:
                keyword = match.group(1).lower()
                
                # Verifica keywords incorretas
                if keyword not in ['include', 'includes', 'extend', 'extends']:
                    self.errors.append({
                        'tipo': 'relacionamentos',
                        'linha': str(i),
                        'mensagem': f'Palavra-chave incorreta para relacionamento: "{keyword}". Use "include", "includes", "extend" ou "extends"',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['relacionamentos'] += 1
                
                # Verifica direção inconsistente de inclusão
                if '<.' in line and ('include' in keyword or 'includes' in keyword):
                    self.errors.append({
                        'tipo': 'relacionamentos',
                        'linha': str(i),
                        'mensagem': 'Direção incorreta para relacionamento de inclusão. Use (base) ..> (incluído) : include',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['relacionamentos'] += 1
            
            # Verifica relação entre elementos inexistentes
            for pattern in [r'([^\s<>\.]+)\s*-->\s*([^\s<>\.]+)', r'([^\s<>\.]+)\s*->\s*([^\s<>\.]+)', 
                           r'([^\s<>\.]+)\s*\.\.\>\s*([^\s<>\.]+)', r'([^\s<>\.]+)\s*<\|--\s*([^\s<>\.]+)']:
                match = re.search(pattern, line)
                if match:
                    left = match.group(1).strip()
                    right = match.group(2).strip()
                    
                    # Remove parênteses se existirem
                    if left.startswith('(') and left.endswith(')'):
                        left = left[1:-1].strip()
                    if right.startswith('(') and right.endswith(')'):
                        right = right[1:-1].strip()
                    
                    if left not in actor_names and left not in use_case_names and not left.startswith('('):
                        self.warnings.append({
                            'tipo': 'relacionamentos',
                            'linha': str(i),
                            'mensagem': f'Elemento "{left}" não foi definido antes de ser usado em relacionamento',
                            'severidade': 'aviso',
                            'conteudo': line
                        })
                    
                    if right not in actor_names and right not in use_case_names and not right.startswith('('):
                        self.warnings.append({
                            'tipo': 'relacionamentos',
                            'linha': str(i),
                            'mensagem': f'Elemento "{right}" não foi definido antes de ser usado em relacionamento',
                            'severidade': 'aviso',
                            'conteudo': line
                        })
    
    def _validate_system(self, lines):
        in_rectangle = False
        open_braces = 0
        
        for i, line in enumerate(lines, 1):
            if 'rectangle' in line:
                if not '{' in line:
                    self.errors.append({
                        'tipo': 'sistema',
                        'linha': str(i),
                        'mensagem': 'Definição de retângulo sem chave de abertura',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['sistema'] += 1
                else:
                    in_rectangle = True
                    open_braces += 1
            
            if in_rectangle:
                if '{' in line:
                    open_braces += line.count('{') - (1 if 'rectangle' in line else 0)
                if '}' in line:
                    open_braces -= line.count('}')
                
                if open_braces == 0:
                    in_rectangle = False
        
        if in_rectangle:
            self.errors.append({
                'tipo': 'sistema',
                'linha': 'N/A',
                'mensagem': 'Retângulo sem chave de fechamento',
                'severidade': 'erro',
                'conteudo': 'N/A'
            })
            self.error_count['sistema'] += 1
    
    def _validate_notes(self, lines):
        in_note = False
        
        for i, line in enumerate(lines, 1):
            if line.startswith('note '):
                if not 'of ' in line and not line.startswith('note left') and not line.startswith('note right') and not line.startswith('note top') and not line.startswith('note bottom'):
                    self.errors.append({
                        'tipo': 'notas',
                        'linha': str(i),
                        'mensagem': 'Formato incorreto de nota. Use "note left/right/top/bottom of elemento"',
                        'severidade': 'erro',
                        'conteudo': line
                    })
                    self.error_count['notas'] += 1
                in_note = True
            
            if line == 'end note':
                in_note = False
        
        if in_note:
            self.errors.append({
                'tipo': 'notas',
                'linha': 'N/A',
                'mensagem': 'Nota sem fechamento (end note)',
                'severidade': 'erro',
                'conteudo': 'N/A'
            })
            self.error_count['notas'] += 1

    def print_report(self):
        total_errors = sum(self.error_count.values())
        total_warnings = len(self.warnings)
        
        print("\n=== VALIDAÇÃO DO DIAGRAMA DE CASOS DE USO ===\n")
        
        print("RESUMO DE ERROS:")
        print("-" * 30)
        print(f"| {'Tipo':<15} | {'Quantidade':<10} |")
        print("-" * 30)
        for error_type, count in self.error_count.items():
            print(f"| {error_type.replace('_', ' ').capitalize():<15} | {count:<10} |")
        print("-" * 30)
        print(f"| {'Total Erros':<15} | {total_errors:<10} |")
        print(f"| {'Total Avisos':<15} | {total_warnings:<10} |")
        print("-" * 30)
        
        if total_errors > 0:
            print("\nDETALHES DOS ERROS:")
            for error in self.errors:
                print(f"\n[{error['tipo'].upper()}] Linha {error['linha']} - {error['mensagem']}")
                if 'conteudo' in error:
                    print(f"  Conteúdo: {error['conteudo']}")
        
        if total_warnings > 0:
            print("\nAVISOS (não impedem o funcionamento, mas podem causar confusão):")
            for warning in self.warnings:
                print(f"\n[{warning['tipo'].upper()}] Linha {warning['linha']} - {warning['mensagem']}")
                if 'conteudo' in warning:
                    print(f"  Conteúdo: {warning['conteudo']}")
        
        if total_errors == 0 and total_warnings == 0:
            print("\nNenhum erro ou aviso encontrado! O diagrama está sintaticamente correto.")


def validate_plantuml(plantuml_code):
    validator = PlantUMLValidator()
    validator.validate(plantuml_code)
    validator.print_report()
    return validator.errors, validator.warnings, validator.error_count