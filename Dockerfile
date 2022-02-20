#FastenThings 
FROM ubuntu:20.04

RUN apt -y update

RUN apt install -y git
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y wget
RUN apt install build-essential


RUN apt-get install -y gcc-arm-none-eabi
RUN apt-get install -y gdb-multiarch
RUN ln -s /usr/bin/gdb-multiarch /usr/bin/arm-none-eabi-gdb


RUN arm-none-eabi-gcc --version
RUN arm-none-eabi-gdb --version

##RUN python --version
RUN python3 --version

RUN gcc --version



# QEMU
# Install with manual
# https://xpack.github.io/qemu-arm/install/
# downloaded file
RUN qemu_version="2.8.0-9"
RUN qemu_path_first_part="xpack-qemu-arm-${qemu_version}"
RUN qemu_install_file="${qemu_path_first_part}-linux-x64.tar.gz"
# https://github.com/xpack-dev-tools/qemu-arm-xpack/releases/download/v2.8.0-9/xpack-qemu-arm-2.8.0-9-linux-x64.tar.gz
RUN download_full_path="https://github.com/xpack-dev-tools/qemu-arm-xpack/releases/download/v${qemu_version}/${qemu_install_file}"
RUN echo "Download: ${download_full_path}"
RUN wget $download_full_path

RUN mkdir -p opt
RUN cd opt

# E.g. tar xvf ~/Downloads/xpack-qemu-arm-2.8.0-7-linux-x64.tgz
RUN echo "Unzip: ${qemu_install_file}"
RUN tar xvf ../$qemu_install_file
# E.g. chmod -R -w xPacks/qemu-arm/2.8.0-7
#chmod -R -w $qemu_path_first_part
RUN chmod -R 777 $qemu_path_first_part
RUN qemu_bin_path="${qemu_path_first_part}/bin/qemu-system-gnuarmeclipse"
# Execute the version
RUN echo "Execute: ${qemu_bin_path}"
RUN ./$qemu_bin_path --version
RUN pwd  # Debug

RUN cd ..



# Unittest
# QEMU path is required for test
RUN export QEMU_BIN_PATH="opt/${qemu_bin_path}"


##python3 -m unittest discover

# SystemTest
##relative_qemu_bin_path="opt/${qemu_bin_path}"
##python3 -u gdb_test.py --test_file_path test/reference/FastenHomeAut --qemu_bin_path $relative_qemu_bin_path

