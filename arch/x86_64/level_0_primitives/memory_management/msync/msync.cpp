// filepath: msync.cpp
/**
 * POSIX Syscall Implementation: msync
 * Architecture: 64-bit
 * Module: msync - Memory Synchronization
 * Level: 0 (Primitive)
 */

#include "msync.h"

// Definizioni minime necessarie
#define NULL ((void*)0)
#define EINVAL 22
#define ENOMEM 12
#define EIO 5
#define ENOSYS 38

// Forward declarations for system calls
extern "C" {
    long syscall(long number, ...);
    char* getenv(const char* name);
    long write(int fd, const void* buf, unsigned long count);
    long open(const char* pathname, int flags);
    long close(int fd);
    long sysconf(int name);
}

// Syscall numbers for x86_64
#define SYS_mmap 9
#define SYS_munmap 11
#define SYS_msync 26
#define SYS_write 1
#define SYS_open 2
#define SYS_close 3

// Open flags
#define O_RDWR 2
#define O_CREAT 64

// mmap flags
#define PROT_READ 1
#define PROT_WRITE 2
#define MAP_SHARED 1

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
    if (getenv("MSYNC_DEBUG")) {
        const char debug_prefix[] = "[MSYNC DEBUG] ";
        const char newline[] = "\n";
        write(2, debug_prefix, sizeof(debug_prefix) - 1);
        write(2, msg, __builtin_strlen(msg));
        write(2, newline, 1);
    }
}

// Print helper for tests
static void msync_print_msg(const char* msg) {
    write(1, msg, __builtin_strlen(msg));
    write(1, "\n", 1);
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg msync_print_msg
#else
#define print_msg msync_print_msg
#endif

extern "C" {

/**
 * msync_impl - Synchronize memory with physical storage
 * @addr: Starting address of the memory area
 * @length: Length of the memory area in bytes
 * @flags: Synchronization flags (MS_ASYNC, MS_SYNC, MS_INVALIDATE)
 * 
 * Returns: 0 on success, -1 on error (with errno set)
 */
int msync_impl(void *addr, size_t length, int flags) {
    debug_log("msync_impl called");
    
    // Parameter validation
    if (addr == NULL) {
        debug_log("msync_impl: addr is NULL");
        errno = EINVAL;
        return -1;
    }
    
    if (length == 0) {
        debug_log("msync_impl: length is 0");
        errno = EINVAL;
        return -1;
    }
    
    // Validate synchronization flags
    if ((flags & (MS_ASYNC | MS_SYNC)) == (MS_ASYNC | MS_SYNC)) {
        debug_log("msync_impl: MS_ASYNC and MS_SYNC cannot be used together");
        errno = EINVAL;
        return -1;
    }
    
    if ((flags & (MS_ASYNC | MS_SYNC)) == 0) {
        debug_log("msync_impl: either MS_ASYNC or MS_SYNC must be specified");
        errno = EINVAL;
        return -1;
    }
    
    // Check for invalid flags
    if (flags & ~(MS_ASYNC | MS_SYNC | MS_INVALIDATE)) {
        debug_log("msync_impl: invalid flags specified");
        errno = EINVAL;
        return -1;
    }
    
    // Check address alignment (should be page-aligned)
    long page_size = sysconf(_SC_PAGESIZE);
    if (page_size == -1) {
        page_size = 4096; // Default page size
    }
    
    if ((unsigned long)addr % page_size != 0) {
        debug_log("msync_impl: addr not page-aligned");
        errno = EINVAL;
        return -1;
    }
    
#ifdef __x86_64__
    // x86_64 syscall: msync
    long result = syscall(SYS_msync, addr, length, flags);
    
    if (result == -1) {
        debug_log("msync_impl: syscall failed");
        // errno is already set by syscall
        return -1;
    }
    
    debug_log("msync_impl: success");
    return 0;
#else
    debug_log("msync_impl: unsupported architecture");
    errno = ENOSYS;
    return -1;
#endif
}

/**
 * msync_test - Test function for msync implementation
 * 
 * Returns: 0 on success, -1 on failure
 */
int msync_test() {
    print_msg("=== Testing msync implementation ===");
    
    // Test 1: Create a temporary file and test file-backed mapping sync
    print_msg("Test 1: Test msync with file-backed mapping");
    
    // Create a temporary file
    const char* test_file = "/tmp/msync_test.tmp";
    int fd = syscall(SYS_open, test_file, O_RDWR | O_CREAT, 0644);
    if (fd == -1) {
        print_msg("Test 1: Failed to create test file");
        return -1;
    }
    
    // Write some data to the file and extend it to page size
    const char test_data[] = "Hello, msync test!";
    write(fd, test_data, sizeof(test_data));
    
    // Map the file with shared mapping
    void *mapped_addr = (void*)syscall(SYS_mmap, NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (mapped_addr == (void*)-1) {
        print_msg("Test 1: Failed to map file");
        close(fd);
        return -1;
    }
    
    print_msg("Test 1: File mapped successfully");
    
    // Modify the mapped memory
    char* mapped_data = (char*)mapped_addr;
    mapped_data[0] = 'X'; // Change first character
    
    // Test synchronous sync
    int result = msync_impl(mapped_addr, 4096, MS_SYNC);
    if (result == 0) {
        print_msg("Test 1: MS_SYNC successful ✓");
    } else {
        print_msg("Test 1: MS_SYNC failed ✗");
        syscall(SYS_munmap, mapped_addr, 4096);
        close(fd);
        return -1;
    }
    
    // Test asynchronous sync  
    result = msync_impl(mapped_addr, 4096, MS_ASYNC);
    if (result == 0) {
        print_msg("Test 1: MS_ASYNC successful ✓");
    } else {
        print_msg("Test 1: MS_ASYNC failed ✗");
        syscall(SYS_munmap, mapped_addr, 4096);
        close(fd);
        return -1;
    }
    
    // Clean up
    syscall(SYS_munmap, mapped_addr, 4096);
    close(fd);
    
    // Test 2: Try msync with NULL pointer (should fail)
    print_msg("Test 2: Try msync with NULL pointer (should fail)");
    result = msync_impl(NULL, 4096, MS_SYNC);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 2: Correctly rejected NULL pointer ✓");
    } else {
        print_msg("Test 2: Failed to reject NULL pointer ✗");
        return -1;
    }
    
    // Test 3: Try msync with length 0 (should fail)
    print_msg("Test 3: Try msync with length 0 (should fail)");
    result = msync_impl((void*)0x1000, 0, MS_SYNC);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 3: Correctly rejected zero length ✓");
    } else {
        print_msg("Test 3: Failed to reject zero length ✗");
        return -1;
    }
    
    // Test 4: Try msync with both MS_ASYNC and MS_SYNC (should fail)
    print_msg("Test 4: Try msync with both MS_ASYNC and MS_SYNC (should fail)");
    result = msync_impl((void*)0x1000, 4096, MS_ASYNC | MS_SYNC);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 4: Correctly rejected conflicting flags ✓");
    } else {
        print_msg("Test 4: Failed to reject conflicting flags ✗");
        return -1;
    }
    
    // Test 5: Try msync with neither MS_ASYNC nor MS_SYNC (should fail)
    print_msg("Test 5: Try msync with no sync flags (should fail)");
    result = msync_impl((void*)0x1000, 4096, MS_INVALIDATE);
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 5: Correctly rejected missing sync flags ✓");
    } else {
        print_msg("Test 5: Failed to reject missing sync flags ✗");
        return -1;
    }
    
    // Test 6: Try msync with non-aligned address (should fail)
    print_msg("Test 6: Try msync with non-aligned address (should fail)");
    result = msync_impl((void*)0x1001, 4096, MS_SYNC); // Not page-aligned
    if (result == -1 && errno == EINVAL) {
        print_msg("Test 6: Correctly rejected non-aligned address ✓");
    } else {
        print_msg("Test 6: Failed to reject non-aligned address ✗");
        return -1;
    }
    
    print_msg("=== All msync tests passed! ===");
    return 0;
}

/**
 * Module information functions
 */
const char* msync_get_description() {
    return "POSIX msync syscall - synchronize memory with physical storage";
}

const char* msync_get_arch() {
    return "x86_64";
}

int msync_get_dependencies(char** deps, int max_deps) {
    if (deps && max_deps > 0) {
        deps[0] = (char*)"syscall interface";
        if (max_deps > 1) {
            deps[1] = (char*)"memory management";
            if (max_deps > 2) {
                deps[2] = (char*)"file system";
                if (max_deps > 3) {
                    deps[3] = (char*)"memory mapping";
                    return 4;
                }
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
    print_msg("=== MSYNC Module Test ===");
    const char desc_prefix[] = "Description: ";
    const char arch_prefix[] = "Architecture: ";
    write(1, desc_prefix, sizeof(desc_prefix) - 1);
    write(1, msync_get_description(), __builtin_strlen(msync_get_description()));
    write(1, "\n", 1);
    write(1, arch_prefix, sizeof(arch_prefix) - 1);
    write(1, msync_get_arch(), __builtin_strlen(msync_get_arch()));
    write(1, "\n\n", 2);
    
    return msync_test();
}
#endif
