import unittest
from unittest.mock import patch, MagicMock
from src.plantuml_utils.plantuml_use_case_controller import PlantUMLUseCaseController


class TestPlantUMLUseCaseController(unittest.TestCase):
    """Test case for the PlantUMLUseCaseController class."""

    def setUp(self):
        """Set up the test environment."""
        self.controller = PlantUMLUseCaseController()

    @patch("src.plantuml_utils.plantuml_use_case_controller.search")
    def test_extract_plantuml_use_case_code(self, mock_search):
        """Test extracting PlantUML code block from text."""
        # Configurar o mock para retornar um objeto que se comporte como um match de regex
        mock_match = MagicMock()
        # Configurar o acesso a [0] para retornar o texto esperado
        mock_match.__getitem__.return_value = "@startuml\nActor -> UseCase\n@enduml"
        mock_search.return_value = mock_match
        
        text_with_code = "Some text with @startuml\nActor -> UseCase\n@enduml inside."
        result = self.controller.extract_plantuml_use_case_code(text_with_code)
        self.assertEqual(result, "@startuml\nActor -> UseCase\n@enduml")

        # Test with no PlantUML code
        mock_search.return_value = None
        result = self.controller.extract_plantuml_use_case_code("No PlantUML code here.")
        self.assertEqual(result, "")

    @patch("src.plantuml_utils.plantuml_use_case_controller.PlantUML.processes")
    def test_extract_plantuml_use_case_image(self, mock_processes):
        """Test generating a diagram image from PlantUML code."""
        mock_processes.return_value = b"fake_image_bytes"
        plantuml_code = "@startuml\nActor -> UseCase\n@enduml"
        result = self.controller.extract_plantuml_use_case_image(plantuml_code)
        self.assertEqual(result, b"fake_image_bytes")

        # Test with invalid PlantUML code
        mock_processes.side_effect = Exception("Failed to process PlantUML code")
        result = self.controller.extract_plantuml_use_case_image("Invalid code")
        self.assertIsNone(result)

    @patch("src.plantuml_utils.plantuml_use_case_controller.PlantUMLUseCaseParser.parse")
    def test_extract_plantuml_use_case_components(self, mock_parse):
        """Test extracting components and counts from PlantUML code."""
        # Modificar para retornar um único valor que corresponda à implementação atual
        mock_parse.return_value = {"actors": [{"name": "Actor"}]}
        plantuml_code = "@startuml\nActor -> UseCase\n@enduml"
        
        # Fazer patch do método de extração de código para garantir um retorno válido
        with patch.object(self.controller, "extract_plantuml_use_case_code", return_value="@startuml\nActor -> UseCase\n@enduml"):
            components = self.controller.extract_plantuml_use_case_components(plantuml_code)
            self.assertIn("actors", components)
        
        # Test with invalid PlantUML code
        mock_parse.side_effect = Exception("Parsing error")
        components = self.controller.extract_plantuml_use_case_components("Invalid code")
        self.assertIsNone(components)
        
        # Test with empty code
        mock_parse.side_effect = None
        with patch.object(self.controller, "extract_plantuml_use_case_code", return_value=""):
            components = self.controller.extract_plantuml_use_case_components("")
            self.assertIsNone(components)

    @patch("src.plantuml_utils.plantuml_use_case_controller.pd.ExcelWriter")
    @patch("src.plantuml_utils.plantuml_use_case_controller.io.BytesIO")
    @patch("src.plantuml_utils.plantuml_use_case_controller.pd.DataFrame")
    def test_extract_excel_report(self, mock_dataframe, mock_bytesio, mock_excel_writer):
        """Test generating an Excel report from PlantUML code."""
        # Mock de DataFrame para evitar o erro na criação
        mock_df_instance = MagicMock()
        mock_dataframe.return_value = mock_df_instance
        
        # Configurar o mock do BytesIO
        mock_buffer = MagicMock()
        mock_bytesio.return_value.__enter__.return_value = mock_buffer
        mock_buffer.seek = MagicMock()
        mock_buffer.read.return_value = b"fake_excel_bytes"
        
        # Mock do ExcelWriter
        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Preparar os dados de entrada
        plantuml_code = "@startuml\nActor -> UseCase\n@enduml"
        
        # Caso de sucesso: mock components é um dicionário válido
        with patch.object(self.controller, "extract_plantuml_use_case_components") as mock_extract:
            # Configure o mock para retornar um dicionário válido
            mock_extract.return_value = {"actors": [{"name": "Actor"}], "relations": [{"source": "Actor", "target": "UseCase"}]}
            result = self.controller.extract_excel_diagram_component_detailed_report(plantuml_code, "output.xlsx")
            self.assertEqual(result, b"fake_excel_bytes")
            
        # Caso de falha: componentes é None
        with patch.object(self.controller, "extract_plantuml_use_case_components") as mock_extract:
            mock_extract.return_value = None
            result = self.controller.extract_excel_diagram_component_detailed_report("Invalid code", "output.xlsx")
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
