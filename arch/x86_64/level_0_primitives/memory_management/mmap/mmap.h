// filepath: mmap.h
/**
 * POSIX Syscall Header: mmap
 * Module: mmap - Memory Mapping
 * Architecture: x86_64
 * Level: 0 (Primitive)
 */

#ifndef MMAP_H
#define MMAP_H

// Type definitions
typedef long off_t;
typedef unsigned long size_t;

#ifdef __cplusplus
extern "C" {
#endif

// Main implementation functions
void* mmap_impl(void *addr, size_t length, int prot, int flags, int fd, off_t offset);
int mmap_test(void);

// Module information API
const char* mmap_get_description(void);
const char* mmap_get_arch(void);
int mmap_get_dependencies(char** deps, int max_deps);

// POSIX mmap constants and definitions
#define MAP_FAILED      ((void*)-1)

// Protection flags
#define PROT_NONE       0x0
#define PROT_READ       0x1
#define PROT_WRITE      0x2
#define PROT_EXEC       0x4

// Mapping flags
#define MAP_SHARED      0x01
#define MAP_PRIVATE     0x02
#define MAP_ANONYMOUS   0x20
#define MAP_ANON        MAP_ANONYMOUS

// File operations
#define O_RDONLY        0x00
#define O_WRONLY        0x01
#define O_RDWR          0x02

// fcntl commands
#define F_GETFD         1

// Error conditions
#define MMAP_EINVAL     22    // Invalid argument
#define MMAP_EBADF      9     // Bad file descriptor
#define MMAP_ENOMEM     12    // Out of memory

#ifdef __cplusplus
}
#endif

#endif // MMAP_H
