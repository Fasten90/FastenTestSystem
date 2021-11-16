import subprocess
import time
import re
from enum import Enum
import os
import argparse
from sys import platform
import csv


# These threads shall be terminated
proc_qemu = None
proc_gdb = None

# TODO: Handle it by arg?
DEBUG = False

# TODO: Add comments to dependency of TestSystem - C code
gdb_cmd_template = \
"""file <test_file_path>
target remote localhost:1234
#load <test_file_path>
# ASSERT breakpoint
break UnitTest_CheckResult
# UnitTest finished breakpoint
break UnitTest_Finished
continue
set $successful = 0
set $failed = 0
set $file = "Unknown"
while(1)
    p UnitTest_Finished_flag
    if $
        # Finish Unittest execution
        print "Finished!"
        printf "Successful: %d, failed: %d", $successful, $failed
        #if $failed
        #    print "[error] There was failed test assert!"
        #end
        detach
        quit
    else
        p UnitTest_FileName
        set $file = $
        p isValid
        if $
            set $successful = $successful + 1 
            print "Valid test assert"
            continue   
        else
            set $failed = $failed + 1
            print "Invalid test assert"
            print "Frame"
            frame
            print "Backtrace"
            backtrace
            continue
        end
    end
end

#backtrace
#frame
#p 'UnitTest.c'::UnitTest_ValidCnt
#p 'UnitTest.c'::UnitTest_InvalidCnt
#detach
#quit
"""


class TestResultType(Enum):
    DontCare = 1
    Min = 2
    Max = 3
    Equal = 4


def log_error(msg):
    print('[ERROR] ' + msg)


def log_warning(msg):
    print('[WARNING] ' + msg)


def update_gdb_cmd(test_elf_path):
    gdb_cmd_file_path = 'gdb_cmd'

    # Remove
    if os.path.exists(gdb_cmd_file_path):
        os.remove(gdb_cmd_file_path)
        print('"{}" file has removed'.format(gdb_cmd_file_path))

    # Replace the target string
    # TODO: Hardcoded TestSystem
    gdb_cmd_new_content = gdb_cmd_template.replace('<test_file_path>', test_elf_path)

    # Write the file out again
    with open(gdb_cmd_file_path, 'w') as file:
        file.write(gdb_cmd_new_content)


def restore_gdb_cmd(test_elf_path):
    gdb_cmd_file_path = 'gdb_cmd'
    # Read in the file
    with open(gdb_cmd_file_path, 'r') as file:
        gdb_cmd_content = file.read()

    # Replace the target string
    # TODO: Hardcoded TestSystem
    gdb_cmd_content = gdb_cmd_content.replace(test_elf_path, '<test_file_path>')

    # Write the file out again
    with open(gdb_cmd_file_path, 'w') as file:
        file.write(gdb_cmd_content)


def start_qemu_test(test_elf_path, qemu_path='qemu-system-gnuarmeclipse'):
    global proc_qemu
    global proc_gdb

    print('Given arguments:\n'
          '  test_elf_path = {}\n'
          '  qemu_path = {}'.format(
            test_elf_path, qemu_path))

    qemu_machine = 'STM32F4-Discovery'

    qemu_args = '-machine {machine} -kernel {elf} -nographic -S -s'.format(
        machine=qemu_machine,
        elf=test_elf_path)

    if platform == 'linux' or platform == 'linux2':
        # linux
        qemu_path = './{bin_path}'.format(bin_path=qemu_path)
    elif platform == 'darwin':
        # OS X
        raise Exception('OS X not supported yet')
    elif platform == 'win32':
        # Do nothing with the command
        pass

    qemu_command = '{} {}'.format(qemu_path, qemu_args)

    # Check the test file is exists or not
    if not os.path.exists(test_elf_path):
        raise Exception('Test file is not exists: {}'.format(test_elf_path))
    else:
        print('Test file seems exists')

    # Check
    if not os.path.exists(qemu_path):
        log_warning('QEMU does not exists as path: {}. It is possible if it is on the PATH'.format(qemu_path))
    else:
        print('QEMU executable file seems exists')

    try:
        #Test: qemu-system-gnuarmeclipse.exe --version
        qemu_test_cmd = '{bin} --version'.format(bin=qemu_path)
        print('Test: {}'.format(qemu_test_cmd))
        proc_qemu_test = subprocess.Popen(qemu_test_cmd,
                                          shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
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
        proc_gdb_test = subprocess.Popen('arm-none-eabi-gdb --version',
                                         shell=True, stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = proc_gdb_test.communicate()[0]
    except Exception as ex:
        log_error('GDB test has failed!')
        raise ex

    print('Result of GDB test: {}'.format(stdout))

    if 'GNU gdb' not in str(stdout):
        raise Exception('GDB version response was wrong: {}'.format(stdout))

    # Start Normal phase

    # Execute QEMU
    # E.g. qemu-system-gnuarmeclipse.exe -machine STM32F4-Discovery -kernel FastenNodeF4Discovery.elf -nographic -S -s
    print('Execute: "{}"'.format(qemu_command))
    proc_qemu = subprocess.Popen(qemu_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    # Update gdb_cmd
    print('Update gdb_cmd')
    update_gdb_cmd(test_elf_path)

    # GDB
    print('Start GDB')
    proc_gdb = subprocess.Popen('arm-none-eabi-gdb -x gdb_cmd', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # stdout = proc.communicate()[0]
    #print(stdout)
    print('GDB execution result: ')
    gdb_proc_result = ""
    while True:
        line = proc_gdb.stdout.readline()
        if line:
            try:
                line = line.decode('ISO-8859-1')
            except UnicodeDecodeError as ex:
                log_error('Exception: {}'.format(str(ex)))
                line = str(line)
            gdb_proc_result += line
            print(line.strip())
        else:
            break

    #print('GDB process result: {}'.format(gdb_proc_result))
    #gdb_proc_result = ''.join(item.decode() + ' ' for item in gdb_proc_result)

    print('GDB finished')

    #print('proc_qemu.stdout'.format(proc_qemu.stdout))
    # Cannot readlines() for qemu process, because it is running yet
    print('Close QEMU')
    # 1. Try with 'quit' command
    qemu_output = proc_qemu.communicate(input=b'quit\n')[0]
    print('QEMU output result: "{}"'.format(qemu_output.decode()))
    time.sleep(2)
    # 2. Try to kill if it is exists yet
    if proc_qemu and proc_qemu.returncode is None:
            proc_qemu.terminate()
            time.sleep(1)
            if proc_qemu and proc_qemu.returncode is None:
                proc_qemu.kill()
    print('QEMU result code: "{}"'.format(proc_qemu.returncode))

    # TODO: Save to a log file
    # TODO: Move to another file/class the parsing test execution data
    # Check GDB result
    print('Collect GDB test results')
    # Example content: $1 = 34\r\n', b'$2 = 0\
    value_result_list = []
    # Note: The collector regex expression contains System Unit-test dependency (e.g. UnitTest assert arguments)
    # https://regex101.com/r/Abm3Zm/7
    regex_pattern = re.compile(r'Breakpoint \d, .* \(isValid\=\d .*\,[\r\n]+ *conString\=0x[\d\w]+ \"(?P<assert_string>.*)\"\,([\r\n]+| )errorString\=0x[\d\w]+ \"(?P<error_string>.*)\"\,([\r\n]+| )*line\=(?P<line>\d+)\)[\r\n]* *at .*[\r\n]+(\d+.*[\r\n]+)?\$\d+.*[\r\n]+\$\d+ \= 0x[a-f0-9]+ \"(?P<file_path>.*)\"[\r\n]+\$\d+.*[\r\n]+\$\d+ \= \"(?P<assert_result>.*)\"', re.MULTILINE)

    for re_found in regex_pattern.finditer(gdb_proc_result):
        if DEBUG:
            print(m.groupdict())
        re_found_dict = re_found.groupdict()
        unit_test_dict = {
            'assert_string': re_found_dict['assert_string'],
            'line': re_found_dict['line'],
            'assert_result': re_found_dict['assert_result'],
            'error_string': re_found_dict['error_string'],
            'file_path': re_found_dict['file_path'],
        }
        value_result_list.append(unit_test_dict)

    found_test_assert_regex_count = len(value_result_list)
    print('Found Test assert results: {}'.format(found_test_assert_regex_count))

    # Cross-check:
    # Note: GDB command dependency
    # E.g. "Successful: 573, failed: 0"
    summary_result = re.search(r'Successful: (\d+), failed: (\d+)', gdb_proc_result)
    res_all_successful = int(summary_result[1])
    res_all_failed = int(summary_result[2])
    res_all_count = res_all_successful + res_all_failed

    print('Found test_assert: {}, GDB counts: {} : It is: {}'.format(
        found_test_assert_regex_count,
        res_all_count,
        'OK' if found_test_assert_regex_count == res_all_count else 'Wrong'
    ))

    if DEBUG:
        for item in value_result_list:
            print(''.join([' ' + dictionary_elem for dictionary_elem in item.items()]))

    # Finish / Clean
    restore_gdb_cmd(test_elf_path)

    return value_result_list


def export_to_csv(export_filename, result_list):
    # Create CSV
    with open(export_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['file_path', 'line', 'assert_string', 'assert_result', 'error_string']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in result_list:
            writer.writerow(row)
        print('Exported to {}'.format(export_filename))


# TODO: Update: FileName, LineNumber
def check_results(value_result_list):

    #expected_results = [
    #    (1, 10, 'Successful', TestResultType.Min),  # TODO: Read it from a config
    #    (2, 0,  'Failed',     TestResultType.Equal)]

    for index, result_item in enumerate(value_result_list):
        # Id
        # TODO: Maybe it was planned to be a comparation to a fix config/result list.
        #assert int(result_item[0]) == expected_results[index][0]

        # TODO: Generalize

        #expected_val = expected_results[index][1]
        #test_name = expected_results[index][2]
        #test_res_type = expected_results[index][3]
        #test_return_val = int(result_item[1])
        #if test_res_type == TestResultType.Equal:
        #    assert test_return_val == expected_val
        #elif test_res_type == TestResultType.Min:
        #    assert test_return_val >= expected_val
        #elif test_res_type == TestResultType.Max:
        #    assert test_return_val <= expected_val
        #elif test_res_type == TestResultType.DontCare:
        #    pass
        #else:
        #    raise Exception('Unhandled TestResultType')
        assert 'Valid' in result_item['assert_result']

        print('Result of "{}" test was okay. At {}:{}, test result: {}, error message: {}'.format(
            result_item['assert_string'], result_item['file_path'], result_item['line'], result_item['assert_result'], result_item['error_string']))


def main():
    parser = argparse.ArgumentParser(description='FastenTestSystem')
    parser.add_argument('--test_file_path', required=True,
                        help='path for test file (E.g. .elf file)')
    parser.add_argument('--qemu_bin_path', required=False,
                        default='qemu-system-gnuarmeclipse',
                        help='path for QEMU')
    parser.add_argument('--export-csv', required=False,
                        default='TestResults.csv',
                        help='path for exported CSV')
    args = parser.parse_args()

    # TODO: Add verbose/debug

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
    # 3. Phase: Export
    export_to_csv(args.export_csv, value_result_list)


if __name__ == '__main__':
    main()
