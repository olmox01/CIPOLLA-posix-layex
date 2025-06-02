// filepath: readdir.cpp
/**
 * POSIX Syscall Implementation: readdir
 * Architecture: 64-bit
 * Module: readdir
 */

#include "readdir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare readdir per architettura 64-bit

extern "C" {

int readdir_impl() {
    // TODO: Implementazione della syscall readdir
    std::cout << "Syscall readdir (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int readdir_test() {
    // TODO: Test di base per readdir
    std::cout << "Testing readdir (64-bit)..." << std::endl;
    return readdir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing readdir ===" << std::endl;
    return readdir_test();
}
#endif
