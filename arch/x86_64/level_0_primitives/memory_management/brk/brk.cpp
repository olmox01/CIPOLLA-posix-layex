// filepath: brk.cpp
/**
 * POSIX Syscall Implementation: brk
 * Architecture: 64-bit
 * Module: brk - Program Break Control
 * Level: 0 (Primitive)
 */

#include "brk.h"

// Definizioni minime necessarie
#define NULL ((void*)0)
#define EINVAL 22
#define ENOMEM 12
#define ENOSYS 38

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
static void brk_print_msg(const char* msg) {
    const char* p = msg;
    int len = 0;
    while (p[len]) len++;  // Calculate length
    syscall(SYS_write, 1, msg, len);  // Write to stdout
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg brk_print_msg
#else
#define print_msg brk_print_msg
#endif

extern "C" {

int brk_impl(void *addr) {
    // Debug logging opzionale (simple version)
    char* debug_env = getenv("BRK_DEBUG");
    if (debug_env) {
        print_msg("DEBUG: brk_impl called\n");
    }
    
    // 1. Validazione indirizzo
    if (addr == NULL) {
        errno = EINVAL;
        return -1;
    }
    
    // 2. Ottieni break attuale per validazione
    void *current_brk = (void*)syscall(SYS_brk, 0);
    if (current_brk == (void*)-1) {
        return -1;
    }
    
    // 3. Validazione range - permettiamo solo espansione
    if (addr < current_brk) {
        // Non permettiamo riduzione dell'heap per sicurezza
        errno = EINVAL;
        return -1;
    }
    
    // 4. Chiamata syscall architettura-specifica
    #ifdef __x86_64__
    void *result = (void*)syscall(SYS_brk, addr);
    #elif defined(__i386__)
    void *result = (void*)syscall(SYS_brk, addr);
    #else
    #error "Unsupported architecture"
    #endif
    
    // 5. Verifica successo
    if (result == addr) {
        return 0;  // Successo
    } else {
        errno = ENOMEM;
        return -1;
    }
}

int brk_test(void) {
    print_msg("Testing brk (64-bit)...\n");
    
    // Test 1: Query current break
    void *initial_brk = (void*)syscall(SYS_brk, 0);
    if (initial_brk == (void*)-1) {
        print_msg("❌ Failed to query initial break\n");
        return -1;
    }
    print_msg("✅ Initial break queried\n");
    
    // Test 2: Expand heap
    void *new_brk = (char*)initial_brk + 4096;
    if (brk_impl(new_brk) != 0) {
        print_msg("❌ Failed to expand heap\n");
        return -1;
    }
    print_msg("✅ Heap expanded\n");
    
    // Test 3: Verify expansion
    void *verify_brk = (void*)syscall(SYS_brk, 0);
    if (verify_brk != new_brk) {
        print_msg("❌ Break verification failed\n");
        return -1;
    }
    print_msg("✅ Break verification successful\n");
    
    // Test 4: Test solo espansione (non reset per sicurezza)
    void *larger_brk = (char*)new_brk + 4096;
    if (brk_impl(larger_brk) != 0) {
        print_msg("❌ Failed to expand further\n");
        return -1;
    }
    print_msg("✅ Further expansion successful\n");
    
    // Test 5: Invalid parameter test
    if (brk_impl(NULL) == 0) {
        print_msg("❌ NULL parameter should fail\n");
        return -1;
    }
    print_msg("✅ NULL parameter correctly rejected\n");
    
    print_msg("✅ All brk tests passed!\n");
    return 0;  // All tests passed
}

// Module information API
const char* brk_get_description(void) {
    return "POSIX brk syscall - Program break control for heap management";
}

const char* brk_get_arch(void) {
    return "x86_64";
}

int brk_get_dependencies(char** deps, int max_deps) {
    // brk is a primitive with no dependencies
    (void)deps;    // Suppress unused parameter warning
    (void)max_deps;
    return 0;      // No dependencies
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    print_msg("=== Testing brk ===\n");
    print_msg("Description: POSIX brk syscall - Program break control\n");
    print_msg("Architecture: x86_64\n");
    print_msg("\n");
    
    return brk_test();
}
#endif
