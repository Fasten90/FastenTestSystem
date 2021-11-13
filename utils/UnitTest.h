/*
 *    UnitTest.h
 *    Created on:   2016-11-24
 *    Author:       Vizi Gabor
 *    E-mail:       vizi.gabor90@gmail.com
 *    Function:     UnitTest module
 *    Target:       STM32Fx
 */

#ifndef UNITTEST_H_
#define UNITTEST_H_


/* USERT INCLUDES SHOULD BE HERE */
#include "GenericTypeDefs.h"


/*------------------------------------------------------------------------------
 *  Macros
 *----------------------------------------------------------------------------*/

/**
 * (1)    SW will pause, when a UnitTest result be failed
 * (0)    SW will continue the run (and printed the condition)
 */
#ifndef UNITTEST_PAUSE_WHEN_ERROR
    #define UNITTEST_PAUSE_WHEN_ERROR                    (0)
#endif

/**
 * (1)    Print assert message (very useful for finding bug)
 * (0)    Do not print assert message
 */
#ifndef UNITTEST_PRINT_ASSERT
    #define UNITTEST_PRINT_ASSERT                        (1)
#endif

/* if con == true, is valid */
#define UNITTEST_ASSERT(con, errorstring)            UnitTest_CheckResult(con, #con, errorstring, __LINE__)



/*------------------------------------------------------------------------------
 *  Global function declarations
 *----------------------------------------------------------------------------*/

void UnitTest_Start(const char *moduleName, const char *fileName);
void UnitTest_CheckResult(bool isValid, const char *conString, const char *errorString, uint32_t line);
uint32_t UnitTest_End(void);



#endif /* UNITTEST_H_ */
