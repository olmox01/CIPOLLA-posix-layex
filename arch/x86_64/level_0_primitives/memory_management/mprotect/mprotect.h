// filepath: mprotect.h
/**
 * POSIX Syscall Header: mprotect
 * Module: mprotect - Memory Protection
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef MPROTECT_H
#define MPROTECT_H

// Type definitions
typedef unsigned long size_t;

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
int mprotect_impl(void *addr, size_t len, int prot);
int mprotect_test(void);

// Module information API
const char* mprotect_get_description(void);
const char* mprotect_get_arch(void);
int mprotect_get_dependencies(char** deps, int max_deps);

// POSIX mprotect constants and definitions
#define MPROTECT_SUCCESS      0
#define MPROTECT_FAILURE     -1

// Memory protection flags (POSIX standard)
#define PROT_NONE     0x0    // No permissions
#define PROT_READ     0x1    // Read permission
#define PROT_WRITE    0x2    // Write permission
#define PROT_EXEC     0x4    // Execute permission

// Combined permissions (common combinations)
#define PROT_READ_WRITE    (PROT_READ | PROT_WRITE)
#define PROT_READ_EXEC     (PROT_READ | PROT_EXEC)
#define PROT_ALL           (PROT_READ | PROT_WRITE | PROT_EXEC)

// Error conditions
#define MPROTECT_EINVAL   22    // Invalid argument
#define MPROTECT_ENOMEM   12    // Not enough memory
#define MPROTECT_EACCES   13    // Permission denied

#ifdef __cplusplus
}
#endif

#endif // MPROTECT_H
