// filepath: write.cpp
/**
 * POSIX Syscall Implementation: write
 * Architecture: 64-bit
 * Module: write
 */

#include "write.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare write per architettura 64-bit

extern "C" {

int write_impl() {
    // TODO: Implementazione della syscall write
    std::cout << "Syscall write (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int write_test() {
    // TODO: Test di base per write
    std::cout << "Testing write (64-bit)..." << std::endl;
    return write_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing write ===" << std::endl;
    return write_test();
}
#endif
