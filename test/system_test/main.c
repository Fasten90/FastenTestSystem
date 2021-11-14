#include <stdio.h>
#include "UnitTest.h"

int main(void);


int main(void)
{
    
    UnitTest_Start("TestModule", "main.c");
    UNITTEST_ASSERT(1, "TestValid-ErrorMessage");
    UNITTEST_ASSERT(0, "TestInvalid-ErrorMessage");
    UnitTest_End();
}
