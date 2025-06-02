// filepath: x86_readdir.cpp
/**
 * POSIX Syscall Implementation: readdir
 * Architecture: 32-bit
 * Module: x86_readdir
 */

#include "x86_readdir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare readdir per architettura 32-bit

extern "C" {

int x86_readdir_impl() {
    // TODO: Implementazione della syscall readdir
    std::cout << "Syscall readdir (32-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int x86_readdir_test() {
    // TODO: Test di base per readdir
    std::cout << "Testing readdir (32-bit)..." << std::endl;
    return x86_readdir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing x86_readdir ===" << std::endl;
    return x86_readdir_test();
}
#endif
