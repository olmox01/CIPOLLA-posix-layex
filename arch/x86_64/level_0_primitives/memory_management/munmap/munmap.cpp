// filepath: munmap.cpp
/**
 * POSIX Syscall Implementation: munmap
 * Architecture: 64-bit
 * Module: munmap - Memory Unmapping
 * Level: 0 (Primitive)
 */

#include "munmap.h"

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
    long sysconf(int name);
}

// Syscall numbers for x86_64
#define SYS_mmap 9
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
    if (getenv("MUNMAP_DEBUG")) {
        const char debug_prefix[] = "[MUNMAP DEBUG] ";
        const char newline[] = "\n";
        write(2, debug_prefix, sizeof(debug_prefix) - 1);
        write(2, msg, __builtin_strlen(msg));
        write(2, newline, 1);
    }
}

// Print helper for tests
static void munmap_print_msg(const char* msg) {
    write(1, msg, __builtin_strlen(msg));
    write(1, "\n", 1);
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg munmap_print_msg
#else
#define print_msg munmap_print_msg
#endif

extern "C" {

/**
 * munmap_impl - Remove memory mapping
 * @addr: Starting address of the mapping to unmap
 * @length: Length of the mapping in bytes
 * 
 * Returns: 0 on success, -1 on error (with errno set)
 */
int munmap_impl(void *addr, size_t length) {
    debug_log("munmap_impl called");
    
    // Parameter validation
    if (addr == NULL) {
        debug_log("munmap_impl: addr is NULL");
        errno = EINVAL;
        return -1;
    }
    
    if (length == 0) {
        debug_log("munmap_impl: length is 0");
        errno = EINVAL;
        return -1;
    }
    
    // Check address alignment (should be page-aligned)
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        page_size = 4096; // Default page size
    }
    
    if ((unsigned long)addr % page_size != 0) {
        debug_log("munmap_impl: addr not page-aligned");
        errno = EINVAL;
        return -1;
    }
    
#ifdef __x86_64__
    // x86_64 syscall: munmap
    long result = syscall(SYS_munmap, addr, length);
    
    if (result == -1) {
        debug_log("munmap_impl: syscall failed");
        // errno is already set by syscall
        return -1;
    }
    
    debug_log("munmap_impl: success");
    return 0;
#else
    debug_log("munmap_impl: unsupported architecture");
    errno = ENOSYS;
    return -1;
#endif
}

/**
 * munmap_test - Test function for munmap implementation
 * 
 * Returns: 0 on success, -1 on failure
 */
int munmap_test() {
    print_msg("=== Testing munmap implementation ===");
    
    // Test 1: Map some memory first, then unmap it
    print_msg("Test 1: Map memory and then unmap it");
    
    // Need to include mmap for testing
    void *mapped_addr = (void*)syscall(SYS_mmap, NULL, 4096, 3, 34, -1, 0); // mmap anonymous
    if (mapped_addr == (void*)-1) {
        print_msg("Test 1: Failed to map memory for testing");
        return -1;
    }
    
    print_msg("Test 1: Memory mapped successfully");
    
    // Now test unmapping
    int result = munmap_impl(mapped_addr, 4096);
    if (result == 0) {
        print_msg("Test 1: Successfully unmapped memory ✓");
    } else {
        print_msg("Test 1: Failed to unmap memory ✗");
        return -1;
    }
    
    // Test 2: Try to unmap NULL pointer (should fail)
    print_msg("Test 2: Try to unmap NULL pointer (should fail)");
    result = munmap_impl(NULL, 4096);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 2: Correctly rejected NULL pointer ✓");
    } else {
        print_msg("Test 2: Failed to reject NULL pointer ✗");
        return -1;
    }
    
    // Test 3: Try to unmap with length 0 (should fail)  
    print_msg("Test 3: Try to unmap with length 0 (should fail)");
    result = munmap_impl((void*)0x1000, 0);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 3: Correctly rejected zero length ✓");
    } else {
        print_msg("Test 3: Failed to reject zero length ✗");
        return -1;
    }
    
    // Test 4: Try to unmap non-aligned address (should fail)
    print_msg("Test 4: Try to unmap non-aligned address (should fail)");
    result = munmap_impl((void*)0x1001, 4096); // Not page-aligned
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 4: Correctly rejected non-aligned address ✓");
    } else {
        print_msg("Test 4: Failed to reject non-aligned address ✗");
        return -1;
    }
    
    print_msg("=== All munmap tests passed! ===");
    return 0;
}

/**
 * Module information functions
 */
const char* munmap_get_description() {
    return "POSIX munmap syscall - remove memory mapping";
}

const char* munmap_get_arch() {
    return "x86_64";
}

int munmap_get_dependencies(char** deps, int max_deps) {
    if (deps && max_deps > 0) {
        deps[0] = (char*)"syscall interface";
        if (max_deps > 1) {
            deps[1] = (char*)"memory management";
            return 2;
        }
        return 1;
    }
    return 0;
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    print_msg("=== MUNMAP Module Test ===");
    const char desc_prefix[] = "Description: ";
    const char arch_prefix[] = "Architecture: ";
    write(1, desc_prefix, sizeof(desc_prefix) - 1);
    write(1, munmap_get_description(), __builtin_strlen(munmap_get_description()));
    write(1, "\n", 1);
    write(1, arch_prefix, sizeof(arch_prefix) - 1);
    write(1, munmap_get_arch(), __builtin_strlen(munmap_get_arch()));
    write(1, "\n\n", 2);
    
    return munmap_test();
}
#endif
