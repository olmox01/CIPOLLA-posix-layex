// filepath: sigaction.cpp
/**
 * POSIX Syscall Implementation: sigaction
 * Architecture: 64-bit
 * Module: sigaction
 */

#include "sigaction.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare sigaction per architettura 64-bit

extern "C" {

int sigaction_impl() {
    // TODO: Implementazione della syscall sigaction
    std::cout << "Syscall sigaction (64-bit) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}

int sigaction_test() {
    // TODO: Test di base per sigaction
    std::cout << "Testing sigaction (64-bit)..." << std::endl;
    return sigaction_impl();
}

} // extern "C"

#ifdef STANDALONE_BUILD
int main() {
    std::cout << "=== Testing sigaction ===" << std::endl;
    return sigaction_test();
}
#endif
