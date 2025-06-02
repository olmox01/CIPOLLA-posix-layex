// filepath: x86_telldir.cpp
/**
 * POSIX Syscall Implementation: telldir
 * Architecture: 32-bit
 * Module: x86_telldir
 */

#include "x86_telldir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare telldir per architettura 32-bit

extern "C" {

int x86_telldir_impl() {
    // TODO: Implementazione della syscall telldir
    std::cout << "Syscall telldir (32-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int x86_telldir_test() {
    // TODO: Test di base per telldir
    std::cout << "Testing telldir (32-bit)..." << std::endl;
    return x86_telldir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing x86_telldir ===" << std::endl;
    return x86_telldir_test();
}
#endif
