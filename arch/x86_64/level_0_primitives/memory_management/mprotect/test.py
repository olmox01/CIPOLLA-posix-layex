#!/usr/bin/env python3
# filepath: test.py

"""
Test suite per mprotect (architettura)
"""

import subprocess
import sys
import os
from pathlib import Path

class MprotectTest:
    def __init__(self):
        self.module_name = "mprotect"
        self.test_executable = f"./{self.module_name}"
        
    def compile_module(self):
        """Compila il modulo"""
        print(f"🔨 Compilando {self.module_name}...")
        try:
            result = subprocess.run(["make", "clean"], capture_output=True, text=True)
            result = subprocess.run(["make", "debug"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Errore compilazione: {result.stderr}")
                return False
            print(f"✅ Compilazione {self.module_name} completata")
            return True
        except Exception as e:
            print(f"❌ Errore durante compilazione: {e}")
            return False
    
    def run_basic_test(self):
        """Esegue test di base"""
        if not Path(self.test_executable).exists():
            print(f"❌ Eseguibile {self.test_executable} non trovato")
            return False
            
        print(f"🧪 Eseguendo test di base per {self.module_name}...")
        try:
            result = subprocess.run([self.test_executable], 
                                  capture_output=True, text=True, timeout=10)
            print(f"📋 Output: {result.stdout}")
            if result.stderr:
                print(f"⚠️  Stderr: {result.stderr}")
            
            # Verifiche specifiche per mprotect
            success_indicators = [
                "Test 1: Successfully changed protection to read-only ✓",
                "Test 2: Correctly rejected NULL pointer ✓", 
                "Test 3: Correctly rejected zero length ✓",
                "=== All mprotect tests passed! ==="
            ]
            
            for indicator in success_indicators:
                if indicator not in result.stdout:
                    print(f"❌ Test fallito: manca '{indicator}'")
                    return False
                    
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout durante test di {self.module_name}")
            return False
        except Exception as e:
            print(f"❌ Errore durante test: {e}")
            return False
    
    def run_all_tests(self):
        """Esegue tutti i test"""
        print(f"🚀 Avvio test completi per {self.module_name}")
        
        if not self.compile_module():
            return False
            
        if not self.run_basic_test():
            return False
            
        print(f"✅ Tutti i test per {self.module_name} completati con successo")
        return True

def main():
    """Funzione principale"""
    tester = MprotectTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
