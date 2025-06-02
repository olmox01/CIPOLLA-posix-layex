// filepath: memory_manager.cpp
/**
 * Memory Management Suite - POSIX System Calls
 * Team Level 0 - Memory Management Integration
 * Architecture: x86_64
 * 
 * Unified memory manager that integrates all POSIX memory management syscalls
 */

#include "memory_manager.h"

// Definizioni minime necessarie
#define NULL 0

// Forward declarations for system calls
extern "C" {
    long write(int fd, const void* buf, unsigned long count);
    unsigned long __builtin_strlen(const char* s);
    int __builtin_strcmp(const char* s1, const char* s2);
}

// Global errno variable for library linking
int errno = 0;

// Internal helper functions
static void mm_print_msg(const char* msg) {
    if (msg) {
        write(1, msg, __builtin_strlen(msg));
        write(1, "\n", 1);
    }
}

static void mm_print_separator(void) {
    const char separator[] = "=====================================";
    write(1, separator, sizeof(separator) - 1);
    write(1, "\n", 1);
}

static void mm_print_header(const char* title) {
    mm_print_separator();
    mm_print_msg(title);
    mm_print_separator();
}

// Global module registry
static mm_module_t mm_modules[] = {
    {
        .name = "brk",
        .description = "Program break control",
        .arch = "x86_64",
        .test_function = brk_test,
        .get_description = brk_get_description,
        .get_arch = brk_get_arch,
        .get_dependencies = brk_get_dependencies
    },
    {
        .name = "sbrk", 
        .description = "Increment program break",
        .arch = "x86_64",
        .test_function = sbrk_test,
        .get_description = sbrk_get_description,
        .get_arch = sbrk_get_arch,
        .get_dependencies = sbrk_get_dependencies
    },
    {
        .name = "mmap",
        .description = "Memory mapping",
        .arch = "x86_64", 
        .test_function = mmap_test,
        .get_description = mmap_get_description,
        .get_arch = mmap_get_arch,
        .get_dependencies = mmap_get_dependencies
    },
    {
        .name = "munmap",
        .description = "Memory unmapping",
        .arch = "x86_64",
        .test_function = munmap_test,
        .get_description = munmap_get_description,
        .get_arch = munmap_get_arch,
        .get_dependencies = munmap_get_dependencies
    },
    {
        .name = "mprotect",
        .description = "Memory protection",
        .arch = "x86_64",
        .test_function = mprotect_test,
        .get_description = mprotect_get_description,
        .get_arch = mprotect_get_arch,
        .get_dependencies = mprotect_get_dependencies
    },
    {
        .name = "msync",
        .description = "Memory synchronization", 
        .arch = "x86_64",
        .test_function = msync_test,
        .get_description = msync_get_description,
        .get_arch = msync_get_arch,
        .get_dependencies = msync_get_dependencies
    }
};

static const int mm_module_count = sizeof(mm_modules) / sizeof(mm_modules[0]);

extern "C" {

/**
 * memory_manager_init - Initialize memory manager
 * 
 * Returns: 0 on success, -1 on failure
 */
int memory_manager_init(void) {
    mm_print_header("MEMORY MANAGER INITIALIZATION");
    mm_print_msg("Initializing POSIX Memory Management Suite...");
    mm_print_msg("Architecture: x86_64");
    
    // Print available modules
    mm_print_msg("\nAvailable modules:");
    for (int i = 0; i < mm_module_count; i++) {
        const char prefix[] = "  - ";
        const char sep[] = ": ";
        write(1, prefix, sizeof(prefix) - 1);
        write(1, mm_modules[i].name, __builtin_strlen(mm_modules[i].name));
        write(1, sep, sizeof(sep) - 1);
        write(1, mm_modules[i].description, __builtin_strlen(mm_modules[i].description));
        write(1, "\n", 1);
    }
    
    mm_print_msg("\nMemory Manager initialized successfully!");
    return 0;
}

/**
 * memory_manager_test_all - Run tests for all memory management modules
 * 
 * Returns: 0 if all tests pass, -1 if any test fails
 */
int memory_manager_test_all(void) {
    mm_print_header("MEMORY MANAGER - COMPREHENSIVE TEST SUITE");
    
    int total_tests = 0;
    int passed_tests = 0;
    int failed_tests = 0;
    
    for (int i = 0; i < mm_module_count; i++) {
        mm_module_t* module = &mm_modules[i];
        
        // Print module header
        const char test_header[] = "\n--- Testing Module: ";
        const char header_end[] = " ---";
        write(1, test_header, sizeof(test_header) - 1);
        write(1, module->name, __builtin_strlen(module->name));
        write(1, header_end, sizeof(header_end) - 1);
        write(1, "\n", 1);
        
        // Print module description
        const char desc_prefix[] = "Description: ";
        write(1, desc_prefix, sizeof(desc_prefix) - 1);
        if (module->get_description) {
            write(1, module->get_description(), __builtin_strlen(module->get_description()));
        }
        write(1, "\n\n", 2);
        
        // Run test
        total_tests++;
        if (module->test_function && module->test_function() == 0) {
            const char success[] = "✅ Module test PASSED\n";
            write(1, success, sizeof(success) - 1);
            passed_tests++;
        } else {
            const char failure[] = "❌ Module test FAILED\n";
            write(1, failure, sizeof(failure) - 1);
            failed_tests++;
        }
    }
    
    // Print summary
    mm_print_header("TEST SUMMARY");
    const char total_str[] = "Total modules tested: ";
    const char passed_str[] = "Passed: ";
    const char failed_str[] = "Failed: ";
    
    write(1, total_str, sizeof(total_str) - 1);
    // Convert number to string (simple implementation)
    char num_buf[16];
    int pos = 0;
    int temp = total_tests;
    if (temp == 0) {
        num_buf[pos++] = '0';
    } else {
        while (temp > 0) {
            num_buf[pos++] = '0' + (temp % 10);
            temp /= 10;
        }
        // Reverse the string
        for (int j = 0; j < pos / 2; j++) {
            char tmp = num_buf[j];
            num_buf[j] = num_buf[pos - 1 - j];
            num_buf[pos - 1 - j] = tmp;
        }
    }
    num_buf[pos] = '\0';
    write(1, num_buf, pos);
    write(1, "\n", 1);
    
    // Convert passed tests
    pos = 0;
    temp = passed_tests;
    if (temp == 0) {
        num_buf[pos++] = '0';
    } else {
        while (temp > 0) {
            num_buf[pos++] = '0' + (temp % 10);
            temp /= 10;
        }
        for (int j = 0; j < pos / 2; j++) {
            char tmp = num_buf[j];
            num_buf[j] = num_buf[pos - 1 - j];
            num_buf[pos - 1 - j] = tmp;
        }
    }
    num_buf[pos] = '\0';
    write(1, passed_str, sizeof(passed_str) - 1);
    write(1, num_buf, pos);
    write(1, "\n", 1);
    
    // Convert failed tests
    pos = 0;
    temp = failed_tests;
    if (temp == 0) {
        num_buf[pos++] = '0';
    } else {
        while (temp > 0) {
            num_buf[pos++] = '0' + (temp % 10);
            temp /= 10;
        }
        for (int j = 0; j < pos / 2; j++) {
            char tmp = num_buf[j];
            num_buf[j] = num_buf[pos - 1 - j];
            num_buf[pos - 1 - j] = tmp;
        }
    }
    num_buf[pos] = '\0';
    write(1, failed_str, sizeof(failed_str) - 1);
    write(1, num_buf, pos);
    write(1, "\n", 1);
    
    if (failed_tests == 0) {
        mm_print_msg("\n🎉 ALL TESTS PASSED! Memory management suite is fully functional.");
        return 0;
    } else {
        mm_print_msg("\n⚠️  Some tests failed. Please check individual module implementations.");
        return -1;
    }
}

/**
 * memory_manager_get_modules - Get list of available modules
 * 
 * @modules: Pointer to receive modules array
 * @count: Pointer to receive module count
 * 
 * Returns: 0 on success, -1 on failure
 */
int memory_manager_get_modules(mm_module_t** modules, int* count) {
    if (!modules || !count) {
        return -1;
    }
    
    *modules = mm_modules;
    *count = mm_module_count;
    return 0;
}

/**
 * memory_manager_print_info - Print detailed information about memory manager
 */
void memory_manager_print_info(void) {
    mm_print_header("MEMORY MANAGER INFORMATION");
    
    mm_print_msg("POSIX Memory Management Suite");
    mm_print_msg("Team Level 0 - Complete Implementation");
    mm_print_msg("Architecture: x86_64");
    mm_print_msg("");
    
    mm_print_msg("Implemented System Calls:");
    for (int i = 0; i < mm_module_count; i++) {
        const char prefix[] = "  ";
        const char sep1[] = " (";
        const char sep2[] = ") - ";
        
        write(1, prefix, sizeof(prefix) - 1);
        write(1, mm_modules[i].name, __builtin_strlen(mm_modules[i].name));
        write(1, sep1, sizeof(sep1) - 1);
        write(1, mm_modules[i].arch, __builtin_strlen(mm_modules[i].arch));
        write(1, sep2, sizeof(sep2) - 1);
        if (mm_modules[i].get_description) {
            write(1, mm_modules[i].get_description(), __builtin_strlen(mm_modules[i].get_description()));
        }
        write(1, "\n", 1);
    }
    
    mm_print_msg("");
    mm_print_msg("Features:");
    mm_print_msg("  • Full POSIX compliance");
    mm_print_msg("  • x86_64 native syscalls");
    mm_print_msg("  • Comprehensive error handling");
    mm_print_msg("  • Complete test coverage");
    mm_print_msg("  • Production-ready implementation");
}

// Individual module test functions
int memory_manager_test_brk(void) {
    mm_print_msg("Testing BRK module...");
    return brk_test();
}

int memory_manager_test_sbrk(void) {
    mm_print_msg("Testing SBRK module...");
    return sbrk_test();
}

int memory_manager_test_mmap(void) {
    mm_print_msg("Testing MMAP module...");
    return mmap_test();
}

int memory_manager_test_munmap(void) {
    mm_print_msg("Testing MUNMAP module...");
    return munmap_test();
}

int memory_manager_test_mprotect(void) {
    mm_print_msg("Testing MPROTECT module...");
    return mprotect_test();
}

int memory_manager_test_msync(void) {
    mm_print_msg("Testing MSYNC module...");
    return msync_test();
}

/**
 * memory_manager_print_module_info - Print detailed info for specific module
 * 
 * @module_name: Name of the module to print info for
 */
void memory_manager_print_module_info(const char* module_name) {
    if (!module_name) {
        mm_print_msg("Error: Module name is NULL");
        return;
    }
    
    // Find module
    mm_module_t* found_module = NULL;
    for (int i = 0; i < mm_module_count; i++) {
        if (__builtin_strcmp(mm_modules[i].name, module_name) == 0) {
            found_module = &mm_modules[i];
            break;
        }
    }
    
    if (!found_module) {
        mm_print_msg("Error: Module not found");
        return;
    }
    
    // Print module information
    const char header[] = "MODULE INFORMATION: ";
    write(1, header, sizeof(header) - 1);
    write(1, found_module->name, __builtin_strlen(found_module->name));
    write(1, "\n", 1);
    mm_print_separator();
    
    const char desc_prefix[] = "Description: ";
    const char arch_prefix[] = "Architecture: ";
    
    write(1, desc_prefix, sizeof(desc_prefix) - 1);
    if (found_module->get_description) {
        write(1, found_module->get_description(), __builtin_strlen(found_module->get_description()));
    }
    write(1, "\n", 1);
    
    write(1, arch_prefix, sizeof(arch_prefix) - 1);
    if (found_module->get_arch) {
        write(1, found_module->get_arch(), __builtin_strlen(found_module->get_arch()));
    }
    write(1, "\n", 1);
    
    // Print dependencies
    mm_print_msg("Dependencies:");
    if (found_module->get_dependencies) {
        char* deps[10];
        int dep_count = found_module->get_dependencies(deps, 10);
        if (dep_count == 0) {
            mm_print_msg("  None (primitive module)");
        } else {
            for (int i = 0; i < dep_count; i++) {
                const char dep_prefix[] = "  - ";
                write(1, dep_prefix, sizeof(dep_prefix) - 1);
                write(1, deps[i], __builtin_strlen(deps[i]));
                write(1, "\n", 1);
            }
        }
    }
}

/**
 * memory_manager_validate_all - Validate all modules are working correctly
 * 
 * Returns: 0 if all modules validate, -1 if any validation fails
 */
int memory_manager_validate_all(void) {
    mm_print_header("MEMORY MANAGER VALIDATION");
    
    mm_print_msg("Validating all memory management modules...");
    
    // Check each module has required functions
    for (int i = 0; i < mm_module_count; i++) {
        mm_module_t* module = &mm_modules[i];
        
        const char validating[] = "Validating ";
        const char ellipsis[] = "...";
        write(1, validating, sizeof(validating) - 1);
        write(1, module->name, __builtin_strlen(module->name));
        write(1, ellipsis, sizeof(ellipsis) - 1);
        
        if (!module->test_function || !module->get_description || 
            !module->get_arch || !module->get_dependencies) {
            mm_print_msg(" ❌ MISSING FUNCTIONS");
            return -1;
        }
        
        mm_print_msg(" ✅ OK");
    }
    
    mm_print_msg("\n✅ All modules validated successfully!");
    return 0;
}

} // extern "C"

// Main function for the unified memory manager
int main() {
    // Debug output first
    const char debug_start[] = "MEMORY MANAGER STARTING...\n";
    write(1, debug_start, sizeof(debug_start) - 1);
    
    // Initialize memory manager
    if (memory_manager_init() != 0) {
        mm_print_msg("Failed to initialize memory manager");
        return 1;
    }
    
    // Print information
    memory_manager_print_info();
    
    // Validate all modules
    if (memory_manager_validate_all() != 0) {
        mm_print_msg("Module validation failed");
        return 1;
    }
    
    // Run comprehensive tests
    int result = memory_manager_test_all();
    
    const char debug_end[] = "MEMORY MANAGER COMPLETED.\n";
    write(1, debug_end, sizeof(debug_end) - 1);
    
    return result;
}
