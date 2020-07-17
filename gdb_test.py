import subprocess
import time
import re

# QEMU starting
test_elf_path = r'd:\VG\Projects\AtollicWorkspace\FastenNodeF4Discovery\Debug\FastenNodeF4Discovery.elf'

qemu_path = r'c:\Programs\Engineer\xpack-qemu-arm-2.8.0-8-win32-x64\xPack\QEMU ARM\2.8.0-8\bin\qemu-system-gnuarmeclipse.exe'

qemu_machine = 'STM32F4-Discovery'

qemu_args = '-machine {machine} -kernel {elf} -nographic -S -s'.format(
    machine=qemu_machine,
    elf=test_elf_path)

qemu_command = '{} {}'.format(qemu_path, qemu_args)

proc_qemu = None
proc_gdb = None


def start_qemu_test():
    global proc_qemu
    global proc_gdb

    try:
        # Start:
        #Test: qemu-system-gnuarmeclipse.exe --version
        proc_qemu_test = subprocess.Popen('qemu-system-gnuarmeclipse.exe --version', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        stdout = proc_qemu_test.communicate()[0]
        print('Result of QEMU test: {}'.format(stdout))


        print('Execute: {}'.format(qemu_command))

        proc_qemu = subprocess.Popen(qemu_command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait until QEMU stand up
        print('Wait to start up QEMU')
        time.sleep(10)


        #proc = subprocess.Popen('arm-none-eabi-gdb', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Failed on a stdin error

        #proc = subprocess.Popen(['arm-none-eabi-gdb', '-s', '-v', 'gdb_cmd.gdb.txt'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        proc_gdb = subprocess.Popen('arm-none-eabi-gdb -x gdb_cmd', shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


        #stdout = proc.communicate()[0]
        #print(stdout)
        gdb_proc_result = proc_gdb.stdout.readlines()
        print('proc_readline: {}'.format(gdb_proc_result))
        gdb_proc_result = ''.join(item.decode() + ' ' for item in gdb_proc_result)


        #print('proc_qemu.stdout'.format(proc_qemu.stdout))
        # Cannot readlines() for qemu process, because it is running yet

        proc_qemu.terminate()


        # Check proc.stdout

        # Example content: $1 = 34\r\n', b'$2 = 0\
        regex_result = re.findall(r'\$(\d+) \= (\d+)', gdb_proc_result)
        for re_found in regex_result:
            # Result is tuple, e.g. (1, 34)
            val_id = re_found[0]
            val_value = re_found[1]
            print('Val: {} = {}'.format(val_id, val_value))

    except Exception as ex:
        print('Exception: {}'.format(ex))
        if proc_qemu:
            proc_qemu.terminate()
        if proc_gdb:
            proc_gdb.terminate()


def main():
    start_qemu_test()


if __name__ == '__main__':
    main()
