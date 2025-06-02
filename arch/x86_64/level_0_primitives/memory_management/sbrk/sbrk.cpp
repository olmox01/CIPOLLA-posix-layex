// filepath: sbrk.cpp
/**
 * POSIX Syscall Implementation: sbrk
 * Architecture: 64-bit
 * Module: sbrk - Increment Program Break
 * Level: 0 (Primitive)
 */

#include "sbrk.h"

// Definizioni minime necessarie
#define NULL ((void*)0)
#define ENOMEM 12

// Forward declarations for system calls
extern "C" {
    long syscall(long number, ...);
    char* getenv(const char* name);
    long write(int fd, const void* buf, unsigned long count);
}

// Syscall numbers for x86_64
#define SYS_brk 12
#define SYS_write 1

// Global errno variable
#ifdef STANDALONE_BUILD
int errno = 0;
#else
extern int errno;
#endif

// Simple print function using write syscall
static void sbrk_print_msg(const char* msg) {
    const char* p = msg;
    int len = 0;
    while (p[len]) len++;  // Calculate length
    syscall(SYS_write, 1, msg, len);  // Write to stdout
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg sbrk_print_msg
#else
#define print_msg sbrk_print_msg
#endif

extern "C" {

void* sbrk_impl(intptr_t increment) {
    // Debug logging opzionale
    char* debug_env = getenv("SBRK_DEBUG");
    if (debug_env) {
        print_msg("DEBUG: sbrk_impl called\n");
    }
    
    // 1. Ottieni program break attuale
    void* old_brk = (void*)syscall(SYS_brk, 0);
    if (old_brk == (void*)-1) {
        return (void*)-1;
    }
    
    // 2. Se increment è 0, ritorna solo il valore attuale
    if (increment == 0) {
        return old_brk;
    }
    
    // 3. Calcola nuovo break
    void* new_brk = (char*)old_brk + increment;
    
    // 4. Validazione overflow/underflow
    if (increment > 0 && new_brk < old_brk) {
        errno = ENOMEM;  // Overflow
        return (void*)-1;
    }
    
    if (increment < 0 && new_brk > old_brk) {
        errno = ENOMEM;  // Underflow
        return (void*)-1;
    }
    
    // 5. Imposta nuovo break (solo espansioni per sicurezza)
    if (increment > 0) {
        void* result_brk = (void*)syscall(SYS_brk, new_brk);
        if (result_brk != new_brk) {
            errno = ENOMEM;
            return (void*)-1;
        }
    }
    
    // 6. Ritorna vecchio valore
    return old_brk;
}

int sbrk_test(void) {
    print_msg("Testing sbrk (64-bit)...\n");
    
    // Test 1: Query (increment = 0)
    void *current = sbrk_impl(0);
    if (current == (void*)-1) {
        print_msg("❌ Failed to query current break\n");
        return -1;
    }
    print_msg("✅ Current break queried\n");
    
    // Test 2: Positive increment
    void *after_inc = sbrk_impl(4096);
    if (after_inc == (void*)-1) {
        print_msg("❌ Failed positive increment\n");
        return -1;
    }
    if (after_inc != current) {
        print_msg("❌ Returned value should be old break\n");
        return -1;
    }
    print_msg("✅ Positive increment successful\n");
    
    // Test 3: Verify new break
    void *new_current = sbrk_impl(0);
    if (new_current != (char*)current + 4096) {
        print_msg("❌ New break verification failed\n");
        return -1;
    }
    print_msg("✅ New break verified\n");
    
    // Test 4: Another expansion
    void *second_inc = sbrk_impl(8192);
    if (second_inc == (void*)-1) {
        print_msg("❌ Second increment failed\n");
        return -1;
    }
    print_msg("✅ Second increment successful\n");
    
    print_msg("✅ All sbrk tests passed!\n");
    return 0;
}

// Module information API
const char* sbrk_get_description(void) {
    return "POSIX sbrk syscall - Increment program break for heap management";
}

const char* sbrk_get_arch(void) {
    return "x86_64";
}

int sbrk_get_dependencies(char** deps, int max_deps) {
    // sbrk is a primitive with no dependencies
    (void)deps;    // Suppress unused parameter warning
    (void)max_deps;
    return 0;      // No dependencies
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    print_msg("=== Testing sbrk ===\n");
    print_msg("Description: POSIX sbrk syscall - Increment program break\n");
    print_msg("Architecture: x86_64\n");
    print_msg("\n");
    
    return sbrk_test();
}
#endif
