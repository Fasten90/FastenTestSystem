# FastenTestSystem

## Goals
This project has been started for automating the test execution in simple situation:  
* Code (binary)is executed in emulator (QEMU)
* The python script will connect via gdb to the target
* Check the UnitTest execution results


## Useful links
* [QEMU link](https://github.com/xpack-dev-tools/qemu-arm-xpack/)
* [GDB](https://www.gnu.org/software/gdb/)


## Note
I started this project for my Embedded project 'FastenHomeAut'  
See the Azure pipeline for the project: [FastenHomeAut pipeline](https://dev.azure.com/FastenOrganization/Fasten90%20-%20FastenHomeAut%20pipeline/_build)


## TODO
* Write UnitTests
* Execute UnitTests at CI
* Draw design
* Issue: QEMU sometimes has stuck. Kill the process if there is issue
* Improvement: Expected TestResults shall moved to a config file
  * E.g. JSON file?
* Improvement: gdb_cmd (GDB command list file) shall be generated from template
* Improvement: Change optional the QEMU or GDB execution:
  * E.g. What if the User want to start the QEMU, and the script shall connect to that
  * This require lot of arguments, and only useful for some local development situations
* Improvement: Move 'machine' to argument, now it is hardcoded
* Improvement: Next level in test execution: Execute one-by-one the tests and check result
* Improvement (Extremely high level, near to the SAFETY - ASIL-D requirements): Check the assert messages, send communication informations (E.g. ASSERT message, measurement time, etc)
