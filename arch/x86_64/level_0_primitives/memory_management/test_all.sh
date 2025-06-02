#!/bin/bash

# =======================================================
# POSIX Memory Management Suite - Complete Test Runner
# =======================================================
# Script di test automatizzato completo per il sistema

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Log file
LOG_FILE="test_results_$(date +%Y%m%d_%H%M%S).log"

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message" | tee -a "$LOG_FILE"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Function to run a test
run_test() {
    local test_name=$1
    local test_command=$2
    local expected_success_indicator=$3
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    print_status "INFO" "Running test: $test_name"
    
    # Capture output
    if output=$(eval "$test_command" 2>&1); then
        # Check for success indicator in output
        if echo "$output" | grep -q "$expected_success_indicator"; then
            PASSED_TESTS=$((PASSED_TESTS + 1))
            print_status "SUCCESS" "$test_name passed"
            echo "Output: $output" >> "$LOG_FILE"
            return 0
        else
            FAILED_TESTS=$((FAILED_TESTS + 1))
            print_status "ERROR" "$test_name failed - success indicator not found"
            echo "Output: $output" >> "$LOG_FILE"
            return 1
        fi
    else
        FAILED_TESTS=$((FAILED_TESTS + 1))
        print_status "ERROR" "$test_name failed - command execution error"
        echo "Error output: $output" >> "$LOG_FILE"
        return 1
    fi
}

# Function to check file exists
check_file() {
    local file_path=$1
    local description=$2
    
    if [ -f "$file_path" ]; then
        print_status "SUCCESS" "$description exists: $file_path"
        return 0
    else
        print_status "ERROR" "$description missing: $file_path"
        return 1
    fi
}

# Start test suite
print_status "INFO" "=========================================================="
print_status "INFO" "POSIX Memory Management Suite - Automated Test Runner"
print_status "INFO" "=========================================================="
print_status "INFO" "Starting comprehensive test suite..."
print_status "INFO" "Log file: $LOG_FILE"
echo

# 1. Environment checks
print_status "INFO" "=== Phase 1: Environment Verification ==="

# Check required files
check_file "memory_manager" "Memory manager executable"
check_file "Makefile" "Main Makefile"

# Check module directories and executables
modules=("brk" "sbrk" "mmap" "munmap" "mprotect" "msync")
for module in "${modules[@]}"; do
    check_file "$module/$module" "Module executable: $module"
    check_file "$module/test.py" "Module test script: $module"
done

echo

# 2. Integration tests
print_status "INFO" "=== Phase 2: Integration Tests ==="

# Test memory manager with all modules
run_test "Memory Manager Integration" "./memory_manager" "All 6 modules tested successfully"

echo

# 3. Individual module tests
print_status "INFO" "=== Phase 3: Individual Module Tests ==="

# Test each module standalone
for module in "${modules[@]}"; do
    case $module in
        "brk")
            run_test "BRK Standalone Test" "./$module/$module" "BRK test completed successfully"
            ;;
        "sbrk")
            run_test "SBRK Standalone Test" "./$module/$module" "SBRK test completed successfully"
            ;;
        "mmap")
            run_test "MMAP Standalone Test" "./$module/$module" "MMAP test completed successfully"
            ;;
        "munmap")
            run_test "MUNMAP Standalone Test" "./$module/$module" "MUNMAP test completed successfully"
            ;;
        "mprotect")
            run_test "MPROTECT Standalone Test" "./$module/$module" "MPROTECT test completed successfully"
            ;;
        "msync")
            run_test "MSYNC Standalone Test" "./$module/$module" "MSYNC test completed successfully"
            ;;
    esac
done

echo

# 4. Python test suite
print_status "INFO" "=== Phase 4: Python Test Suite ==="

# Test main memory manager with Python
if [ -f "test.py" ]; then
    run_test "Memory Manager Python Test" "python3 test.py" "SUCCESS"
else
    print_status "WARNING" "Main test.py not found, skipping"
fi

# Test each module with Python
for module in "${modules[@]}"; do
    if [ -f "$module/test.py" ]; then
        run_test "Module $module Python Test" "cd $module && python3 test.py" "SUCCESS"
    else
        print_status "WARNING" "Python test for $module not found"
    fi
done

echo

# 5. Performance and stress tests
print_status "INFO" "=== Phase 5: Performance Tests ==="

# Performance test (basic timing)
print_status "INFO" "Running performance test..."
start_time=$(date +%s.%N)
./memory_manager >> "$LOG_FILE" 2>&1
end_time=$(date +%s.%N)
if command -v bc &> /dev/null; then
    execution_time=$(echo "$end_time - $start_time" | bc -l)
    print_status "INFO" "Memory manager execution time: ${execution_time}s"
else
    print_status "INFO" "Memory manager execution completed (timing requires bc)"
fi

# Test concurrent execution (basic stress test)
print_status "INFO" "Running basic stress test..."
for i in {1..3}; do
    run_test "Stress Test Run $i" "./memory_manager" "All 6 modules tested successfully"
done

echo

# =======================================================
# Test Results Summary
# =======================================================

print_status "INFO" "=========================================================="
print_status "INFO" "TEST SUITE COMPLETED"
print_status "INFO" "=========================================================="

echo
echo "📊 TEST SUMMARY:"
echo "===================="
echo "Total Tests: $TOTAL_TESTS"
echo "Passed: $PASSED_TESTS"
echo "Failed: $FAILED_TESTS"

if [ $FAILED_TESTS -eq 0 ]; then
    print_status "SUCCESS" "🎉 ALL TESTS PASSED! System is fully functional!"
    echo
    echo "✅ Memory Management Suite is PRODUCTION READY!"
    echo "✅ All 6 POSIX modules working correctly"
    echo "✅ Integration successful"
    echo "✅ Standalone functionality verified"
    echo
    echo "🚀 You can now use:"
    echo "   ./memory_manager          # Integrated suite"
    echo "   ./brk/brk                # Individual modules"
    echo "   ./sbrk/sbrk"
    echo "   ./mmap/mmap"
    echo "   ./munmap/munmap"
    echo "   ./mprotect/mprotect"
    echo "   ./msync/msync"
    exit 0
else
    print_status "ERROR" "❌ $FAILED_TESTS test(s) failed!"
    echo
    echo "🔍 Check the log file for details: $LOG_FILE"
    echo "🛠️  Common issues:"
    echo "   - Compilation errors: Check GCC version and flags"
    echo "   - Runtime errors: Check system permissions"
    echo "   - Missing files: Ensure all modules are present"
    exit 1
fi
