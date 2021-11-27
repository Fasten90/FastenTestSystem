import unittest
import os

import gdb_test


class TestCheckTestExecutionResult(unittest.TestCase):

    def test_check_test_execution_result_correct(self):
        # See example log in reference.log file
        test_gdb_proc_result = """
Breakpoint 1, UnitTest_CheckResult (isValid=1 '\\001', 
    conString=0x8012080 \"test condition\", 
    errorString=0x8012044 \"Test error message\", line=2587)
    at ..\\..\\FastenHomeAut\\Src\\Common\\Helper\\UnitTest.c:66
66	in /MyProject/TestFile.c
$1 = 0 '\\000'
$2 = 0x8011304 \"/MyProject/TestFile.c\"
$3 = 1 '\\001'
$4 = \"Valid test assert\"


Breakpoint 2, UnitTest_Finished () at ..\\..\\FastenHomeAut\\Src\\main.c:273
273	    UnitTest_Finished_flag = true;
$1720 = 1 '\\001'
$1721 = \"Finished!\"
Successful: 1, failed: 0[Inferior 1 (Remote target) detached]

        """
        value_result_list = gdb_test.check_test_execution_result(test_gdb_proc_result)
        expected_result = {
            'assert_string': 'test condition',
            'line': '2587',
            'assert_result': 'Valid test assert',
            'error_string': 'Test error message',
            'file_path': 'TestFile.c'
        }
        assert value_result_list
        self.assertDictEqual(expected_result, value_result_list[0])


    def test_check_test_execution_result_there_is_no_test_exception(self):
        # See example log in reference.log file
        test_gdb_proc_result = """
            MISSING TEST ASSERTS. OHH NOOOOO

            MISSED END OF UNITTEST
        """
        with self.assertRaises(Exception) as context:
            value_result_list = gdb_test.check_test_execution_result(test_gdb_proc_result)

        print(context.exception)
        self.assertIn('UnitTest assert', str(context.exception))


    def test_check_test_execution_result_missed_end_exception(self):
        # See example log in reference.log file
        test_gdb_proc_result = """
Breakpoint 1, UnitTest_CheckResult (isValid=1 '\\001', 
    conString=0x8012080 \"test condition\", 
    errorString=0x8012044 \"Test error message\", line=2587)
    at ..\\..\\FastenHomeAut\\Src\\Common\\Helper\\UnitTest.c:66
66	in /MyProject/TestFile.c
$1 = 0 '\\000'
$2 = 0x8011304 \"/MyProject/TestFile.c\"
$3 = 1 '\\001'
$4 = \"Valid test assert\"


MISSED END OF UNITTEST
        """
        with self.assertRaises(Exception) as context:
            value_result_list = gdb_test.check_test_execution_result(test_gdb_proc_result)
        print(context.exception)
        self.assertIn('UnitTest_End', str(context.exception))


if __name__ == '__main__':
    unittest.main()
