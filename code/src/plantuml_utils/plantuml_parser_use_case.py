from src.utils.logger import Logger
from plantuml import PlantUML
from pathlib import Path
from src.utils.system_parametrization import SYSTEM_CONFIG

import subprocess
import json
import os


class Actor:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class UseCase:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Relationship:
    def __init__(self, source, target, relationship_type, label):
        self.source = source
        self.target = target
        self.type = relationship_type
        self.label = label


class Package:
    def __init__(self, id, name, elements):
        self.id = id
        self.name = name
        self.elements = elements


class Rectangle:
    def __init__(self, id, name, elements):
        self.id = id
        self.name = name
        self.elements = elements


class PlantUMLUseCaseParser:
    """
    Parser for PlantUML use case diagrams.
    This class performs detailed analysis of PlantUML code.
    """
    def __init__(self, fullname_plantuml_file: str):
        self.LOGGER = Logger
        self.plantuml_code = fullname_plantuml_file
        self.fullname_plantuml_file = fullname_plantuml_file
        self.PLANT_UML_URL = SYSTEM_CONFIG.get("artifacts.plantuml_png_url", "http://www.plantuml.com/plantuml/png/")
        self.PLANTUML_SERVER = PlantUML(url=self.PLANT_UML_URL)

        self.json = self._call_external_plantuml_parser(fullname_plantuml_file)

        self._parse(self.json)

    def get_use_case_diagram(self):
        return self.diagram

    def get_actors(self) -> None:
        return self.diagram['actors'], len(self.diagram['actors'])

    def get_use_cases(self) -> None:
        return self.diagram['usecases'], len(self.diagram['usecases'])

    def get_rectangles(self) -> None:
        return self.diagram['rectangles'], len(self.diagram['rectangles'])

    def get_relationships(self) -> None:
        return self.diagram['relationships'], len(self.diagram['relationships'])

    def generate_image_bytes(self):
        diagram_image = None

        try:
            diagram_image = self.PLANTUML_SERVER.processes(self.plantuml_code)

        except Exception as e:
            self.LOGGER.info(f"Could not generate usecase diagram byte image: {str(e)}")

        return diagram_image

    def _parse_element(self, element):
        type = element.get("type")

        if type == "Actor":
            return Actor(id=element["name"], name=element["title"])
        elif type == "UseCase":
            return UseCase(id=element["name"], name=element["title"])
        elif type == "Package":
            subelements = [self.parse_element(e) for e in element.get("elements", [])]
            return Package(id=element["name"], name=element["title"], elements=subelements)
        elif type == "Rectangle":
            subelements = [self.parse_element(e) for e in element.get("elements", [])]
            return Rectangle(id=element["name"], name=element["title"], elements=subelements)
        elif type == "Relationship":
            return Relationship(
                source=element["source"],
                target=element["target"],
                relationship_type=element["relationshipType"],
                label=element["label"]
            )
        else:
            raise ValueError(f"Unrecognized Type: {type}")

    def _parse_rectangles(self, rectangles_data):
        rectangles = []

        for rect in rectangles_data:
            elements = [self._parse_element(el) for el in rect.get("elements", [])]
            rectangles.append(Rectangle(id=rect["name"], name=rect["title"], elements=elements))

        return rectangles

    def _parse_packages(self, packages_data):
        packages = []

        for pkg in packages_data:
            elements = [self._parse_element({**el, "type": "UseCase"}) for el in pkg.get("elements", [])]
            packages.append(Package(id=pkg["name"], name=pkg["title"], elements=elements))

        return packages

    def _parse_actors(self, actors_data):
        return [Actor(id=el["name"], name=el["title"]) for el in actors_data]

    def _parse_usecases(self, usecases_data):
        return [UseCase(id=el["name"], name=el["title"]) for el in usecases_data]

    def _parse_relationships(self, relationships_data):
        return [
            Relationship(
                source=el["source"],
                target=el["target"],
                relationship_type=el["relationshipType"],
                label=el["label"]
            )
            for el in relationships_data
        ]

    def _parse(self, data: dict):

        diagram = {
            'type': 'use case',
            'title': "",
            'elements': [],
            'count': 0,
            'detailed_count': {}
        }

        if not data:
            diagram['compile'] = "Error"
            self.LOGGER.info(f"Error compiling diagram {self.plantuml_code}")
            self.diagram = diagram
        else:

            plantuml_basename = os.path.basename(self.fullname_plantuml_file)
            diagram_base_name, _ = os.path.splitext(plantuml_basename)

            diagram['base_name'] = diagram_base_name

            diagram['compile'] = True if len(self.plantuml_code) > 0 else False
            self.LOGGER.info(f"Compiled diagram {diagram['compile']} existent source code:{len(self.plantuml_code) > 0}")

            if diagram['compile']:
                try:
                    self.LOGGER.info("Compiling diagram")
                    diagram['compile'] = self._verify_diagram_compilation()
                    self.LOGGER.info(f"Compiled diagram {self.plantuml_code}")
                except Exception:
                    diagram['compile'] = False

            diagram['actors'] = self._parse_actors(data["actors"])
            diagram['usecases'] = self._parse_usecases(data["usecases"])
            diagram['relationships'] = self._parse_relationships(data["relationships"])
            diagram['packages'] = self._parse_packages(data["packages"])
            diagram['rectangles'] = self._parse_rectangles(data["rectangles"])

            diagram['detailed_count'] = {
                'actors': len(diagram['actors']),
                'use_cases': len(diagram['usecases']),
                'relationships': len(diagram['relationships']),
                'rectangles': len(diagram['rectangles']),
                'packages': len(diagram['packages'])
            }

            diagram['count'] = len(diagram['actors']) + len(diagram['usecases']) + len(diagram['relationships']) + len(diagram['rectangles']) + len(diagram['packages'])

            self.diagram = diagram

    def _call_external_plantuml_parser(self, fullname_plantuml_file):
        result = []

        command = ['plantuml-parser-hsl', '-i', fullname_plantuml_file, '-f', "usecase_structured"]

        try:
            completed_process = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True,
                timeout=30  # Prevent indefinite hang
            )

            try:
                parsed_json = json.loads(completed_process.stdout)
                return parsed_json
            except json.JSONDecodeError as e:
                self.LOGGER.error(f"Failed to parse JSON output from PlantUML parser error: {e}")
                self.LOGGER.debug(f"Raw output from parser:\n{completed_process.stdout}")
   
        except subprocess.TimeoutExpired as e:
            self.LOGGER.critical(f"Timeout expired while executing external parser: {e}")

        except FileNotFoundError as e:
            self.LOGGER.critical(f"Command not found: {command[0]} — {e}")

        except subprocess.CalledProcessError as e:
            self.LOGGER.error("Subprocess returned non-zero exit status.")
            self.LOGGER.debug(f"Standard error output:\n{e.stderr}")

        except Exception as e:
            self.LOGGER.exception(f"Unexpected error while executing external parser: {e}")

        return result

    import subprocess

    def _verify_diagram_compilation(self):
        """
        Verifica se o diagrama PlantUML compila corretamente utilizando a opção -checkonly.

        Retorna:
            bool: True se o diagrama compilar corretamente, False caso contrário.
        """
        ROOT_DIR = Path(__file__).resolve().parent
        PROJECT_ROOT = ROOT_DIR.parent
        caminho_plantuml_jar = PROJECT_ROOT / 'utils' / 'plantuml.jar'

        evaluation = False

        try:
            result = subprocess.run(
                ['java', '-jar', caminho_plantuml_jar, '-checkonly', self.fullname_plantuml_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Verifica se a execução foi bem-sucedida
            if result.returncode == 0:
                # Mesmo com código 0, checamos se há mensagens de erro não críticas em stderr
                if not result.stderr.strip():
                    evaluation = True
                else:
                    self.LOGGER.warning(f"Diagram compiled with messages on stderr: {result.stderr.strip()}")
            else:
                self.LOGGER.error(f"PlantUML compilation error (code {result.returncode}):\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

        except Exception as e:
            self.LOGGER.exception(f'Exception when checking diagram compilation: {e}')

        return evaluation
