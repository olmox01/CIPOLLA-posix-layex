// filepath: x86_mkdir.cpp
/**
 * POSIX Syscall Implementation: mkdir
 * Architecture: 32-bit
 * Module: x86_mkdir
 */

#include "x86_mkdir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare mkdir per architettura 32-bit

extern "C" {

int x86_mkdir_impl() {
    // TODO: Implementazione della syscall mkdir
    std::cout << "Syscall mkdir (32-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int x86_mkdir_test() {
    // TODO: Test di base per mkdir
    std::cout << "Testing mkdir (32-bit)..." << std::endl;
    return x86_mkdir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing x86_mkdir ===" << std::endl;
    return x86_mkdir_test();
}
#endif
