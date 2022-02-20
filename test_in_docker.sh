# Test in docker

git clone https://github.com/Fasten90/FastenTestSystem.git

cd FastenTestSystem

python3 -m pip install update
python3 -m pip install -r requirements.txt

# UnitTest
python3 -m unittest discover

# SystemTest
relative_qemu_bin_path="opt/${qemu_bin_path}"
python3 -u gdb_test.py --test_file_path test/reference/FastenHomeAut --qemu_bin_path $relative_qemu_bin_path


