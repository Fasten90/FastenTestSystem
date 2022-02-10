/*
 *    UnitTest.c
 *    Created on:   2016-11-24
 *    Author:       Vizi Gabor
 *    E-mail:       vizi.gabor90@gmail.com
 *    Function:     UnitTest module
 *    Target:       STM32Fx
 */



/*------------------------------------------------------------------------------
 *  Header files
 *----------------------------------------------------------------------------*/

/* USERT INCLUDES SHOULD BE HERE */
#include "UnitTest.h"


#ifdef CONFIG_MODULE_UNITTEST_ENABLE



/*------------------------------------------------------------------------------
 *  Local variables
 *----------------------------------------------------------------------------*/

static uint16_t UnitTest_ValidCnt = 0;
static uint16_t UnitTest_InvalidCnt = 0;

static const char *UnitTest_FileName = NULL;



/*------------------------------------------------------------------------------
 *  Functions
 *----------------------------------------------------------------------------*/


/**
 * @brief       Start unit test
 */
void UnitTest_Start(const char *moduleName, const char *fileName)
{
    uprintf("\r\n"
            "Start %s module unit test\r\n"
            "File: \"%s\"\r\n"
            "\r\n",
            moduleName, fileName);
    UnitTest_ValidCnt = 0;
    UnitTest_InvalidCnt = 0;
    UnitTest_FileName = fileName;
}



/**
 * @brief       Check unit test result (~assert) (+ condition string)
 */
void UnitTest_CheckResult(bool isValid, const char *conString, const char *errorString, uint32_t line)
{
    if (isValid)
    {
        /* Valid */
        UnitTest_ValidCnt++;

#if (UNITTEST_PRINT_ASSERT == 1)
        /* Successful ASSERT, but need print */
        uprintf("Assert OK: %s:%d - \"%s\" - \"%s\"\r\n",
                UnitTest_FileName, line,
                conString,
                errorString);
#endif
    }
    else
    {
        /* Invalid */
        UnitTest_InvalidCnt++;

#if (UNITTEST_PAUSE_WHEN_ERROR == 1)
        UNUSED_ARGUMENT(conString);
        UNUSED_ARGUMENT(errorString);
        UNUSED_ARGUMENT(line);
        DEBUG_BREAKPOINT();
#else

    #ifdef CONFIG_MODULE_COLOREDMESSAGE_ENABLE
        char coloredMsg[ESCAPE_FORMAT_STANDARD_STRING_MAX_LENGTH * 2] = { 0 };
        ColoredMessage_SendTextColor(coloredMsg, Color_Black);
        ColoredMessage_SendBackgroundColor(coloredMsg, Color_Red);
        DebugUart_SendMessage(coloredMsg);
    #endif

        /* Failed condition + message will printed */
        uprintf("\r\n"
                "Error in \"%s\" at %d. line.\r\n"
                "Condition: \"%s\"\r\n"
                "Case: \"%s\"\r\n"
                "\r\n",
                UnitTest_FileName, line,
                conString,
                errorString);

    #ifdef CONFIG_MODULE_COLOREDMESSAGE_ENABLE
        /* Set default color */
        coloredMsg[0] = '\0';    /* Clear colorMsg */

        ColoredMessage_SendTextColor(coloredMsg, COLOREDMESSAGE_STANDARD_TEXT_COLOR);
        ColoredMessage_SendBackgroundColor(coloredMsg, COLOREDMESSAGE_STANDARD_BACKGROUND_COLOR);
        DebugUart_SendMessage(coloredMsg);
    #endif
#endif
    }
}



/**
 * @brief       Finish unit test
 * @retval      0 if successfully run all tests
 */
uint32_t UnitTest_End(void)
{
    uprintf("\r\n"
            "In \"%s\" file run unit test:\r\n"
            "Successful: %d\r\n"
            "Error: %d\r\n"
            "\r\n",
            UnitTest_FileName,
            UnitTest_ValidCnt,
            UnitTest_InvalidCnt);

#ifdef CONFIG_MODULE_COLOREDMESSAGE_ENABLE
    char coloredMsg[ESCAPE_FORMAT_STANDARD_STRING_MAX_LENGTH * 2 + 40] = { 0 };
#endif

    if (UnitTest_InvalidCnt)
    {
#ifdef CONFIG_MODULE_COLOREDMESSAGE_ENABLE
        ColoredMessage_SendErrorMsg(coloredMsg, "UnitTest run failed\r\n");
        DebugUart_SendMessage(coloredMsg);
        /* Send sound */
        DebugUart_SendChar(TERMINAL_KEY_BELL);
#else
        uprintf("UnitTest run failed\r\n");
#endif
    }
    else
    {
#ifdef CONFIG_MODULE_COLOREDMESSAGE_ENABLE
        ColoredMessage_SendMsg(coloredMsg, "UnitTest run successfully\r\n", Color_Green);
        DebugUart_SendMessage(coloredMsg);
#else
        uprintf("UnitTest run successfully\r\n");
#endif
    }

    return UnitTest_InvalidCnt;
}



#endif    /* #ifdef CONFIG_MODULE_UNITTEST_ENABLE */
