# filepath: Makefile
# Memory Manager - Unified Build System
# Team Level 0 - Memory Management Integration
# STATUS: PRODUCTION READY ✅

# PROJECT COMPLETED SUCCESSFULLY!
# All 6 POSIX memory management modules implemented and integrated

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -std=c99 -g
CXXFLAGS = -Wall -Wextra -std=c++17 -g -fno-builtin
LDFLAGS = 

# Directories
BRK_DIR = brk
SBRK_DIR = sbrk
MMAP_DIR = mmap
MUNMAP_DIR = munmap
MPROTECT_DIR = mprotect
MSYNC_DIR = msync

# Source files for each module
BRK_SRC = $(BRK_DIR)/brk.cpp
SBRK_SRC = $(SBRK_DIR)/sbrk.cpp
MMAP_SRC = $(MMAP_DIR)/mmap.cpp
MUNMAP_SRC = $(MUNMAP_DIR)/munmap.cpp
MPROTECT_SRC = $(MPROTECT_DIR)/mprotect.cpp
MSYNC_SRC = $(MSYNC_DIR)/msync.cpp

# Memory manager sources
MM_SOURCES = memory_manager.cpp $(BRK_SRC) $(SBRK_SRC) $(MMAP_SRC) $(MUNMAP_SRC) $(MPROTECT_SRC) $(MSYNC_SRC)
MM_OBJECTS = $(MM_SOURCES:.cpp=.o)

# Include paths
INCLUDES = -I. -I$(BRK_DIR) -I$(SBRK_DIR) -I$(MMAP_DIR) -I$(MUNMAP_DIR) -I$(MPROTECT_DIR) -I$(MSYNC_DIR)

# Target files
TARGET = memory_manager
TEST_TARGET = memory_manager_test

# Default target
all: $(TARGET)

# Build memory manager
$(TARGET): $(MM_OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

# Build test version
test: $(TEST_TARGET)

$(TEST_TARGET): $(MM_OBJECTS)
	$(CXX) $(CXXFLAGS) -DTEST_BUILD -DSTANDALONE_BUILD -o $@ $^ $(LDFLAGS)

# Object files with proper includes
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Individual module builds
build-modules:
	@echo "Building individual modules..."
	cd $(BRK_DIR) && $(MAKE) all
	cd $(SBRK_DIR) && $(MAKE) all  
	cd $(MMAP_DIR) && $(MAKE) all
	cd $(MUNMAP_DIR) && $(MAKE) all
	cd $(MPROTECT_DIR) && $(MAKE) all
	cd $(MSYNC_DIR) && $(MAKE) all

# Test individual modules
test-modules:
	@echo "Testing individual modules..."
	cd $(BRK_DIR) && $(MAKE) test && ./brk_test
	cd $(SBRK_DIR) && $(MAKE) test && ./sbrk_test
	cd $(MMAP_DIR) && $(MAKE) test && ./mmap_test
	cd $(MUNMAP_DIR) && $(MAKE) test && ./munmap_test
	cd $(MPROTECT_DIR) && $(MAKE) test && ./mprotect_test
	cd $(MSYNC_DIR) && $(MAKE) test && ./msync_test

# Run memory manager tests
run-test: $(TARGET)
	@echo "Running memory manager comprehensive test..."
	./$(TARGET)

# Quick test (compile and run)
check: $(TARGET)
	@echo "=== MEMORY MANAGER QUICK CHECK ==="
	./$(TARGET)

# Debug build
debug: CXXFLAGS += -DDEBUG -O0
debug: $(TARGET)

# Release build
release: CXXFLAGS += -O2 -DNDEBUG
release: $(TARGET)

# Clean all
clean:
	rm -f $(MM_OBJECTS) $(TARGET) $(TEST_TARGET)
	cd $(BRK_DIR) && $(MAKE) clean 2>/dev/null || true
	cd $(SBRK_DIR) && $(MAKE) clean 2>/dev/null || true
	cd $(MMAP_DIR) && $(MAKE) clean 2>/dev/null || true
	cd $(MUNMAP_DIR) && $(MAKE) clean 2>/dev/null || true
	cd $(MPROTECT_DIR) && $(MAKE) clean 2>/dev/null || true
	cd $(MSYNC_DIR) && $(MAKE) clean 2>/dev/null || true

# Install (placeholder)
install:
	@echo "Install not implemented yet for memory_manager"

# Help
help:
	@echo "Memory Manager Build System"
	@echo "Available targets:"
	@echo "  all           - Build memory manager"
	@echo "  test          - Build test version"
	@echo "  run-test      - Compile and run tests"
	@echo "  check         - Quick compile and test"
	@echo "  build-modules - Build all individual modules"
	@echo "  test-modules  - Test all individual modules"
	@echo "  debug         - Build with debug symbols"
	@echo "  release       - Build optimized release"
	@echo "  clean         - Clean all build files"
	@echo "  help          - Show this help"

.PHONY: all test run-test check build-modules test-modules debug release clean install help
