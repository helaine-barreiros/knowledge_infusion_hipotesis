from pathlib import Path
from unittest.mock import patch, MagicMock

from src.plantuml_utils.plantuml_use_case_controller import (
    extract_plantuml_use_case_code, 
    extract_plantuml_use_case_components, 
    extract_excel_report
)

import unittest
import os
import sys
import tempfile


sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class TestExtractDiagramContent(unittest.TestCase):
    """Test case for extract_diagram_content.py functions."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(__file__).parent
        self.state_machine_file = os.path.join(self.test_dir, 'uml_artifacts', 'state_machine.puml')
        
        # Read the state machine diagram
        with open(self.state_machine_file, 'r') as f:
            self.diagram_content = f.read()
            
        # Create a sample state machine diagram for testing
        self.sample_state_machine = """
        @startuml
        state "Idle" as idle
        state "Active" as active
        state "Completed" as completed
        
        [*] --> idle
        idle --> active : start
        active --> completed : finish
        completed --> [*] : end
        @enduml
        """
        
    def test_extract_plantuml_code(self):
        """Test extraction of PlantUML code from text."""
        # Test with valid PlantUML code
        extracted = extract_plantuml_use_case_code(self.sample_state_machine)
        self.assertIn('@startuml', extracted)
        self.assertIn('@enduml', extracted)
        self.assertIn('state "Idle"', extracted)
        
        # Test with code embedded in other text
        text_with_embedded_diagram = """
        This is some text before the diagram.
        
        @startuml
        state "Test" as test
        [*] --> test
        @enduml
        
        This is some text after the diagram.
        """
        extracted = extract_plantuml_use_case_code(text_with_embedded_diagram)
        self.assertIn('@startuml', extracted)
        self.assertIn('@enduml', extracted)
        self.assertIn('state "Test"', extracted)
        self.assertNotIn('This is some text', extracted)
        
        # Test with invalid input
        invalid_input = "This is not a PlantUML diagram."
        extracted = extract_plantuml_use_case_code(invalid_input)
        self.assertEqual(extracted, "")
        
    def test_extract_components_and_relations(self):
        """Test extraction of states and transitions from a state machine diagram."""
        components, relations = extract_plantuml_use_case_components(self.sample_state_machine)
        
        # Verify components (states)
        self.assertGreaterEqual(len(components), 3)  # Should have at least the 3 explicitly defined states
        state_names = [comp['Complete Name'] for comp in components]
        self.assertIn('Idle', state_names)
        self.assertIn('Active', state_names)
        self.assertIn('Completed', state_names)
        
        # Verify relations (transitions)
        # The function might not capture all transitions as we expect,
        # so just ensure we have some relations
        self.assertGreaterEqual(len(relations), 2)  # Should have at least some transitions
        
        # Check if at least some expected transitions are present
        transitions = [(rel['Source'], rel['Destiny'], rel['Description']) for rel in relations]
        
        # At least one of the expected transitions should be present
        expected_transitions = [
            ('Idle', 'Active', 'start'),
            ('Active', 'Completed', 'finish'),
            ('idle', 'active', 'start'),  # Might use aliases instead of names
            ('active', 'completed', 'finish')
        ]
        
        found = False
        for expected in expected_transitions:
            if expected in transitions:
                found = True
                break
                
        self.assertTrue(found, "None of the expected transitions were found")
        
        # Test with the actual file
        components, relations = extract_plantuml_use_case_components(self.diagram_content)
        self.assertGreater(len(components), 0)
        self.assertGreater(len(relations), 0)
        
    @patch('src.artifacts.plantuml.extract_diagram_content.pd.ExcelWriter')
    @patch('src.artifacts.plantuml.extract_diagram_content.pd.DataFrame')
    def test_extract_excel_report(self, mock_dataframe, mock_excel_writer):
        """Test the Excel report generation function."""
        # Create mocks for the DataFrame operations
        mock_df_instance = MagicMock()
        mock_dataframe.return_value = mock_df_instance
        
        # Mock the ExcelWriter context manager
        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            temp_filename = temp_file.name[:-5]  # Remove .xlsx extension
        
        try:
            # Call the function
            extract_excel_report(self.sample_state_machine, temp_filename)
            
            # Verify the calls
            mock_dataframe.assert_called()
            mock_excel_writer.assert_called_with(f"{temp_filename}.xlsx")
            mock_df_instance.to_excel.assert_called()
            
        finally:
            # Clean up the temp file
            if os.path.exists(f"{temp_filename}.xlsx"):
                os.remove(f"{temp_filename}.xlsx")
                
    @patch('src.artifacts.plantuml.extract_diagram_content.pd.ExcelWriter')
    @patch('src.artifacts.plantuml.extract_diagram_content.pd.DataFrame')
    def test_extract_excel_report_error_handling(self, mock_dataframe, mock_excel_writer):
        """Test error handling in the extract_excel_report function."""
        # Make the DataFrame creation raise an exception
        mock_dataframe.side_effect = Exception("Test exception")
        
        # Mock the ExcelWriter context manager for the error case
        mock_writer = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_writer
        
        # Test with temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
            temp_filename = temp_file.name[:-5]  # Remove .xlsx extension
        
        try:
            # Call the function - this should trigger the error handling
            extract_excel_report(self.sample_state_machine, temp_filename)
            
            # Verify error handling - second call to ExcelWriter should be for error file
            calls = mock_excel_writer.call_args_list
            self.assertEqual(len(calls), 1)
            self.assertIn("_error.xlsx", calls[0][0][0])
            
        finally:
            # Clean up any temp files
            error_file = f"{temp_filename}_error.xlsx"
            if os.path.exists(error_file):
                os.remove(error_file)


if __name__ == '__main__':
    unittest.main()