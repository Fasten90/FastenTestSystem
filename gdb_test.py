import subprocess
import time
import re
from enum import Enum
import os
import argparse

# These threads shall be terminated
proc_qemu = None
proc_gdb = None


class TestResultType(Enum):
    DontCare = 1
    Min = 2
    Max = 3
    Equal = 4


def log_error(msg):
    print('[ERROR] ' + msg)


def log_warning(msg):
    print('[WARNING] ' + msg)


def start_qemu_test(test_elf_path, qemu_path='qemu-system-gnuarmeclipse'):
    global proc_qemu
    global proc_gdb

    qemu_machine = 'STM32F4-Discovery'

    qemu_args = '-machine {machine} -kernel {elf} -nographic -S -s'.format(
        machine=qemu_machine,
        elf=test_elf_path)

    qemu_command = '{} {}'.format(qemu_path, qemu_args)

    # Check the test file is exists or not
    if not os.path.exists(test_elf_path):
        raise Exception('Test file is not exists: {}'.format(test_elf_path))

    # Check
    if not os.path.exists(qemu_path):
        log_warning('QEMU does not exists as path: {}. It is possible if it is on the PATH'.format(qemu_path))

    try:
        #Test: qemu-system-gnuarmeclipse.exe --version
        proc_qemu_test = subprocess.Popen('qemu-system-gnuarmeclipse --version', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
        stdout = proc_qemu_test.communicate()[0]
    except Exception as ex:
        log_error('QEMU test has failed!')
        raise ex

    print('Result of QEMU test: {}'.format(stdout))

    if 'QEMU emulator version' not in str(stdout):
        raise Exception('QEMU version response was wrong!')

    # gdb test
    try:
        proc_gdb_test = subprocess.Popen('arm-none-eabi-gdb --version', shell=False, stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = proc_gdb_test.communicate()[0]
    except Exception as ex:
        log_error('GDB test has failed!')
        raise ex

    print('Result of GDB test: {}'.format(stdout))

    if 'GNU gdb' not in str(stdout):
        raise Exception('GDB version response was wrong!')

    # Start Normal phase

    # Execute QEMU
    print('Execute: {}'.format(qemu_command))
    proc_qemu = subprocess.Popen(qemu_command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait until QEMU stand up
    # TODO: Risk: This is execution time dependent
    print('Wait to start up QEMU...')
    qemu_start_up_timeout_sec = 10
    for i in range(qemu_start_up_timeout_sec):
        time.sleep(1)
    print('Continue...')

    # Note: Tested a one-by-one command, but:
    #proc = subprocess.Popen('arm-none-eabi-gdb', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Failed on a stdin error

    # GDB
    print('Start GDB')
    proc_gdb = subprocess.Popen('arm-none-eabi-gdb -x gdb_cmd', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # stdout = proc.communicate()[0]
    #print(stdout)
    gdb_proc_result = proc_gdb.stdout.readlines()
    print('proc_readline: {}'.format(gdb_proc_result))
    gdb_proc_result = ''.join(item.decode() + ' ' for item in gdb_proc_result)

    #print('proc_qemu.stdout'.format(proc_qemu.stdout))
    # Cannot readlines() for qemu process, because it is running yet
    # TODO: Patient kill?
    proc_qemu.terminate()

    # Check GDB result
    # Example content: $1 = 34\r\n', b'$2 = 0\
    value_result_list = []
    regex_result = re.findall(r'\$(\d+) \= (\d+)', gdb_proc_result)
    for re_found in regex_result:
        # Result is tuple, e.g. (1, 34)
        val_id = re_found[0]
        val_value = re_found[1]
        value_result_list.append((val_id, val_value))
        print('Val: {} = {}'.format(val_id, val_value))

    return value_result_list


def check_results(value_result_list):
    expected_results = [
        (1, 34, 'Successful', TestResultType.Min),
        (2, 0,  'Failed',     TestResultType.Equal)]

    for index, result_item in enumerate(value_result_list):
        # Id
        assert int(result_item[0]) == expected_results[index][0]

        # TODO: Generalize

        expected_val = expected_results[index][1]
        test_name = expected_results[index][2]
        test_res_type = expected_results[index][3]
        test_return_val = int(result_item[1])
        if test_res_type == TestResultType.Equal:
            assert test_return_val == expected_val
        elif test_res_type == TestResultType.Min:
            assert test_return_val >= expected_val
        elif test_res_type == TestResultType.Max:
            assert test_return_val <= expected_val
        elif test_res_type == TestResultType.DontCare:
            pass
        else:
            raise Exception('Unhandled TestResultType')
        print('Result of "{}" test was okay. Expected: {}, test result: {}, condition type: {}'.format(
            test_name, expected_val, test_return_val, str(test_res_type)))


def main():
    parser = argparse.ArgumentParser(description='FastenTestSystem')
    parser.add_argument('--test_file_path', required=True,
                        help='path for test file (E.g. .elf file)')
    parser.add_argument('--qemu_bin_path', required=False,
                        default='qemu-system-gnuarmeclipse',
                        help='path for QEMU')
    args = parser.parse_args()

    # 1. Phase: Test execution
    try:
        value_result_list = start_qemu_test(test_elf_path=args.test_file_path,
                                            qemu_path=args.qemu_bin_path)
    except Exception as ex:
        global proc_qemu
        global proc_gdb
        log_error('Exception: {}'.format(ex))
        if proc_qemu:
            proc_qemu.terminate()
        if proc_gdb:
            proc_gdb.terminate()
        raise ex
    # 2. Phase: Test result check
    check_results(value_result_list)


if __name__ == '__main__':
    main()
