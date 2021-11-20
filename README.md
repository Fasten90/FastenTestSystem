# FastenTestSystem

## Summmary
I started this project for my Embedded project 'FastenHomeAut'  
See the Azure pipeline for the project: [FastenHomeAut pipeline](https://dev.azure.com/FastenOrganization/Fasten90%20-%20FastenHomeAut%20pipeline/_build)


## Goals
This project has been started for automating the test execution in simple situation:  
* Embedded C project use the provided fix format UniTest functions (ASSERTs)
* Built
* Code (binary)is executed in emulator (QEMU)
* The python script will connect via gdb to the target
* Check the UnitTest execution results
* Export the result


## Useful links
* [QEMU link](https://github.com/xpack-dev-tools/qemu-arm-xpack/)
* [GDB](https://www.gnu.org/software/gdb/)


## How to Use
### C / Embedded side
* Expected: Available C project
* Needed:
  * Add the utils\UnitTest.c nad utils\UnitTest.h files in your project
    * Do not forget to include the header file:
    `#include "UnitTest.h"`
  * Call the assert functions
    * At begin of your tests:  
     `UnitTest_Start(const char *moduleName, const char *fileName);`  
     E.g. `UnitTest_Start("ModuleName", "MyFile.c");`
    * At your tests, use the assert:
     `#define UNITTEST_ASSERT(con, errorstring)`
     `UNITTEST_ASSERT(1, "ErrorString for explain why it should be OK") /* True condition expected */`
    * When the all tests are executed:
     `UnitTest_End();`
### Host / Test execution / Pipeline side
* See the 'azure-pipelines.yml' for tool installation and executions.
* Install the python, QEMU, GDB
* Execute the gdb_test.py:
  * `python3 -u gdb_test.py --test_file_path <your_built_binary> --qemu_bin_path <qemu_path>`
    * your_built_binary --> Your built binary (maybe elf file)
    * qemu_path --> PATH of your installed QEMU - Not needed if it is on PATH
    * Check the other arguments: `python gdb_test.py --help`
 * It report the executed ASSERTs

