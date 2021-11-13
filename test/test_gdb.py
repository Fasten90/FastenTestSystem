import unittest
import os

import gdb_test


class TestReference(unittest.TestCase):
    def test_reference(self):
        import subprocess

        python_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'gdb_test.py'))
        test_file_path = os.path.dirname(__file__) + '/' + 'reference' + '/' + 'FastenHomeAut'
        args = '--test_file_path {}'.format(test_file_path)

        #subprocess.run(['python', python_file + ' ' + args])
        exec_command = 'python' + ' ' + '-u' + ' ' + python_file + ' ' + args
        #p = subprocess.Popen(exec_command, shell=True, stdout=subprocess.PIPE)
        #out, err = p.communicate()

        from subprocess import Popen, PIPE, CalledProcessError
        with Popen(exec_command, stdout=PIPE, bufsize=1, universal_newlines=True, shell=True) as p:
            for line in p.stdout:
                print(line, end='')  # process line here

        if p.returncode != 0:
            raise CalledProcessError(p.returncode, p.args)


if __name__ == '__main__':
    unittest.main()
