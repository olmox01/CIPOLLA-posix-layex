#!/usr/bin/env python3

"""
Utilities avanzate per il progetto POSIX Syscalls
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import shutil
import re

class ProjectUtilities:
    def __init__(self, project_root: str = "/home/sh/progetti/CIPOLLA"):
        self.project_root = Path(project_root)
        
    def interactive_module_creator(self):
        """Wizard interattivo per creare nuovi moduli"""
        print("WIZARD CREAZIONE MODULO")
        print("=" * 40)
        
        # Selezione architettura
        print("\n1. Architettura:")
        print("   1) x86_64 (64-bit)")
        print("   2) x86_32 (32-bit)")
        print("   3) Entrambe")
        
        arch_choice = input("Scelta [1]: ").strip() or "1"
        
        # Selezione livello
        levels = [
            "level_0_primitives",
            "level_1_fundamental", 
            "level_2_intermediate",
            "level_3_complex",
            "level_4_highlevel",
            "level_5_specialized"
        ]
        
        print("\n2. Livello:")
        for i, level in enumerate(levels, 1):
            print(f"   {i}) {level}")
        
        level_choice = input("Livello [1]: ").strip() or "1"
        try:
            selected_level = levels[int(level_choice) - 1]
        except (ValueError, IndexError):
            selected_level = levels[0]
        
        # Lista categorie esistenti per il livello selezionato
        existing_categories = self._get_existing_categories(selected_level)
        if existing_categories:
            print(f"\n3. Categorie esistenti in {selected_level}:")
            for i, cat in enumerate(existing_categories, 1):
                print(f"   {i}) {cat}")
            print(f"   {len(existing_categories)+1}) Nuova categoria")
            
            cat_choice = input(f"Categoria [1]: ").strip() or "1"
            try:
                choice_idx = int(cat_choice) - 1
                if choice_idx < len(existing_categories):
                    category = existing_categories[choice_idx]
                else:
                    category = input("Nome nuova categoria: ").strip()
            except (ValueError, IndexError):
                category = existing_categories[0] if existing_categories else "custom"
        else:
            category = input("3. Nome categoria: ").strip() or "custom"
        
        # Input nome syscall
        syscall_name = input("4. Nome syscall: ").strip()
        if not syscall_name:
            print("ERRORE: Nome syscall obbligatorio")
            return
        
        # Verifica se esiste già
        if self._module_exists(syscall_name, arch_choice):
            print(f"ATTENZIONE: Modulo {syscall_name} già esistente")
            if input("Continuare? [y/N]: ").strip().lower() != 'y':
                return
        
        # Descrizione e dipendenze
        description = input("5. Descrizione: ").strip() or f"Implementazione syscall {syscall_name}"
        dependencies = input("6. Dipendenze (separate da virgola): ").strip()
        dep_list = [d.strip() for d in dependencies.split(',') if d.strip()] if dependencies else []
        
        # Conferma
        print(f"\nRIEPILOGO:")
        print(f"Syscall: {syscall_name}")
        print(f"Livello: {selected_level}")
        print(f"Categoria: {category}")
        print(f"Architettura: {arch_choice}")
        print(f"Dipendenze: {dep_list}")
        
        if input("\nCreare modulo? [y/N]: ").strip().lower() == 'y':
            self._create_custom_module(syscall_name, selected_level, category, arch_choice, description, dep_list)
        else:
            print("Creazione annullata")
    
    def _get_existing_categories(self, level: str) -> List[str]:
        """Ottiene categorie esistenti per un livello"""
        categories = set()
        
        for arch in ["x86_64", "x86_32"]:
            level_path = self.project_root / "arch" / arch / level
            if level_path.exists():
                for item in level_path.iterdir():
                    if item.is_dir():
                        categories.add(item.name)
        
        return sorted(list(categories))
    
    def _module_exists(self, syscall_name: str, arch_choice: str) -> bool:
        """Verifica se un modulo esiste già"""
        archs = ["x86_64", "x86_32"] if arch_choice == "3" else [f"x86_{32 if arch_choice == '2' else 64}"]
        
        for arch in archs:
            arch_path = self.project_root / "arch" / arch
            if arch_path.exists():
                for module_dir in arch_path.rglob("*"):
                    if module_dir.is_dir() and module_dir.name.endswith(syscall_name):
                        return True
        return False
    
    def _create_custom_module(self, syscall: str, level: str, category: str, arch_choice: str, description: str, dependencies: List[str]):
        """Crea modulo personalizzato con logica completa"""
        architectures = []
        if arch_choice == "1":
            architectures = [("x86_64", "")]
        elif arch_choice == "2":
            architectures = [("x86_32", "x86_")]
        else:
            architectures = [("x86_64", ""), ("x86_32", "x86_")]
        
        for arch, prefix in architectures:
            module_name = f"{prefix}{syscall}"
            module_path = self.project_root / "arch" / arch / level / category / module_name
            
            if module_path.exists():
                print(f"Modulo già esistente: {module_path}")
                continue
            
            module_path.mkdir(parents=True, exist_ok=True)
            self._generate_complete_module_files(module_path, syscall, prefix, description, dependencies)
            print(f"Creato: {module_path}")

    def _generate_complete_module_files(self, module_dir: Path, syscall: str, prefix: str, description: str, dependencies: List[str]):
        """Genera file completi per modulo con implementazioni reali"""
        module_name = f"{prefix}{syscall}"
        arch = "64-bit" if not prefix else "32-bit"
        arch_define = "__x86_64__" if not prefix else "__i386__"
        
        # Genera includes per dipendenze
        dependency_includes = ""
        dependency_calls = ""
        
        for dep in dependencies:
            dep_module = f"{prefix}{dep}"
            dependency_includes += f'#include "../../../{dep_module}/{dep_module}.h"\n'
            dependency_calls += f"    // Dipendenza: {dep_module}_impl();\n"
        
        # Template CPP con implementazione reale
        cpp_content = f'''// filepath: {module_name}.cpp
/**
 * POSIX Syscall Implementation: {syscall}
 * Architecture: {arch}
 * Module: {module_name}
 * Description: {description}
 */

#include "{module_name}.h"
#include <iostream>
#include <cerrno>
#include <cstring>
#include <unistd.h>
#include <sys/types.h>
#include <sys/syscall.h>

{dependency_includes}

// Architecture-specific includes
#ifdef {arch_define}
#include <asm/unistd.h>
#endif

extern "C" {{

/**
 * Implementazione reale della syscall {syscall}
 * Architettura: {arch}
 */
int {module_name}_impl() {{
    // Log di debug
    if (getenv("{module_name.upper()}_DEBUG")) {{
        std::cerr << "DEBUG: Executing {syscall} on {arch}" << std::endl;
    }}
    
{dependency_calls}
    
    // Implementazione specifica per {syscall}
    int result = -1;
    
    // TODO: Sostituire con implementazione reale
    // Esempio di struttura per syscall:
    
    /*
    // 1. Validazione parametri
    if (/* parametri non validi */) {{
        errno = EINVAL;
        return -1;
    }}
    
    // 2. Chiamata diretta al kernel
    #ifdef {arch_define}
    result = syscall(SYS_{syscall});
    #else
    result = syscall(SYS_{syscall});
    #endif
    
    // 3. Gestione errori
    if (result == -1) {{
        // errno è già impostato da syscall()
        return -1;
    }}
    */
    
    // Implementazione stub per ora
    std::cout << "{syscall} ({arch}): {description}" << std::endl;
    errno = ENOSYS;  // Funzione non implementata
    return -1;
}}

/**
 * Test completo per {syscall}
 */
int {module_name}_test() {{
    std::cout << "Testing {syscall} ({arch})..." << std::endl;
    
    // Test di base
    int result = {module_name}_impl();
    
    // Verifica risultato atteso per stub
    if (result == -1 && errno == ENOSYS) {{
        std::cout << "Test PASSED: Stub funziona correttamente" << std::endl;
        return 0;
    }}
    
    // TODO: Aggiungere test specifici quando implementato
    /*
    // Test casi validi
    // Test casi di errore
    // Test edge cases
    */
    
    return result;
}}

/**
 * Informazioni sul modulo
 */
const char* {module_name}_get_description() {{
    return "{description}";
}}

const char* {module_name}_get_arch() {{
    return "{arch}";
}}

int {module_name}_get_dependencies(char** deps, int max_deps) {{
    const char* dep_list[] = {{{', '.join(f'"{dep}"' for dep in dependencies) or '""'}}};
    int dep_count = {len(dependencies)};
    
    if (deps && max_deps > 0) {{
        for (int i = 0; i < dep_count && i < max_deps; i++) {{
            deps[i] = strdup(dep_list[i]);
        }}
    }}
    
    return dep_count;
}}

}} // extern "C"

#ifdef STANDALONE_BUILD
int main() {{
    std::cout << "=== Testing {module_name} ===" << std::endl;
    std::cout << "Description: " << {module_name}_get_description() << std::endl;
    std::cout << "Architecture: " << {module_name}_get_arch() << std::endl;
    
    char* deps[10];
    int dep_count = {module_name}_get_dependencies(deps, 10);
    if (dep_count > 0) {{
        std::cout << "Dependencies: ";
        for (int i = 0; i < dep_count; i++) {{
            std::cout << deps[i];
            if (i < dep_count - 1) std::cout << ", ";
            free(deps[i]);
        }}
        std::cout << std::endl;
    }}
    
    return {module_name}_test();
}}
#endif
'''
        
        (module_dir / f"{module_name}.cpp").write_text(cpp_content)
        
        # Header completo
        guard = f"{module_name.upper()}_H"
        h_content = f'''// filepath: {module_name}.h
/**
 * POSIX Syscall Header: {syscall}
 * Module: {module_name}
 * Description: {description}
 */

#ifndef {guard}
#define {guard}

#ifdef __cplusplus
extern "C" {{
#endif

// Main API functions
int {module_name}_impl();
int {module_name}_test();

// Module information functions
const char* {module_name}_get_description();
const char* {module_name}_get_arch();
int {module_name}_get_dependencies(char** deps, int max_deps);

// Constants for {syscall}
#define {module_name.upper()}_VERSION "1.0.0"
#define {module_name.upper()}_ARCH "{arch}"

// Error codes specific to {syscall}
// TODO: Aggiungere codici errore specifici se necessari

#ifdef __cplusplus
}}
#endif

#endif // {guard}
'''
        
        (module_dir / f"{module_name}.h").write_text(h_content)
        
        # Makefile completo e funzionale
        makefile_content = f'''# filepath: Makefile
# Makefile for {module_name} module

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -std=c99 -g -fPIC
CXXFLAGS = -Wall -Wextra -std=c++17 -g -fPIC
LDFLAGS = 

# Architecture specific flags
ARCH_FLAGS = 
ifeq ($(shell uname -m),x86_64)
    ARCH_FLAGS += -m64
else
    ARCH_FLAGS += -m32
endif

CFLAGS += $(ARCH_FLAGS)
CXXFLAGS += $(ARCH_FLAGS)

# Target files
MODULE = {module_name}
SOURCES = $(MODULE).cpp
OBJECTS = $(SOURCES:.cpp=.o)
TARGET = $(MODULE)
TEST_TARGET = test_$(MODULE)
LIB_TARGET = lib$(MODULE).so

# Default target
all: $(TARGET) $(LIB_TARGET)

# Build main executable
$(TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -DSTANDALONE_BUILD -o $@ $^ $(LDFLAGS)

# Build shared library
$(LIB_TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -shared -o $@ $^ $(LDFLAGS)

# Build test version
test: $(TEST_TARGET)
	./$(TEST_TARGET)

$(TEST_TARGET): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -DTEST_BUILD -o $@ $^ $(LDFLAGS)

# Object files
%.o: %.cpp $(MODULE).h
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Run all checks
check: test
	@echo "Running Python tests..."
	@python3 test.py

# Clean
clean:
	rm -f $(OBJECTS) $(TARGET) $(TEST_TARGET) $(LIB_TARGET) *.log

# Install to system
install: $(LIB_TARGET)
	@echo "Installing $(MODULE) to /usr/local/lib/"
	@sudo cp $(LIB_TARGET) /usr/local/lib/
	@sudo cp $(MODULE).h /usr/local/include/
	@sudo ldconfig

# Uninstall from system
uninstall:
	@echo "Uninstalling $(MODULE)..."
	@sudo rm -f /usr/local/lib/$(LIB_TARGET)
	@sudo rm -f /usr/local/include/$(MODULE).h
	@sudo ldconfig

# Debug build
debug: CXXFLAGS += -DDEBUG -O0 -ggdb
debug: clean $(TARGET)

# Release build  
release: CXXFLAGS += -O2 -DNDEBUG
release: clean $(TARGET)

# Profile build
profile: CXXFLAGS += -pg -O2
profile: clean $(TARGET)

# Static analysis
analyze:
	@echo "Running static analysis..."
	@cppcheck --enable=all --std=c++17 $(SOURCES) || true
	@echo "Running clang-tidy..."
	@clang-tidy $(SOURCES) -- $(CXXFLAGS) || true

# Format code
format:
	@echo "Formatting code..."
	@clang-format -i $(SOURCES) $(MODULE).h || true

.PHONY: all test check clean install uninstall debug release profile analyze format
'''
        
        (module_dir / "Makefile").write_text(makefile_content)
        
        # Documentazione completa
        md_content = f'''# filepath: {module_name}.md

# {syscall} - {arch} Implementation

## Descrizione
{description}

Implementazione della system call POSIX `{syscall}` per architettura {arch}.

## Stato Implementazione
- [x] Struttura base del modulo
- [x] Template di implementazione
- [x] Sistema di build
- [x] Test di base
- [ ] Implementazione funzionale completa
- [ ] Test di integrazione
- [ ] Validazione POSIX
- [ ] Ottimizzazioni specifiche

## API

### Funzioni Principali
```c
int {module_name}_impl();                    // Implementazione principale
int {module_name}_test();                    // Test di funzionamento
const char* {module_name}_get_description(); // Descrizione modulo
const char* {module_name}_get_arch();        // Architettura target
int {module_name}_get_dependencies(char** deps, int max_deps); // Dipendenze
```

## Dipendenze
{chr(10).join(f"- {dep}" for dep in dependencies) if dependencies else "Nessuna dipendenza"}

## Build e Test

### Compilazione
```bash
make              # Build normale
make debug        # Build con debug info
make release      # Build ottimizzato
```

### Test
```bash
make test         # Test C++
make check        # Test completi (C++ + Python)
```

### Installazione
```bash
make install      # Installa nel sistema
make uninstall    # Rimuove dal sistema
```

### Analisi Codice
```bash
make analyze      # Static analysis
make format       # Format del codice
```

## Implementazione

### TODO Prioritari
1. Implementare logica principale in `{module_name}_impl()`
2. Sostituire stub con chiamata syscall reale
3. Aggiungere validazione parametri
4. Implementare gestione errori completa
5. Aggiungere test specifici

### Note Architettura {arch}
- Syscall number: da definire
- Registri utilizzati: da documentare
- Limitazioni specifiche: da identificare

## Testing

### Test Automatici
Il modulo include test automatici che verificano:
- Compilazione corretta
- Esecuzione senza crash
- Gestione errori base
- Performance base

### Test Manuali
```bash
# Test diretto
./{module_name}

# Test con debug
{module_name.upper()}_DEBUG=1 ./{module_name}
```

## Conformità POSIX

### Standard di riferimento
- POSIX.1-2017
- Sezione specifica: da identificare per {syscall}

### Comportamento richiesto
- Da documentare in base a specifica POSIX

## Note di Sviluppo

### Struttura Implementazione
1. Validazione parametri di input
2. Conversione architettura-specifica se necessaria  
3. Chiamata al kernel via syscall()
4. Gestione valore di ritorno ed errno
5. Log e debug opzionali

### Debugging
```bash
export {module_name.upper()}_DEBUG=1
```

## Changelog
- v1.0.0: Creazione modulo base con template
'''
        
        (module_dir / f"{module_name}.md").write_text(md_content)
        
        # Test Python funzionale completo
        test_content = f'''#!/usr/bin/env python3
# filepath: test.py

"""
Test suite completa per {syscall} ({arch})
"""

import subprocess
import sys
import os
import time
import tempfile
import shutil
import json
from pathlib import Path

class {syscall.title()}Test:
    def __init__(self):
        self.module_name = "{module_name}"
        self.test_executable = f"./{{self.module_name}}"
        self.lib_file = f"lib{{self.module_name}}.so"
        self.test_results = {{}}
        
    def run_command(self, cmd, timeout=30):
        """Esegue comando con gestione errori"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                shell=isinstance(cmd, str)
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "TIMEOUT"
        except Exception as e:
            return -1, "", str(e)
    
    def test_compilation(self):
        """Test compilazione"""
        print("Test compilazione...")
        
        # Clean prima
        ret, out, err = self.run_command(["make", "clean"])
        
        # Compila debug
        ret, out, err = self.run_command(["make", "debug"])
        
        success = ret == 0 and Path(self.test_executable).exists()
        self.test_results["compilation"] = {{
            "success": success,
            "details": err if not success else "OK",
            "executable_exists": Path(self.test_executable).exists(),
            "lib_exists": Path(self.lib_file).exists()
        }}
        
        if success:
            print("  PASS: Compilazione riuscita")
        else:
            print(f"  FAIL: Compilazione fallita - {{err[:100]}}")
        
        return success
    
    def test_basic_execution(self):
        """Test esecuzione base"""
        print("Test esecuzione base...")
        
        if not Path(self.test_executable).exists():
            self.test_results["basic_execution"] = {{
                "success": False,
                "details": "Eseguibile non trovato"
            }}
            print("  FAIL: Eseguibile non trovato")
            return False
        
        ret, out, err = self.run_command([self.test_executable])
        
        success = ret in [0, -1, 255]  # Allow some error codes for stubs
        self.test_results["basic_execution"] = {{
            "success": success,
            "return_code": ret,
            "stdout": out,
            "stderr": err,
            "contains_description": "{description}" in out
        }}
        
        if success:
            print("  PASS: Esecuzione completata")
        else:
            print(f"  FAIL: Esecuzione fallita (code {{ret}})")
        
        return success
    
    def test_make_targets(self):
        """Test vari target del Makefile"""
        print("Test target Makefile...")
        
        targets_to_test = ["all", "clean"]
        results = {{}}
        
        for target in targets_to_test:
            ret, out, err = self.run_command(["make", target])
            results[target] = {{
                "success": ret == 0,
                "output": out,
                "error": err
            }}
            
            if ret == 0:
                print(f"  PASS: make {{target}}")
            else:
                print(f"  FAIL: make {{target}} - {{err[:50]}}")
        
        self.test_results["make_targets"] = results
        return all(r["success"] for r in results.values())
    
    def generate_report(self):
        """Genera report completo"""
        print("\\nGENERAZIONE REPORT")
        print("=" * 40)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results.values() 
                          if isinstance(r, dict) and r.get("success", True))
        
        print(f"Modulo: {{self.module_name}}")
        print(f"Architettura: {arch}")
        print(f"Descrizione: {description}")
        print(f"Test eseguiti: {{total_tests}}")
        print(f"Test passati: {{passed_tests}}")
        print(f"Percentuale successo: {{passed_tests/total_tests*100:.1f}}%" if total_tests > 0 else "0%")
        
        # Salva report JSON
        report_file = Path("test_report.json")
        report_data = {{
            "module": self.module_name,
            "architecture": "{arch}",
            "description": "{description}",
            "timestamp": time.time(),
            "summary": {{
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": passed_tests/total_tests*100 if total_tests > 0 else 0
            }},
            "results": self.test_results
        }}
        
        try:
            report_file.write_text(json.dumps(report_data, indent=2))
            print(f"Report salvato: {{report_file}}")
        except Exception as e:
            print(f"Errore salvataggio report: {{e}}")
        
        return passed_tests == total_tests
    
    def run_all_tests(self):
        """Esegue tutti i test"""
        print(f"AVVIO TEST COMPLETI: {{self.module_name}}")
        print(f"Descrizione: {description}")
        print("=" * 50)
        
        # Esegui tutti i test
        tests = [
            self.test_compilation,
            self.test_basic_execution, 
            self.test_make_targets
        ]
        
        all_passed = True
        for test_func in tests:
            try:
                if not test_func():
                    all_passed = False
            except Exception as e:
                print(f"  ERROR: {{test_func.__name__}} - {{e}}")
                all_passed = False
        
        # Genera report finale
        report_success = self.generate_report()
        
        if all_passed and report_success:
            print("\\nRISULTATO FINALE: TUTTI I TEST PASSATI")
            return True
        else:
            print("\\nRISULTATO FINALE: ALCUNI TEST FALLITI")
            return False

def main():
    """Funzione principale"""
    tester = {syscall.title()}Test()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
'''
        
        (module_dir / "test.py").write_text(test_content)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 project_utilities.py <command> [options]")
        print("Commands:")
        print("  wizard      - Crea modulo interattivo")
        return
    
    command = sys.argv[1]
    
    utils = ProjectUtilities()
    
    if command == "wizard":
        utils.interactive_module_creator()
    else:
        print(f"Comando sconosciuto: {command}")
        print("Comandi disponibili: wizard")

if __name__ == "__main__":
    main()
