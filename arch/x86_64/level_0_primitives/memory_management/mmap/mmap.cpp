// filepath: mmap.cpp
/**
 * POSIX Sys// Global errno variable  
#ifdef STANDALONE_BUILD
int errno = 0;
#else
extern int errno;
#endifll Implementation: mmap
 * Architecture: 64-bit
 * Module: mmap - Memory Mapping
 * Level: 0 (Primitive)
 */

#include "mmap.h"

// Definizioni minime necessarie
#define NULL ((void*)0)
#define EINVAL 22
#define EBADF 9
#define ENOMEM 12

// Forward declarations for system calls
extern "C" {
    long syscall(long number, ...);
    char* getenv(const char* name);
    long write(int fd, const void* buf, unsigned long count);
    long open(const char* pathname, int flags);
    long close(int fd);
    long fcntl(int fd, int cmd, ...);
    long sysconf(int name);
}

// Syscall numbers for x86_64
#define SYS_mmap 9
#define SYS_munmap 11
#define SYS_write 1
#define SYS_open 2
#define SYS_close 3
#define SYS_fcntl 72

// sysconf constants
#define _SC_PAGESIZE 30

// Global errno variable  
#ifdef STANDALONE_BUILD
int errno = 0;
#else
extern int errno;
#endif

// Simple print function using write syscall
static void mmap_print_msg(const char* msg) {
    const char* p = msg;
    int len = 0;
    while (p[len]) len++;  // Calculate length
    syscall(SYS_write, 1, msg, len);  // Write to stdout
}

// Compatibility macro for standalone vs library builds
#ifdef STANDALONE_BUILD
#define print_msg mmap_print_msg
#else
#define print_msg mmap_print_msg
#endif

extern "C" {

void* mmap_impl(void *addr, size_t length, int prot, int flags, int fd, off_t offset) {
    // Debug logging opzionale
    char* debug_env = getenv("MMAP_DEBUG");
    if (debug_env) {
        print_msg("DEBUG: mmap_impl called\n");
    }
    
    // 1. Validazioni parametri
    if (length == 0) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 2. Validazione flags obbligatori
    if (!(flags & MAP_SHARED) && !(flags & MAP_PRIVATE)) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 3. Validazione per file mapping
    if (!(flags & MAP_ANONYMOUS)) {
        if (fd < 0) {
            errno = EBADF;
            return MAP_FAILED;
        }
        
        // Verifica che il file descriptor sia valido
        if (syscall(SYS_fcntl, fd, F_GETFD) == -1) {
            errno = EBADF;
            return MAP_FAILED;
        }
        
        // Validazione allineamento offset
        long page_size = syscall(_SC_PAGESIZE);
        if (page_size <= 0) page_size = 4096;  // Default fallback
        if (offset % page_size != 0) {
            errno = EINVAL;
            return MAP_FAILED;
        }
    }
    
    // 4. Validazione protezioni
    if (prot & ~(PROT_READ | PROT_WRITE | PROT_EXEC | PROT_NONE)) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 5. Chiamata syscall
    #ifdef __x86_64__
    void* result = (void*)syscall(SYS_mmap, addr, length, prot, flags, fd, offset);
    #elif defined(__i386__)
    // Su i386 mmap ha una calling convention diversa
    void* result = (void*)syscall(SYS_mmap, addr, length, prot, flags, fd, offset >> 12);
    #else
    #error "Unsupported architecture"
    #endif
    
    // 6. Gestione errori
    if (result == MAP_FAILED) {
        // errno già impostato dal kernel
        return MAP_FAILED;
    }
    
    return result;
}

int mmap_test(void) {
    print_msg("Testing mmap (64-bit)...\n");
    
    long page_size = 4096;  // Default page size
    
    // Test 1: Anonymous mapping
    void *anon_map = mmap_impl(NULL, page_size, PROT_READ | PROT_WRITE, 
                              MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (anon_map == MAP_FAILED) {
        print_msg("❌ Anonymous mapping failed\n");
        return -1;
    }
    print_msg("✅ Anonymous mapping successful\n");
    
    // Test 2: Write to mapped memory
    *(char*)anon_map = 'A';
    if (*(char*)anon_map != 'A') {
        print_msg("❌ Write to mapped memory failed\n");
        return -1;
    }
    print_msg("✅ Write to mapped memory successful\n");
    
    // Test 3: Unmap
    if (syscall(SYS_munmap, anon_map, page_size) != 0) {
        print_msg("❌ Unmap failed\n");
        return -1;
    }
    print_msg("✅ Unmap successful\n");
    
    // Test 4: File mapping with /dev/zero
    int fd = syscall(SYS_open, "/dev/zero", O_RDONLY);
    if (fd == -1) {
        print_msg("❌ Failed to open /dev/zero\n");
        return -1;
    }
    
    void *file_map = mmap_impl(NULL, page_size, PROT_READ, 
                              MAP_PRIVATE, fd, 0);
    syscall(SYS_close, fd);
    
    if (file_map == MAP_FAILED) {
        print_msg("❌ File mapping failed\n");
        return -1;
    }
    print_msg("✅ File mapping successful\n");
    
    // Test 5: Read from file mapping
    char test_byte = *(char*)file_map;
    if (test_byte != 0) {
        print_msg("❌ /dev/zero should give zero\n");
        return -1;
    }
    print_msg("✅ Read from file mapping successful\n");
    
    // Test 6: Unmap file mapping
    if (syscall(SYS_munmap, file_map, page_size) != 0) {
        print_msg("❌ File unmap failed\n");
        return -1;
    }
    print_msg("✅ File unmap successful\n");
    
    // Test 7: Invalid parameters
    void *invalid_map = mmap_impl(NULL, 0, PROT_READ, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (invalid_map != MAP_FAILED) {
        print_msg("❌ Zero length should fail\n");
        return -1;
    }
    print_msg("✅ Invalid parameter correctly rejected\n");
    
    print_msg("✅ All mmap tests passed!\n");
    return 0;
}

// Module information API
const char* mmap_get_description(void) {
    return "POSIX mmap syscall - Memory mapping for files and anonymous memory";
}

const char* mmap_get_arch(void) {
    return "x86_64";
}

int mmap_get_dependencies(char** deps, int max_deps) {
    // mmap is a primitive with no dependencies
    (void)deps;    // Suppress unused parameter warning
    (void)max_deps;
    return 0;      // No dependencies
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    print_msg("=== Testing mmap ===\n");
    print_msg("Description: POSIX mmap syscall - Memory mapping\n");
    print_msg("Architecture: x86_64\n");
    print_msg("\n");
    
    return mmap_test();
}
#endif
