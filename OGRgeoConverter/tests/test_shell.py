from django.test import TestCase
from OGRgeoConverter.shell.shellcall import ArgumentList
from OGRgeoConverter.shell.shellcall import ShellCall
from OGRgeoConverter.shell import shell
from OGRgeoConverter.shell.shellresult import ShellResult

class ArgumentListTest(TestCase):
    '''
    Tests class ArgumentList
    '''
    
    def test_argument_string_empty_if_no_argument(self):
        arguments = ArgumentList()
        self.assertEqual(arguments.get_arguments_string(), "")
        
    def test_argument_string_contains_prefix_by_default(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue")
        argument_string = arguments.get_arguments_string()
        pos1 = argument_string.find("ExampleArgument")
        self.assertTrue(pos1 >= 1)
        
    def test_argument_string_contains_custom_prefix(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue", prefix="{myprefix}")
        argument_string = arguments.get_arguments_string()
        self.assertTrue(argument_string.find("{myprefix}")>=0)
        
    def test_argument_string_starts_with_prefix(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue", prefix="{myprefix}")
        argument_string = arguments.get_arguments_string()
        self.assertTrue(argument_string.startswith("{myprefix}"))
        
    def test_no_prefix_if_no_argument_name(self):
        arguments1 = ArgumentList()
        arguments1.add_argument(None, "ExampleValue", prefix="{myprefix}")
        argument_string1 = arguments1.get_arguments_string()
        self.assertTrue(argument_string1.find("{myprefix}") == -1)
        
        arguments2 = ArgumentList()
        arguments2.add_argument("", "ExampleValue", prefix="{myprefix}")
        argument_string2 = arguments2.get_arguments_string()
        self.assertTrue(argument_string2.find("{myprefix}") == -1)
        
    def test_argument_string_contains_quotation_marks_by_default(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue")
        argument_string = arguments.get_arguments_string()
        pos1 = argument_string.find("'ExampleValue'")
        pos2 = argument_string.find('"ExampleValue"')
        self.assertTrue(pos1 >= 0 or pos2 >= 0)
        
    def test_argument_string_quotation_marks_removable(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue", value_quotation_marks=False)
        argument_string = arguments.get_arguments_string()
        pos1 = argument_string.find("'")
        pos2 = argument_string.find('"')
        self.assertTrue(pos1==-1 and pos2==-1)
        
    def test_argument_string_contains_argument_name_and_value_in_correct_order(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue")
        argument_string = arguments.get_arguments_string()
        pos1 = argument_string.find("ExampleArgument")
        pos2 = argument_string.find("ExampleValue")
        self.assertTrue(pos1 >= 0 and pos1 < pos2)
        
    def test_argument_string_contains_two_argument_names_and_values_in_correct_order(self):
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument1", "ExampleValue1")
        arguments.add_argument("ExampleArgument2", "ExampleValue2")
        argument_string = arguments.get_arguments_string()
        pos1 = argument_string.find("ExampleArgument1")
        pos2 = argument_string.find("ExampleValue1")
        pos3 = argument_string.find("ExampleArgument2")
        pos4 = argument_string.find("ExampleValue2")
        self.assertTrue(pos1 >= 0 and pos1 < pos2 < pos3 < pos4)
        
    
class ShellCallTest(TestCase):
    '''
    Tests class ShellCall
    '''
    
    def test_shell_command_valid_with_no_arguments(self):
        call = ShellCall()
        call.set_command("ExampleCommand")
        self.assertEquals(call.get_shell_command(), "ExampleCommand")
        
    def test_shell_command_contains_command_and_arguments_in_correct_order(self):
        call = ShellCall()
        call.set_command("ExampleCommand")
        
        arguments = ArgumentList()
        arguments.add_argument("ExampleArgument", "ExampleValue")
        call.set_arguments(arguments)
        
        shell_command = call.get_shell_command()
        pos1 = shell_command.find("ExampleCommand")
        pos2 = shell_command.find(arguments.get_arguments_string())
        
        self.assertTrue(pos1 >= 0 and pos1 < pos2)
        
        
class ShellTest(TestCase):
    '''
    Tests module shell
    '''

    def test_shell_accepts_shellcall_as_parameter_and_returns_shellresult(self):
        call = ShellCall()
        call.set_command("ogr2ogr --formats")
        
        result = shell.execute(call)

        self.assertNotEqual(result.get_text(), "")
        
    def test_shell_returns_errors(self):
        call = ShellCall()
        call.set_command("{UnknownCommand}")
        
        result = shell.execute(call)

        self.assertNotEqual(result.get_error(), "")
        
        
class ShellResultTest(TestCase):
    '''
    Tests class ShellResult
    '''
    
    def test_result_strings_empty_if_initialized_with_none(self):
        shell_result = ShellResult(None, None)
        self.assertEqual(shell_result.get_text(), '')
        self.assertEqual(shell_result.get_error(), '')
        
    def test_result_strings_equal_to_input(self):
        shell_result = ShellResult('Output', 'ErrorMessage')
        self.assertEqual(shell_result.get_text(), 'Output')
        self.assertEqual(shell_result.get_error(), 'ErrorMessage')
    
