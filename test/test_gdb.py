import unittest
import os
import sys

import subprocess

from sys import platform

import gdb_test


def get_python_by_platform():
    python_bin = 'python'
    if platform == 'linux' or platform == 'linux2':
        # linux
        python_bin = 'python3'
    elif platform == 'darwin':
        # OS X
        python_bin = 'python3'
    elif platform == 'win32':
        # Do nothing with the command
        python_bin = 'python'
    return python_bin


class TestReference(unittest.TestCase):
    def test_reference(self):
        import subprocess

        python_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'gdb_test.py'))
        test_file_path = os.path.dirname(__file__) + '/' + 'reference' + '/' + 'FastenHomeAut'
        args = '--test_file_path {}'.format(test_file_path)

        # If pipeline
        is_pipeline = os.getenv('PIPELINE_WORKSPACE')
        if is_pipeline:
            QEMU_BIN_PATH = os.getenv('QEMU_BIN_PATH')
            args += ' ' + '--qemu_bin_path=./{qemu_bin_path}'.format(qemu_bin_path=QEMU_BIN_PATH)

        python = get_python_by_platform()
        #subprocess.run(['python', python_file + ' ' + args])
        exec_command = [sys.executable, python_file, args]
        #p = subprocess.Popen(exec_command, shell=True, stdout=subprocess.PIPE)
        #out, err = p.communicate()

        #from subprocess import Popen, PIPE, CalledProcessError
        #with Popen(exec_command, stdout=PIPE, bufsize=1, universal_newlines=True, shell=True) as p:
        #    for line in p.stdout:
        #        print(line, end='')  # process line here
        print('In the ideal world we execute this: {}'.format(exec_command))
        
        test_execution = subprocess.run(exec_command, capture_output=True) # 'shell=True' maybe not necessary
        # Removed 'stdout=True, ' due 'ValueError: stdout and stderr arguments may not be used with capture_output.' error
        
        print('Execution result: {}'.format(test_execution))
        print(test_execution.stdout)
        print(test_execution.stderr)
        
        test_execution.check_returncode()

        print('In the ideal world that is executed: {}'.format(exec_command))


if __name__ == '__main__':
    unittest.main()
