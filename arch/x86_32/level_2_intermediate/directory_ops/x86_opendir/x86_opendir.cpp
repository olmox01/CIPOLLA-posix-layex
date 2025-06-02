// filepath: x86_opendir.cpp
/**
 * POSIX Syscall Implementation: opendir
 * Architecture: 32-bit
 * Module: x86_opendir
 */

#include "x86_opendir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare opendir per architettura 32-bit

extern "C" {

int x86_opendir_impl() {
    // TODO: Implementazione della syscall opendir
    std::cout << "Syscall opendir (32-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int x86_opendir_test() {
    // TODO: Test di base per opendir
    std::cout << "Testing opendir (32-bit)..." << std::endl;
    return x86_opendir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing x86_opendir ===" << std::endl;
    return x86_opendir_test();
}
#endif
