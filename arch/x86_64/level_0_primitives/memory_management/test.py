#!/usr/bin/env python3
# filepath: test.py

"""
Test suite completa per Memory Manager - POSIX Memory Management Suite
"""

import subprocess
import sys
import os
from pathlib import Path

class MemoryManagerTest:
    def __init__(self):
        self.module_name = "memory_manager"
        self.test_executable = f"./{self.module_name}"
        self.modules = ["brk", "sbrk", "mmap", "munmap", "mprotect", "msync"]
        
    def compile_memory_manager(self):
        """Compila il memory manager"""
        print(f"🔨 Compilando {self.module_name}...")
        try:
            result = subprocess.run(["make", "clean"], capture_output=True, text=True)
            result = subprocess.run(["make", "all"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Errore compilazione: {result.stderr}")
                return False
            print(f"✅ Compilazione {self.module_name} completata")
            return True
        except Exception as e:
            print(f"❌ Errore durante compilazione: {e}")
            return False
    
    def run_memory_manager_test(self):
        """Esegue test completo del memory manager"""
        if not Path(self.test_executable).exists():
            print(f"❌ Eseguibile {self.test_executable} non trovato")
            return False
            
        print(f"🧪 Eseguendo test completo per {self.module_name}...")
        try:
            result = subprocess.run([self.test_executable], 
                                  capture_output=True, text=True, timeout=30)
            print(f"📋 Output: {result.stdout}")
            if result.stderr:
                print(f"⚠️  Stderr: {result.stderr}")
            
            # Verifiche specifiche per memory manager
            success_indicators = [
                "MEMORY MANAGER INITIALIZATION",
                "✅ All modules validated successfully!",
                "MEMORY MANAGER - COMPREHENSIVE TEST SUITE",
                "🎉 ALL TESTS PASSED! Memory management suite is fully functional."
            ]
            
            # Verifica che tutti i moduli siano testati
            module_tests = [
                "--- Testing Module: brk ---",
                "--- Testing Module: sbrk ---", 
                "--- Testing Module: mmap ---",
                "--- Testing Module: munmap ---",
                "--- Testing Module: mprotect ---",
                "--- Testing Module: msync ---"
            ]
            
            all_indicators = success_indicators + module_tests
            
            for indicator in all_indicators:
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
    
    def run_individual_module_tests(self):
        """Esegue i test dei singoli moduli"""
        print("🔬 Eseguendo test dei singoli moduli...")
        failed_modules = []
        
        for module in self.modules:
            print(f"\n🧪 Testing modulo: {module}")
            try:
                result = subprocess.run(
                    ["python3", "test.py"], 
                    cwd=f"{module}/",
                    capture_output=True, 
                    text=True, 
                    timeout=15
                )
                
                if result.returncode == 0:
                    print(f"✅ Modulo {module} - Test PASSED")
                else:
                    print(f"❌ Modulo {module} - Test FAILED")
                    print(f"   Output: {result.stdout}")
                    print(f"   Error: {result.stderr}")
                    failed_modules.append(module)
                    
            except Exception as e:
                print(f"❌ Errore durante test modulo {module}: {e}")
                failed_modules.append(module)
        
        if failed_modules:
            print(f"\n❌ Moduli falliti: {', '.join(failed_modules)}")
            return False
        else:
            print(f"\n✅ Tutti i moduli singoli hanno passato i test!")
            return True
    
    def run_all_tests(self):
        """Esegue tutti i test"""
        print(f"🚀 Avvio test completi per {self.module_name}")
        print("=" * 60)
        
        # Test 1: Compilazione memory manager
        if not self.compile_memory_manager():
            return False
            
        # Test 2: Test integrato memory manager
        if not self.run_memory_manager_test():
            print("❌ Test integrato memory manager fallito")
            return False
            
        # Test 3: Test singoli moduli
        if not self.run_individual_module_tests():
            print("❌ Test moduli singoli falliti")
            return False
            
        print("\n" + "=" * 60)
        print(f"🎉 TUTTI I TEST COMPLETATI CON SUCCESSO!")
        print(f"✅ Memory Manager integrato: FUNZIONANTE")
        print(f"✅ Moduli standalone: TUTTI FUNZIONANTI")
        print(f"✅ Sistema pronto per produzione!")
        return True

def main():
    """Funzione principale"""
    tester = MemoryManagerTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
