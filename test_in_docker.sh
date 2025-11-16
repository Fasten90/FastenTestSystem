# Test in docker

git clone https://github.com/Fasten90/FastenTestSystem.git

cd FastenTestSystem

# TODO: Reset it to develop
git checkout test_debug_test_command_failing

python3 -m pip install update
python3 -m pip install -r requirements.txt

# UnitTest
python3 -m unittest discover

# SystemTest
relative_qemu_bin_path="${qemu_bin_path}"
python3 -u gdb_test.py --test_file_path test/reference/FastenHomeAut --qemu_bin_path $relative_qemu_bin_path

