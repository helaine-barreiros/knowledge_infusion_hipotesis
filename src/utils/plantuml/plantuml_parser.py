import re
from collections import defaultdict
from typing import Dict, List, Tuple, Any
from src.utils.logger import Logger


class PlantUMLUseCaseParser:
    """
    Parser for PlantUML use case diagrams.
    This class performs detailed analysis of PlantUML code.
    """
    def __init__(self):
        self.LOGGER = Logger

    def parse(self, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Analyzes PlantUML code and extracts diagram elements.

        Args:
            plantuml_code (str): PlantUML code to analyze

        Returns:
            Tuple: (extracted elements, element counts)
        """
        diagram = {
            'type': 'use case',
            'title': "",
            'elements': [],
            'count': 0,
            'detailed_count': {}
        }

        if not plantuml_code:
            return diagram

        # Convert multiple lines to a single line if the code is compacted
        if '\n' not in plantuml_code and len(plantuml_code.strip()) > 100:
            plantuml_code = plantuml_code.replace('@startuml', '@startuml\n')
            plantuml_code = plantuml_code.replace('@enduml', '\n@enduml')
            plantuml_code = re.sub(r'([^\s])\s*rectangle', r'\1\nrectangle', plantuml_code)
            plantuml_code = re.sub(r'}\s*([^\s])', r'}\n\1', plantuml_code)
            plantuml_code = re.sub(r'(actor|usecase|note|rectangle)(\s+)', r'\n\1\2', plantuml_code)

        # Clean code by removing configuration lines
        cleaned_lines = []
        for line in plantuml_code.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('@startuml') and not line.startswith('@enduml'):
                cleaned_lines.append(line)

        # Extract title if exists
        for line in cleaned_lines:
            if line.startswith('title '):
                diagram['title'] = line[6:].strip()
                break

        actors, qtd_actors = self.get_actors(cleaned_lines)
        use_cases, qtd_use_cases = self.get_use_cases(cleaned_lines)
        rectangles, qtd_rectangles = self.get_rectangles(cleaned_lines)
        relationships, qtd_relationships = self.get_relationships(cleaned_lines)
        notes, qtd_notes = self.get_notes(cleaned_lines)

        diagram['actors'] = actors
        diagram['use_cases'] = use_cases
        diagram['rectangles'] = rectangles
        diagram['relationships'] = relationships
        diagram['notes'] = notes

        elements = []
        elements.extend(actors)
        elements.extend(use_cases)
        elements.extend(rectangles)
        elements.extend(relationships)
        elements.extend(notes)

        diagram['elements'] = elements

        diagram['count'] = len(elements)

        diagram['detailed_count'] = {
            'actors': qtd_actors,
            'use_cases': qtd_use_cases,
            'relationships': qtd_relationships,
            'notes': qtd_notes,
            'rectangles': qtd_rectangles
        }

        return diagram

    def get_actors(self, lines: List[str]) -> None:
        """
        Extracts actors from diagram.
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        actors = []
        qtd_actors = 0
        
        # Pattern for directly defined actors
        actor_pattern = re.compile(r'actor\s+:?([^:]+?)(?::\s*as\s+([^\s]+)|$)')
        # Pattern for actors in inheritance relationships
        inheritance_pattern = re.compile(r'([^\s]+)\s+<\|--\s+([^\s]+)')

        for line in lines:
            # Look for direct actor definitions
            match = actor_pattern.search(line)
            if match:
                actor_name = match.group(1).strip()
                actor_alias = match.group(2) if match.group(2) else actor_name

                # For actors with special format like ":Name:"
                if actor_name.startswith(':') and actor_name.endswith(':'):
                    actor_name = actor_name[1:-1].strip()

                actors.append({'name': actor_name, 'alias': actor_alias, 'type': 'actor'})
                qtd_actors += 1

        # Second pass to identify actors in inheritance relationships that weren't explicitly defined
        for line in lines:
            if '<|--' in line:
                match = inheritance_pattern.search(line)
                if match:
                    parent = match.group(1).strip()
                    child = match.group(2).strip()

                    # Check if actors are already in the list
                    parent_exists = False
                    child_exists = False

                    for actor in actors:
                        if actor['alias'] == parent:
                            parent_exists = True
                        if actor['alias'] == child:
                            child_exists = True

                    # Add actors to the list if not present
                    if not parent_exists:
                        actors.append({'name': parent, 'alias': parent, 'type': 'actor'})
                        qtd_actors += 1

                    if not child_exists:
                        actors.append({'name': child, 'alias': child, 'type': 'inherited actor'})
                        qtd_actors += 1

        return actors, qtd_actors

    def get_use_cases(self, lines: List[str]) -> None:
        """
        Extracts use cases from diagram.
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        use_cases = []
        qtd_use_cases = 0

        # Pattern for directly defined use cases
        usecase_pattern1 = re.compile(r'\(([^)]+)\)(?:\s+as\s+([^\s]+))?')
        usecase_pattern2 = re.compile(r'usecase\s+"([^"]+)"(?:\s+as\s+([^\s]+))?')

        # Pattern for use cases in relationships
        relation_usecase_pattern = re.compile(r'\(([^)]+)\)\s+\.>\s+')

        # First, look for directly defined use cases
        for line in lines:
            # Ignore lines that are clearly relationships
            if ('<|--' in line) or ('-->' in line and '(' not in line) or ('->' in line and '(' not in line):
                continue

            # Look for use cases in format (Case Name)
            for match in usecase_pattern1.finditer(line):
                usecase_name = match.group(1).strip()
                usecase_alias = match.group(2) if match.group(2) else usecase_name

                # Check if this use case has already been added
                if not any(uc['name'] == usecase_name for uc in use_cases):
                    use_cases.append({'name': usecase_name, 'alias': usecase_alias, 'type': 'use case'})
                    qtd_use_cases += 1

            # Look for use cases in format usecase "Case Name"
            for match in usecase_pattern2.finditer(line):
                usecase_name = match.group(1).strip()
                usecase_alias = match.group(2) if match.group(2) else usecase_name

                if not any(uc['name'] == usecase_name for uc in use_cases):
                    use_cases.append({'name': usecase_name, 'alias': usecase_alias, 'type': 'use case'})
                    qtd_use_cases += 1

        # Now, look for use cases in extension/inclusion relationships
        for line in lines:
            if '.>' in line and '(' in line:
                match = relation_usecase_pattern.search(line)
                if match:
                    usecase_name = match.group(1).strip()

                    # Check if this use case has already been added
                    if not any(uc['name'] == usecase_name for uc in use_cases):
                        use_cases.append({'name': usecase_name, 'alias': usecase_name,
                                          'type': 'extensio/inclusion use case'})
                        qtd_use_cases += 1

        return use_cases, qtd_use_cases

    def get_rectangles(self, lines: List[str]) -> None:
        """
        Extracts rectangles (systems/packages) from diagram.
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        rectangles = []
        qtd_rectangles = 0

        in_rectangle = False
        rectangle_name = ""
        rectangle_content = []
        open_braces = 0

        for i, line in enumerate(lines):
            # Detect the start of a rectangle
            if 'rectangle ' in line and '{' in line:
                in_rectangle = True
                open_braces = 1
                rectangle_name = line.split('rectangle ')[1].split(' {')[0].strip()
                continue

            # Track opening and closing braces to handle nested rectangles
            if in_rectangle:
                if '{' in line:
                    open_braces += line.count('{')
                if '}' in line:
                    open_braces -= line.count('}')

                # When all braces are closed, end the rectangle
                if open_braces == 0:
                    rectangles.append({
                        'name': rectangle_name,
                        'content': rectangle_content,
                        'type': 'rectangle'
                    })
                    qtd_rectangles += 1
                    in_rectangle = False
                    rectangle_name = ""
                    rectangle_content = []
                else:
                    # Add line to rectangle content if it's not the closing line
                    if not line.strip() == '}':
                        rectangle_content.append(line)

        return rectangles, qtd_rectangles

    def get_relationships(self, lines: List[str]) -> None:
        """
        Extracts relationships from diagram.
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        relationships = []
        qtd_relationships = 0

        # Patterns for different types of relationships
        relationship_patterns = {
            'extension': re.compile(r'\(([^)]+)\)\s+\.+>\s+\(?([^)\s:]+).*?:\s*extends?'),
            'inclusion': re.compile(r'\(([^)]+)\)\s+\.+>\s+\(?([^)\s:]+).*?:\s*includes?'),
            'generalization': re.compile(r'([^\s]+)\s+<\|--\s+([^\s]+)')
        }

        # Define association patterns
        association_patterns = [
            re.compile(r'([^\s(]+)\s+-->\s+\(?([^)\s:]+)'),
            re.compile(r'([^\s(]+)\s+->\s+\(?([^)\s:]+)'),
            re.compile(r'([^\s(]+)\s+--\s+\(?([^)\s:]+)'),
            re.compile(r'\(([^)]+)\)\s+-->\s+([^\s:]+)'),
            re.compile(r'\(([^)]+)\)\s+->\s+([^\s:]+)'),
            re.compile(r'\(([^)]+)\)\s+--\s+([^\s:]+)')
        ]

        for line in lines:
            # Process extensions and inclusions
            for rel_type, pattern in relationship_patterns.items():
                for match in pattern.finditer(line):
                    source = match.group(1).strip()
                    target = match.group(2).strip()

                    # Remove parentheses if any
                    if target.startswith('(') and target.endswith(')'):
                        target = target[1:-1].strip()

                    relationships.append({
                        'source': source,
                        'target': target,
                        'type': 'relationship',
                        'kind': rel_type
                    })
                    qtd_relationships += 1

            # Process associations using all patterns
            for pattern in association_patterns:
                for match in pattern.finditer(line):
                    # Skip if it's an extend/include relationship
                    if '.>' in line and ':' in line:
                        continue
                        
                    source = match.group(1).strip()
                    target = match.group(2).strip()

                    # Remove parentheses if any
                    if target.startswith('(') and target.endswith(')'):
                        target = target[1:-1].strip()

                    relationships.append({
                        'source': source,
                        'target': target,
                        'type': 'relationship',
                        'kind': 'association'
                    })
                    qtd_relationships += 1

        return relationships, qtd_relationships

    def get_notes(self, lines: List[str]) -> None:
        """
        Extracts notes from diagram.
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        notes = []
        qtd_notes = 0
        
        in_note = False
        note_content = []
        note_target = ""

        for i, line in enumerate(lines):
            # Detect the start of a note
            if line.startswith('note ') and 'of ' in line:
                in_note = True
                parts = line.split('of ')
                if len(parts) >= 2:
                    note_target = parts[1].strip()
                continue

            # Detect the end of a note
            if in_note and line == 'end note':
                notes.append({
                    'target': note_target,
                    'type': 'note',
                    'content': '\n'.join(note_content)
                })
                qtd_notes += 1
                in_note = False
                note_content = []
                note_target = ""
                continue

            # Add content to the note
            if in_note:
                note_content.append(line)

        return notes, qtd_notes

    def get_summary_text(self, lines: List[str]) -> str:
        """
        Generates a text summary of diagram components.
        Returns:
            str: Summary text
        """
        diagram = self.parse(lines)

        total = diagram.count

        lines = ["\n=== USE CASE DIAGRAM ANALYSIS ===\n"]

        if diagram.title:
            lines.append(f"|DIAGRAM TITLE: {diagram.title:<13}|")

        # Count table
        lines.append("ELEMENT COUNT:")
        lines.append("-" * 30)
        lines.append(f"| {'Element':<15} | {'Count':<10} |")
        lines.append("-" * 30)
        lines.append(f"| actors: | {diagram.detailed_count['actors']:<10} |")
        lines.append(f"| use cases: | {diagram.detailed_count['use_cases']:<10} |")
        lines.append(f"| relationships: | {diagram.detailed_count['relationships']:<10} |")
        lines.append(f"| notes: | {diagram.detailed_count['notes']:<10} |")
        lines.append(f"| rectangles: | {diagram.detailed_count['rectangles']:<10} |")
        lines.append("-" * 30)
        lines.append(f"| {'Total':<15} | {total:<10} |")
        lines.append("-" * 30)

        # Element details
        lines.append("\nELEMENT DETAILS:")

        if diagram['actors']:
            lines.append("\nACTORS:")
            for i, actor in diagram['actors']:
                lines.append(f"  {i}. {actor['name']} (alias: {actor['alias']}) (type: {actor['type']})")

        if diagram['use_cases']:
            lines.append("\nUSE CASES:")
            for i, use_cases in diagram['use_cases']:
                lines.append(f"  {i}. {use_cases['use_cases']} (alias: {use_cases['use_cases']}) (type: {
                    use_cases['use_cases']})")

        if diagram['relationships']:
            lines.append("\nRELATIONSHIPS:")
            for i, rel in diagram['relationships']:
                lines.append(f"  {i}. {rel['source']} --> {rel['target']} [{rel['type']}] [{rel['kind']}]")

        if diagram['notes']:
            lines.append("\nNOTES:")
            for i, note in enumerate(diagram['notes'], 1):
                lines.append(f"  {i}. Note for {note['target']}:")
                for line in note['content'].split('\n'):
                    lines.append(f"     {line}")

        if diagram['rectangles']:
            lines.append("\nSYSTEMS/PACKAGES:")
            for i, rect in enumerate(diagram['rectangles'], 1):
                lines.append(f"  {i}. {rect['name']}")

        return '\n'.join(lines)