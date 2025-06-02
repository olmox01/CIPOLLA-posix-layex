// filepath: munmap.h
/**
 * POSIX Syscall Header: munmap
 * Module: munmap - Unmap Memory
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef MUNMAP_H
#define MUNMAP_H

// Type definitions
typedef unsigned long size_t;

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
int munmap_impl(void *addr, size_t length);
int munmap_test(void);

// Module information API
const char* munmap_get_description(void);
const char* munmap_get_arch(void);
int munmap_get_dependencies(char** deps, int max_deps);

// POSIX munmap constants and definitions
#define MUNMAP_SUCCESS     0
#define MUNMAP_FAILURE    -1

// Error conditions
#define MUNMAP_EINVAL     22    // Invalid argument

#ifdef __cplusplus
}
#endif

#endif // MUNMAP_H
