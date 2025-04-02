import re
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Any, Union
from utils.logger import Logger

LOGGER = Logger

class PlantUMLUseCaseParser:
    """
    Internal parser for PlantUML use case diagrams.
    This class performs detailed analysis of PlantUML code.
    """
    def __init__(self):
        self.elements = defaultdict(list)
        self.counts = {
            'actors': 0,
            'use_cases': 0,
            'relationships': 0, 
            'notes': 0,
            'rectangles': 0
        }
        self.title = None

    def parse(self, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Analyzes PlantUML code and extracts diagram elements.

        Args:
            plantuml_code (str): PlantUML code to analyze

        Returns:
            Tuple: (extracted elements, element counts)
        """
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
        self.title = None
        for line in cleaned_lines:
            if line.startswith('title '):
                self.title = line[6:].strip()
                break

        # Reset elements and counts before starting analysis
        self._reset()
        
        # Parse elements
        self._parse_actors(cleaned_lines)
        self._parse_use_cases(cleaned_lines)
        self._parse_rectangles(cleaned_lines)
        self._parse_relationships(cleaned_lines)
        self._parse_notes(cleaned_lines)
        
        return self.elements, self.counts
    
    def _reset(self) -> None:
        """Resets the parser state for a new analysis."""
        self.elements = defaultdict(list)
        self.counts = {
            'actors': 0,
            'use_cases': 0,
            'relationships': 0, 
            'notes': 0,
            'rectangles': 0
        }
    
    def _parse_actors(self, lines: List[str]) -> None:
        """
        Extracts actors from diagram.
        
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
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
                
                self.elements['actors'].append({'name': actor_name, 'alias': actor_alias})
                self.counts['actors'] += 1
        
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
                    
                    for actor in self.elements['actors']:
                        if actor['alias'] == parent:
                            parent_exists = True
                        if actor['alias'] == child:
                            child_exists = True
                    
                    # Add actors to the list if not present
                    if not parent_exists:
                        self.elements['actors'].append({'name': parent, 'alias': parent})
                        self.counts['actors'] += 1
                    
                    if not child_exists:
                        self.elements['actors'].append({'name': child, 'alias': child})
                        self.counts['actors'] += 1
    
    def _parse_use_cases(self, lines: List[str]) -> None:
        """
        Extracts use cases from diagram.
        
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
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
                if not any(uc['name'] == usecase_name for uc in self.elements['use_cases']):
                    self.elements['use_cases'].append({'name': usecase_name, 'alias': usecase_alias})
                    self.counts['use_cases'] += 1
            
            # Look for use cases in format usecase "Case Name"
            for match in usecase_pattern2.finditer(line):
                usecase_name = match.group(1).strip()
                usecase_alias = match.group(2) if match.group(2) else usecase_name
                
                if not any(uc['name'] == usecase_name for uc in self.elements['use_cases']):
                    self.elements['use_cases'].append({'name': usecase_name, 'alias': usecase_alias})
                    self.counts['use_cases'] += 1
        
        # Now, look for use cases in extension/inclusion relationships
        for line in lines:
            if '.>' in line and '(' in line:
                match = relation_usecase_pattern.search(line)
                if match:
                    usecase_name = match.group(1).strip()
                    
                    # Check if this use case has already been added
                    if not any(uc['name'] == usecase_name for uc in self.elements['use_cases']):
                        self.elements['use_cases'].append({'name': usecase_name, 'alias': usecase_name})
                        self.counts['use_cases'] += 1
    
    def _parse_rectangles(self, lines: List[str]) -> None:
        """
        Extracts rectangles (systems/packages) from diagram.
        
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
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
                    self.elements['rectangles'].append({
                        'name': rectangle_name,
                        'content': rectangle_content
                    })
                    self.counts['rectangles'] += 1
                    in_rectangle = False
                    rectangle_name = ""
                    rectangle_content = []
                else:
                    # Add line to rectangle content if it's not the closing line
                    if not line.strip() == '}':
                        rectangle_content.append(line)
    
    def _parse_relationships(self, lines: List[str]) -> None:
        """
        Extracts relationships from diagram.
        
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
        # Patterns for different types of relationships
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
            # Process extensions
            for match in extend_pattern.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parentheses if any
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'extension'
                })
                self.counts['relationships'] += 1
            
            # Process inclusions
            for match in include_pattern.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parentheses if any
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'inclusion'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 1
            for match in association_pattern1.finditer(line):
                if '.>' in line and ':' in line:  # Ignore if it's an extend/include relationship
                    continue
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parentheses if any
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 2
            for match in association_pattern2.finditer(line):
                if '.>' in line and ':' in line:  # Ignore if it's an extend/include relationship
                    continue
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parentheses if any
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 3
            for match in association_pattern3.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                # Remove parentheses if any
                if target.startswith('(') and target.endswith(')'):
                    target = target[1:-1].strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 4
            for match in association_pattern4.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 5
            for match in association_pattern5.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process associations - pattern 6
            for match in association_pattern6.finditer(line):
                source = match.group(1).strip()
                target = match.group(2).strip()
                
                self.elements['relationships'].append({
                    'source': source,
                    'target': target,
                    'type': 'association'
                })
                self.counts['relationships'] += 1
            
            # Process generalizations
            for match in generalization_pattern.finditer(line):
                parent = match.group(1).strip()
                child = match.group(2).strip()
                
                self.elements['relationships'].append({
                    'source': parent,
                    'target': child,
                    'type': 'generalization'
                })
                self.counts['relationships'] += 1
    
    def _parse_notes(self, lines: List[str]) -> None:
        """
        Extracts notes from diagram.
        
        Args:
            lines (List[str]): Cleaned PlantUML code lines
        """
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
                self.elements['notes'].append({
                    'target': note_target,
                    'content': '\n'.join(note_content)
                })
                self.counts['notes'] += 1
                in_note = False
                note_content = []
                note_target = ""
                continue
            
            # Add content to the note
            if in_note:
                note_content.append(line)
    
    def get_summary_text(self) -> str:
        """
        Generates a text summary of diagram components.
        
        Returns:
            str: Summary text
        """
        total = sum(self.counts.values())
        
        lines = []
        lines.append("\n=== USE CASE DIAGRAM ANALYSIS ===\n")
        
        # Count table
        lines.append("ELEMENT COUNT:")
        lines.append("-" * 30)
        lines.append(f"| {'Element':<15} | {'Count':<10} |")
        lines.append("-" * 30)
        for element, count in self.counts.items():
            lines.append(f"| {element.replace('_', ' ').title():<15} | {count:<10} |")
        lines.append("-" * 30)
        lines.append(f"| {'Total':<15} | {total:<10} |")
        lines.append("-" * 30)
        
        # Element details
        lines.append("\nELEMENT DETAILS:")
        
        if self.elements['actors']:
            lines.append("\nACTORS:")
            for i, actor in enumerate(self.elements['actors'], 1):
                if actor['alias'] != actor['name']:
                    lines.append(f"  {i}. {actor['name']} (alias: {actor['alias']})")
                else:
                    lines.append(f"  {i}. {actor['name']}")
        
        if self.elements['use_cases']:
            lines.append("\nUSE CASES:")
            for i, usecase in enumerate(self.elements['use_cases'], 1):
                if usecase['alias'] != usecase['name']:
                    lines.append(f"  {i}. {usecase['name']} (alias: {usecase['alias']})")
                else:
                    lines.append(f"  {i}. {usecase['name']}")
        
        if self.elements['relationships']:
            lines.append("\nRELATIONSHIPS:")
            for i, rel in enumerate(self.elements['relationships'], 1):
                lines.append(f"  {i}. {rel['source']} --> {rel['target']} [{rel['type']}]")
        
        if self.elements['notes']:
            lines.append("\nNOTES:")
            for i, note in enumerate(self.elements['notes'], 1):
                lines.append(f"  {i}. Note for {note['target']}:")
                for line in note['content'].split('\n'):
                    lines.append(f"     {line}")
        
        if self.elements['rectangles']:
            lines.append("\nSYSTEMS/PACKAGES:")
            for i, rect in enumerate(self.elements['rectangles'], 1):
                lines.append(f"  {i}. {rect['name']}")
        
        if self.title:
            lines.append(f"\nDIAGRAM TITLE: {self.title}")
            
        return '\n'.join(lines)
    
    def print_summary(self) -> None:
        """Prints a summary of the diagram."""
        LOGGER.info(self.get_summary_text())


class PlantUMLUseCase:
    """
    Facade for extracting components from PlantUML use case diagrams.
    Provides a simplified API for diagram analysis.
    """
    _last_code = None
    _last_elements = None
    _last_counts = None
    
    @classmethod
    def _get_parsed_data(cls, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Returns parsed data, using cache when possible.
        
        Args:
            plantuml_code (str): PlantUML code to analyze
            
        Returns:
            Tuple: (extracted elements, element counts)
        """
        # Use cache if code is the same as last time
        if cls._last_code == plantuml_code and cls._last_elements and cls._last_counts:
            return cls._last_elements, cls._last_counts
        
        # Otherwise, run the parser
        parser = PlantUMLUseCaseParser()
        elements, counts = parser.parse(plantuml_code)
        
        # Update cache
        cls._last_code = plantuml_code
        cls._last_elements = elements
        cls._last_counts = counts
        
        return elements, counts
    
    @classmethod
    def validate_code(cls, plantuml_code: str) -> bool:
        """
        Validates if the PlantUML code is a valid use case diagram.
        
        Args:
            plantuml_code (str): PlantUML code to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Check if code has mandatory markers
        if '@startuml' not in plantuml_code or '@enduml' not in plantuml_code:
            return False
            
        # Check if there's at least one actor or use case
        _, counts = cls._get_parsed_data(plantuml_code)
        return counts['actors'] > 0 or counts['use_cases'] > 0
    
    @classmethod
    def extract_components(cls, plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
        """
        Extracts all components from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            Tuple: (extracted elements, element counts)
        """
        return cls._get_parsed_data(plantuml_code)
    
    @classmethod
    def extract_actors(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extracts only the actors from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            List[Dict[str, str]]: List of actors in format [{'name': name, 'alias': alias}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['actors']
    
    @classmethod
    def extract_use_cases(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extracts only the use cases from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            List[Dict[str, str]]: List of use cases in format [{'name': name, 'alias': alias}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['use_cases']
    
    @classmethod
    def extract_relationships(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extracts only the relationships from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            List[Dict[str, str]]: List of relationships in format 
                                 [{'source': source, 'target': target, 'type': type}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['relationships']
    
    @classmethod
    def extract_systems(cls, plantuml_code: str) -> List[Dict[str, Union[str, List[str]]]]:
        """
        Extracts only the systems/packages (rectangles) from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            List[Dict[str, Union[str, List[str]]]]: List of systems/packages in format 
                                                  [{'name': name, 'content': [content]}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['rectangles']
    
    @classmethod
    def extract_notes(cls, plantuml_code: str) -> List[Dict[str, str]]:
        """
        Extracts only the notes from the diagram.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            List[Dict[str, str]]: List of notes in format [{'target': target, 'content': content}, ...]
        """
        elements, _ = cls._get_parsed_data(plantuml_code)
        return elements['notes']
    
    @classmethod
    def extract_title(cls, plantuml_code: str) -> Optional[str]:
        """
        Extracts the diagram title, if any.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            Optional[str]: Diagram title or None if none exists
        """
        parser = PlantUMLUseCaseParser()
        parser.parse(plantuml_code)
        return parser.title
    
    @classmethod
    def get_summary(cls, plantuml_code: str) -> str:
        """
        Generates a text summary of diagram components.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
            
        Returns:
            str: Formatted summary of diagram components
        """
        parser = PlantUMLUseCaseParser()
        parser.parse(plantuml_code)
        return parser.get_summary_text()
    
    @classmethod
    def print_summary(cls, plantuml_code: str) -> None:
        """
        Prints a summary of diagram components.
        
        Args:
            plantuml_code (str): PlantUML use case diagram code
        """
        LOGGER.info(cls.get_summary(plantuml_code))


# Legacy function for compatibility with existing code
def analyze_plantuml_use_case(plantuml_code: str) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, int]]:
    """
    Analyzes a PlantUML use case diagram and prints a summary.
    
    Args:
        plantuml_code (str): PlantUML use case diagram code
        
    Returns:
        Tuple: (extracted elements, element counts)
    """
    PlantUMLUseCase.print_summary(plantuml_code)
    return PlantUMLUseCase.extract_components(plantuml_code)


# Example usage
if __name__ == "__main__":
    # Simple example of a use case diagram
    example_plantuml = """
@startuml
left to right direction
actor Customer
actor Employee
rectangle "Reservation System" {
    (Make Reservation) as MR
    (Cancel Reservation) as CR
    (Modify Reservation) as ModR
    (Check Availability) as CA
    (Issue Receipt) as IR
    
    MR --> CA : include
    CR --> MR : extends
    ModR --> MR : extends
    MR --> IR : include
}

Customer --> MR
Customer --> CR
Customer --> ModR
Employee --> MR
Employee --> CR
Employee --> ModR
Employee --> CA

note right of Employee : Employees have access to all functionalities

@enduml
"""

    # Examples of using the new API
    LOGGER.info("\n===== EXAMPLE USING THE NEW API =====\n")
    
    # Validate the code
    if PlantUMLUseCase.validate_code(example_plantuml):
        LOGGER.info("The PlantUML code is valid.")
    else:
        LOGGER.info("The PlantUML code is invalid.")
    
    LOGGER.info("\n-- Extracting Actors --")
    actors = PlantUMLUseCase.extract_actors(example_plantuml)
    for actor in actors:
        LOGGER.info(f"Actor: {actor['name']}")
    
    LOGGER.info("\n-- Extracting Use Cases --")
    use_cases = PlantUMLUseCase.extract_use_cases(example_plantuml)
    for case in use_cases:
        LOGGER.info(f"Use Case: {case['name']}")
    
    LOGGER.info("\n-- Extracting Relationships --")
    relationships = PlantUMLUseCase.extract_relationships(example_plantuml)
    for rel in relationships:
        LOGGER.info(f"Relationship: {rel['source']} -> {rel['target']} ({rel['type']})")
    
    LOGGER.info("\n-- Extracting Systems/Packages --")
    systems = PlantUMLUseCase.extract_systems(example_plantuml)
    for system in systems:
        LOGGER.info(f"System: {system['name']}")
    
    LOGGER.info("\n-- Extracting Notes --")
    notes = PlantUMLUseCase.extract_notes(example_plantuml)
    for note in notes:
        LOGGER.info(f"Note for {note['target']}: {note['content']}")
    
    LOGGER.info("\n-- Complete Diagram Summary --")
    LOGGER.info(PlantUMLUseCase.get_summary(example_plantuml))
    
    # Example using the legacy function for compatibility
    LOGGER.info("\n===== EXAMPLE USING THE LEGACY FUNCTION =====\n")
    elements, counts = analyze_plantuml_use_case(example_plantuml)