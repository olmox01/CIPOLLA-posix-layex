// filepath: times.cpp
/**
 * POSIX Syscall Implementation: times
 * Architecture: 64-bit
 * Module: times
 */

#include "times.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare times per architettura 64-bit

extern "C" {

int times_impl() {
    // TODO: Implementazione della syscall times
    std::cout << "Syscall times (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int times_test() {
    // TODO: Test di base per times
    std::cout << "Testing times (64-bit)..." << std::endl;
    return times_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing times ===" << std::endl;
    return times_test();
}
#endif
