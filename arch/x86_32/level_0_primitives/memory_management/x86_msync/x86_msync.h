// filepath: x86_msync.h
/**
 * POSIX Syscall Header: msync
 * Module: x86_msync
 */

#ifndef X86_MSYNC_H
#define X86_MSYNC_H

#ifdef __cplusplus
extern "C" {
#endif

// Function prototypes
int x86_msync_impl();
int x86_msync_test();

// Constants and definitions for msync
// TODO: Aggiungere definizioni specifiche

#ifdef __cplusplus
}
#endif

#endif // X86_MSYNC_H
