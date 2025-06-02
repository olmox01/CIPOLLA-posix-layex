// filepath: mkdir.cpp
/**
 * POSIX Syscall Implementation: mkdir
 * Architecture: 64-bit
 * Module: mkdir
 */

#include "mkdir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare mkdir per architettura 64-bit

extern "C" {

int mkdir_impl() {
    // TODO: Implementazione della syscall mkdir
    std::cout << "Syscall mkdir (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int mkdir_test() {
    // TODO: Test di base per mkdir
    std::cout << "Testing mkdir (64-bit)..." << std::endl;
    return mkdir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing mkdir ===" << std::endl;
    return mkdir_test();
}
#endif
