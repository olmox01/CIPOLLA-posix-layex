// filepath: rmdir.cpp
/**
 * POSIX Syscall Implementation: rmdir
 * Architecture: 64-bit
 * Module: rmdir
 */

#include "rmdir.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare rmdir per architettura 64-bit

extern "C" {

int rmdir_impl() {
    // TODO: Implementazione della syscall rmdir
    std::cout << "Syscall rmdir (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int rmdir_test() {
    // TODO: Test di base per rmdir
    std::cout << "Testing rmdir (64-bit)..." << std::endl;
    return rmdir_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing rmdir ===" << std::endl;
    return rmdir_test();
}
#endif
