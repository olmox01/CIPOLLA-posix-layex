// filepath: msync.h
/**
 * POSIX Syscall Header: msync
 * Module: msync - Memory Synchronization
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef MSYNC_H
#define MSYNC_H

// Type definitions
typedef unsigned long size_t;

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
int msync_impl(void *addr, size_t length, int flags);
int msync_test(void);

// Module information API
const char* msync_get_description(void);
const char* msync_get_arch(void);
int msync_get_dependencies(char** deps, int max_deps);

// POSIX msync constants and definitions
#define MSYNC_SUCCESS     0
#define MSYNC_FAILURE    -1

// Synchronization flags (POSIX standard)
#define MS_ASYNC          1    // Asynchronous writes
#define MS_SYNC           4    // Synchronous writes
#define MS_INVALIDATE     2    // Invalidate mappings

// Error conditions
#define MSYNC_EINVAL     22    // Invalid argument
#define MSYNC_ENOMEM     12    // Not enough memory
#define MSYNC_EIO         5    // I/O error

#ifdef __cplusplus
}
#endif

#endif // MSYNC_H
