// filepath: brk.h
/**
 * POSIX Syscall Header: brk
 * Module: brk - Program Break Control
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef BRK_H
#define BRK_H

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
int brk_impl(void *addr);
int brk_test(void);

// Module information API
const char* brk_get_description(void);
const char* brk_get_arch(void);
int brk_get_dependencies(char** deps, int max_deps);

// POSIX brk constants and definitions
#define BRK_SUCCESS     0
#define BRK_FAILURE    -1

// Error conditions (using standard errno values)
#define BRK_EINVAL     22    // Invalid address
#define BRK_ENOMEM     12    // Out of memory

#ifdef __cplusplus
}
#endif

#endif // BRK_H
