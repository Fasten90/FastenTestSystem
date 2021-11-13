import unittest
import os

import gdb_test


class TestReference(unittest.TestCase):
    def test_reference_unittest_files(self):
        import subprocess

        # These commands are refers to util and test files
        includes = '-I utils -I test/system_test'
        arguments = '-D CONFIG_MODULE_UNITTEST_ENABLE=1'
        #exec_commands = ['gcc' + ' ' + includes + ' ' + arguments + ' ' + '-c utils/UnitTest.c -o unittest.o',
        #                'gcc' + ' ' + includes + ' ' + arguments + ' ' + 'test/system_test/main.c -o main.o',
        #                'gcc' + ' ' + 'unittest.o' + ' ' + 'main.o']
        exec_commands = ['gcc' + ' ' + includes + ' ' + arguments + ' ' + '-c utils/UnitTest.c test/system_test/main.c',
                         './main.o']

        from subprocess import Popen, PIPE, CalledProcessError

        for cmd in exec_commands:
            with Popen(cmd, stdout=PIPE, bufsize=1, universal_newlines=True) as p:
                for line in p.stdout:
                    print(line, end='')  # process line here

            if p.returncode != 0:
                raise CalledProcessError(p.returncode, p.args)


if __name__ == '__main__':
    unittest.main()
