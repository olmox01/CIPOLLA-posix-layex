// filepath: memory_manager.h
/**
 * Memory Management Suite - POSIX System Calls
 * Team Level 0 - Memory Management Integration
 * Architecture: x86_64
 * 
 * Complete implementation of all POSIX memory management system calls:
 * - brk: Program break control
 * - sbrk: Increment program break
 * - mmap: Memory mapping
 * - munmap: Memory unmapping  
 * - mprotect: Memory protection
 * - msync: Memory synchronization
 */

#ifndef MEMORY_MANAGER_H
#define MEMORY_MANAGER_H

// Include all memory management modules
#include "brk/brk.h"
#include "sbrk/sbrk.h"
#include "mmap/mmap.h"
#include "munmap/munmap.h"
#include "mprotect/mprotect.h"
#include "msync/msync.h"

#ifdef __cplusplus
extern "C" {
#endif

// Memory Manager API
typedef struct {
    const char* name;
    const char* description;
    const char* arch;
    int (*test_function)(void);
    const char* (*get_description)(void);
    const char* (*get_arch)(void);
    int (*get_dependencies)(char**, int);
} mm_module_t;

// Main integration functions
int memory_manager_init(void);
int memory_manager_test_all(void);
int memory_manager_get_modules(mm_module_t** modules, int* count);
void memory_manager_print_info(void);

// Individual module access functions
int memory_manager_test_brk(void);
int memory_manager_test_sbrk(void);
int memory_manager_test_mmap(void);
int memory_manager_test_munmap(void);
int memory_manager_test_mprotect(void);
int memory_manager_test_msync(void);

// Utility functions
void memory_manager_print_module_info(const char* module_name);
int memory_manager_validate_all(void);

#ifdef __cplusplus
}
#endif

#endif // MEMORY_MANAGER_H
