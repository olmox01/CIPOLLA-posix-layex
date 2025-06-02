// filepath: mprotect.cpp
/**
 * POSIX Syscall Implementation: mprotect
 * Architecture: 64-bit
 * Module: mprotect - Memory Protection
 * Level: 0 (Primitive)
 */

#include "mprotect.h"

// Definizioni minime necessarie
#define NULL ((void*)0)
#define EINVAL 22
#define ENOMEM 12
#define EACCES 13
#define ENOSYS 38

// Forward declarations for system calls
extern "C" {
    long syscall(long number, ...);
    char* getenv(const char* name);
    long write(int fd, const void* buf, unsigned long count);
    long sysconf(int name);
}

// Syscall numbers for x86_64
#define SYS_mmap 9
#define SYS_mprotect 10
#define SYS_munmap 11
#define SYS_write 1

// sysconf constants
#define _SC_PAGESIZE 30

// Global errno variable  
#ifdef STANDALONE_BUILD
int errno = 0;
#else
extern int errno;
#endif

// Debug helper
static void debug_log(const char* msg) {
    if (getenv("MPROTECT_DEBUG")) {
        const char debug_prefix[] = "[MPROTECT DEBUG] ";
        const char newline[] = "\n";
        write(2, debug_prefix, sizeof(debug_prefix) - 1);
        write(2, msg, __builtin_strlen(msg));
        write(2, newline, 1);
    }
}

// Print helper for tests
static void mprotect_print_msg(const char* msg) {
    write(1, msg, __builtin_strlen(msg));
    write(1, "\n", 1);
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg mprotect_print_msg
#else
#define print_msg mprotect_print_msg
#endif

extern "C" {

/**
 * mprotect_impl - Change memory protection
 * @addr: Starting address of the memory area
 * @len: Length of the memory area in bytes
 * @prot: Protection flags (PROT_READ, PROT_WRITE, PROT_EXEC, PROT_NONE)
 * 
 * Returns: 0 on success, -1 on error (with errno set)
 */
int mprotect_impl(void *addr, size_t len, int prot) {
    debug_log("mprotect_impl called");
    
    // Parameter validation
    if (addr == NULL) {
        debug_log("mprotect_impl: addr is NULL");
        errno = EINVAL;
        return -1;
    }
    
    if (len == 0) {
        debug_log("mprotect_impl: len is 0");
        errno = EINVAL;
        return -1;
    }
    
    // Validate protection flags
    if (prot & ~(PROT_READ | PROT_WRITE | PROT_EXEC | PROT_NONE)) {
        debug_log("mprotect_impl: invalid protection flags");
        errno = EINVAL;
        return -1;
    }
    
    // Check address alignment (should be page-aligned)
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        page_size = 4096; // Default page size
    }
    
    if ((unsigned long)addr % page_size != 0) {
        debug_log("mprotect_impl: addr not page-aligned");
        errno = EINVAL;
        return -1;
    }
    
#ifdef __x86_64__
    // x86_64 syscall: mprotect
    long result = syscall(SYS_mprotect, addr, len, prot);
    
    if (result == -1) {
        debug_log("mprotect_impl: syscall failed");
        // errno is already set by syscall
        return -1;
    }
    
    debug_log("mprotect_impl: success");
    return 0;
#else
    debug_log("mprotect_impl: unsupported architecture");
    errno = ENOSYS;
    return -1;
#endif
}

/**
 * mprotect_test - Test function for mprotect implementation
 * 
 * Returns: 0 on success, -1 on failure
 */
int mprotect_test() {
    print_msg("=== Testing mprotect implementation ===");
    
    // Test 1: Map some memory first, then change its protection
    print_msg("Test 1: Map memory and change protection to read-only");
    
    // Map memory with read/write permissions
    void *mapped_addr = (void*)syscall(SYS_mmap, NULL, 4096, PROT_READ | PROT_WRITE, 34, -1, 0); // mmap anonymous
    if (mapped_addr == (void*)-1) {
        print_msg("Test 1: Failed to map memory for testing");
        return -1;
    }
    
    print_msg("Test 1: Memory mapped with RW permissions");
    
    // Write to memory (should work)
    *((int*)mapped_addr) = 42;
    print_msg("Test 1: Successfully wrote to memory");
    
    // Change protection to read-only
    int result = mprotect_impl(mapped_addr, 4096, PROT_READ);
    if (result == 0) {
        print_msg("Test 1: Successfully changed protection to read-only ✓");
    } else {
        print_msg("Test 1: Failed to change protection ✗");
        syscall(SYS_munmap, mapped_addr, 4096);
        return -1;
    }
    
    // Verify we can still read
    int value = *((int*)mapped_addr);
    if (value == 42) {
        print_msg("Test 1: Successfully read from protected memory ✓");
    } else {
        print_msg("Test 1: Failed to read from protected memory ✗");
    }
    
    // Clean up
    syscall(SYS_munmap, mapped_addr, 4096);
    
    // Test 2: Try to use mprotect with NULL pointer (should fail)
    print_msg("Test 2: Try mprotect with NULL pointer (should fail)");
    result = mprotect_impl(NULL, 4096, PROT_READ);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 2: Correctly rejected NULL pointer ✓");
    } else {
        print_msg("Test 2: Failed to reject NULL pointer ✗");
        return -1;
    }
    
    // Test 3: Try to use mprotect with length 0 (should fail)
    print_msg("Test 3: Try mprotect with length 0 (should fail)");
    result = mprotect_impl((void*)0x1000, 0, PROT_READ);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 3: Correctly rejected zero length ✓");
    } else {
        print_msg("Test 3: Failed to reject zero length ✗");
        return -1;
    }
    
    // Test 4: Try mprotect with invalid protection flags (should fail)
    print_msg("Test 4: Try mprotect with invalid flags (should fail)");
    result = mprotect_impl((void*)0x1000, 4096, 0xFF); // Invalid flags
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 4: Correctly rejected invalid flags ✓");
    } else {
        print_msg("Test 4: Failed to reject invalid flags ✗");
        return -1;
    }
    
    // Test 5: Try mprotect with non-aligned address (should fail)
    print_msg("Test 5: Try mprotect with non-aligned address (should fail)");
    result = mprotect_impl((void*)0x1001, 4096, PROT_READ); // Not page-aligned
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 5: Correctly rejected non-aligned address ✓");
    } else {
        print_msg("Test 5: Failed to reject non-aligned address ✗");
        return -1;
    }
    
    print_msg("=== All mprotect tests passed! ===");
    return 0;
}

/**
 * Module information functions
 */
const char* mprotect_get_description() {
    return "POSIX mprotect syscall - change memory protection";
}

const char* mprotect_get_arch() {
    return "x86_64";
}

int mprotect_get_dependencies(char** deps, int max_deps) {
    if (deps && max_deps > 0) {
        deps[0] = (char*)"syscall interface";
        if (max_deps > 1) {
            deps[1] = (char*)"memory management";
            if (max_deps > 2) {
                deps[2] = (char*)"memory mapping";
                return 3;
            }
            return 2;
        }
        return 1;
    }
    return 0;
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    print_msg("=== MPROTECT Module Test ===");
    const char desc_prefix[] = "Description: ";
    const char arch_prefix[] = "Architecture: ";
    write(1, desc_prefix, sizeof(desc_prefix) - 1);
    write(1, mprotect_get_description(), __builtin_strlen(mprotect_get_description()));
    write(1, "\n", 1);
    write(1, arch_prefix, sizeof(arch_prefix) - 1);
    write(1, mprotect_get_arch(), __builtin_strlen(mprotect_get_arch()));
    write(1, "\n\n", 2);
    
    return mprotect_test();
}
#endif
