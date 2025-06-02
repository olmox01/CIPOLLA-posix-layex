# filepath: Makefile
# Makefile for x86_pathconf module

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -std=c99 -g
CXXFLAGS = -Wall -Wextra -std=c++17 -g
LDFLAGS = 

# Target files
MODULE = x86_pathconf
SOURCES = $(MODULE).cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = $(MODULE)
TEST_TARGET = test_$(MODULE)

# Default target
all: $(TARGET)

# Build main module
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -DSTANDALONE_BUILD -o $@ $^ $(LDFLAGS)

# Build test version
test: $(TEST_TARGET)

$(TEST_TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -DTEST_BUILD -o $@ $^ $(LDFLAGS)

# Object files
%.o: %.cpp $(MODULE).h
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean
clean:
	rm -f $(OBJECTS) $(TARGET) $(TEST_TARGET)

# Install (placeholder)
install:
	@echo "Install not implemented yet for $(MODULE)"

# Debug build
debug: CXXFLAGS += -DDEBUG -O0
debug: $(TARGET)

# Release build  
release: CXXFLAGS += -O2 -DNDEBUG
release: $(TARGET)

.PHONY: all test clean install debug release
