// filepath: sbrk.h
/**
 * POSIX Syscall Header: sbrk
 * Module: sbrk - Increment Program Break
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef SBRK_H
#define SBRK_H

// Type definitions
typedef long intptr_t;

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
void* sbrk_impl(intptr_t increment);
int sbrk_test(void);

// Module information API
const char* sbrk_get_description(void);
const char* sbrk_get_arch(void);
int sbrk_get_dependencies(char** deps, int max_deps);

// POSIX sbrk constants and definitions
#define SBRK_FAILURE    ((void*)-1)

// Error conditions (using standard errno values)
#define SBRK_ENOMEM     12    // Out of memory

#ifdef __cplusplus
}
#endif

#endif // SBRK_H
