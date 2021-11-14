/*
 *    GenericTypeDefs.h
 *    Created on:   2017-02-27
 *    Author:       Vizi Gabor
 *    E-mail:       vizi.gabor90@gmail.com
 *    Function:     Generic typedefs
 *    Target:       STM32Fx
 */

#ifndef GENERICTYPEDEFS_H_
#define GENERICTYPEDEFS_H_



/*------------------------------------------------------------------------------
 *  Includes
 *----------------------------------------------------------------------------*/

/* bool type */
#if (CONFIG_COMPILER_USE_DEFAULT_BOOL == 1)
#include <stdbool.h>
#endif /* CONFIG_COMPILER_USE_DEFAULT_BOOL */

/* uint32_t type */
#include <stdint.h>

/* size_t, NULL */
#include <stddef.h>



/*------------------------------------------------------------------------------
 *  Macros
 *----------------------------------------------------------------------------*/

#define BOOL_MAX    (1)


/* This defines are defined in "stdint.h" file */
/* TODO: Delete if not need */
/*
#define UINT8_MAX     (0xFF)
#define INT8_MAX      (0x7F)
#define UINT16_MAX    (0xFFFF)
#define INT16_MAX     (0x7FFF)
#define UINT32_MAX    (0xFFFFFFFF)
#define INT32_MAX     (0x7FFFFFFF)
*/



/*------------------------------------------------------------------------------
 *  Type definitions
 *----------------------------------------------------------------------------*/


#if (CONFIG_COMPILER_USE_DEFAULT_BOOL == 0)
/**
 * This solution will help in "small storage" for bool
 */
typedef uint8_t bool;

#define true  1
#define false 0
#endif /* CONFIG_COMPILER_USE_DEFAULT_BOOL */


///< Integer typedefs
typedef unsigned char               uint8_t;
typedef signed char                 int8_t;
typedef short unsigned int          uint16_t;
typedef short signed int            int16_t;
#ifndef __GNUC__
typedef unsigned int                uint32_t;
typedef signed int                  int32_t;
#endif


///< Other typedefs
typedef char                        char_t;
typedef float                       float32_t;
typedef bool                        bool_t;


///< New bool type
typedef enum
{
    Bool_Uninitialized,
    Bool_False,
    Bool_True
} BoolData_t;


#include <stdio.h>
#define uprintf(...)                            printf(__VA_ARGS__)



#endif /* GENERICTYPEDEFS_H_ */
