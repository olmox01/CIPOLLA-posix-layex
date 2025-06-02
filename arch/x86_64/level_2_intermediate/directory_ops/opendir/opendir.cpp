// filepath: opendir.cpp
/**
 * POSIX Syscall Implementation: opendir
 * Architecture: 64-bit
 * Module: opendir
 */

#include "opendir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare opendir per architettura 64-bit

extern "C" {

int opendir_impl() {
    // TODO: Implementazione della syscall opendir
    std::cout << "Syscall opendir (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int opendir_test() {
    // TODO: Test di base per opendir
    std::cout << "Testing opendir (64-bit)..." << std::endl;
    return opendir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing opendir ===" << std::endl;
    return opendir_test();
}
#endif
