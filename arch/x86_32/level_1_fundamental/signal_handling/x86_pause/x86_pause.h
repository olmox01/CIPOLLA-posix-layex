// filepath: x86_pause.h
/**
 * POSIX Syscall Header: pause
 * Module: x86_pause
 */

#ifndef X86_PAUSE_H
#define X86_PAUSE_H

#ifdef __cplusplus
extern "C" {
#endif

// Function prototypes
int x86_pause_impl();
int x86_pause_test();

// Constants and definitions for pause
// TODO: Aggiungere definizioni specifiche

#ifdef __cplusplus
}
#endif

#endif // X86_PAUSE_H
