#!/usr/bin/env python3

import os
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class POSIXSyscallManager:
    def __init__(self, base_dir: str = "/home/sh/progetti/CIPOLLA"):
        self.base_dir = Path(base_dir)
        self.syscalls_data = self._load_syscalls_data()
        
    def _load_syscalls_data(self) -> Dict:
        """Carica i dati delle syscall dalla mappa JSON"""
        return {
            "level_0_primitives": {
                "memory_management": ["brk", "sbrk", "mmap", "munmap", "mprotect", "msync"],
                "process_identity": ["getpid", "getppid", "getuid", "geteuid", "getgid", "getegid"],
                "basic_io": ["read", "write", "open", "close", "lseek"]
            },
            "level_1_fundamental": {
                "filesystem_ops": ["stat", "fstat", "lstat", "access", "chmod", "chown", "link", "unlink", "rename", "mkdir", "rmdir"],
                "process_control": ["fork", "execve", "wait", "waitpid", "exit", "kill"],
                "signal_handling": ["signal", "sigaction", "pause", "alarm"]
            },
            "level_2_intermediate": {
                "advanced_io": ["dup", "dup2", "pipe", "fcntl", "ioctl", "select", "poll"],
                "directory_ops": ["opendir", "readdir", "closedir", "rewinddir", "seekdir", "telldir"],
                "time_ops": ["time", "gettimeofday", "clock", "sleep", "nanosleep"]
            },
            "level_3_complex": {
                "ipc_sysv": ["msgget", "msgsnd", "msgrcv", "msgctl", "semget", "semop", "semctl", "shmget", "shmat", "shmdt", "shmctl"],
                "networking": ["socket", "bind", "listen", "accept", "connect", "send", "recv", "sendto", "recvfrom", "shutdown"],
                "session_control": ["setsid", "getsid", "setpgid", "getpgid", "getpgrp"]
            },
            "level_4_highlevel": {
                "security": ["setuid", "setgid", "seteuid", "setegid", "getgroups", "setgroups"],
                "filesystem_advanced": ["mount", "umount", "sync", "fsync", "fdatasync", "truncate", "ftruncate"],
                "resource_control": ["getrlimit", "setrlimit", "getrusage", "times"]
            },
            "level_5_specialized": {
                "configuration": ["pathconf", "fpathconf", "sysconf", "confstr"],
                "async_io": ["aio_read", "aio_write", "aio_error", "aio_return", "aio_cancel", "aio_suspend"],
                "posix_threads": ["pthread_create", "pthread_join", "pthread_detach", "pthread_exit", "pthread_mutex_init", "pthread_mutex_lock"]
            }
        }
    
    def create_project_structure(self):
        """Crea la struttura completa del progetto"""
        print("🏗️  Creando struttura del progetto POSIX Syscalls...")
        
        # Crea directories principali
        dirs_to_create = [
            "arch/x86_64",
            "arch/x86_32", 
            "patches",
            "tools",
            "docs",
            "tests/integration"
        ]
        
        for dir_path in dirs_to_create:
            full_path = self.base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Creata directory: {dir_path}")
        
        # Crea moduli per ogni architettura
        self._create_arch_modules("arch/x86_64", "")
        self._create_arch_modules("arch/x86_32", "x86_")
        
        # Crea file di configurazione
        self._create_config_files()
        
        print("✅ Struttura del progetto creata con successo!")
    
    def _create_arch_modules(self, arch_dir: str, prefix: str):
        """Crea moduli per una specifica architettura"""
        arch_path = self.base_dir / arch_dir
        
        for level, categories in self.syscalls_data.items():
            level_dir = arch_path / level
            level_dir.mkdir(exist_ok=True)
            
            for category, syscalls in categories.items():
                category_dir = level_dir / category
                category_dir.mkdir(exist_ok=True)
                
                for syscall in syscalls:
                    module_name = f"{prefix}{syscall}"
                    module_dir = category_dir / module_name
                    
                    if not module_dir.exists():
                        module_dir.mkdir(exist_ok=True)
                        self._create_module_files(module_dir, syscall, prefix)
                        print(f"📦 Creato modulo: {arch_dir}/{level}/{category}/{module_name}")
    
    def _create_module_files(self, module_dir: Path, syscall: str, prefix: str):
        """Crea i file template per un modulo"""
        module_name = f"{prefix}{syscall}"
        
        # File CPP
        cpp_content = self._generate_cpp_template(syscall, prefix)
        (module_dir / f"{module_name}.cpp").write_text(cpp_content)
        
        # File Header
        h_content = self._generate_header_template(syscall, prefix)
        (module_dir / f"{module_name}.h").write_text(h_content)
        
        # Makefile
        make_content = self._generate_makefile_template(module_name)
        (module_dir / "Makefile").write_text(make_content)
        
        # Documentation
        md_content = self._generate_doc_template(syscall, prefix)
        (module_dir / f"{module_name}.md").write_text(md_content)
        
        # Test Python
        test_content = self._generate_test_template(syscall, prefix)
        (module_dir / "test.py").write_text(test_content)
    
    def _generate_cpp_template(self, syscall: str, prefix: str) -> str:
        """Genera template CPP per syscall"""
        module_name = f"{prefix}{syscall}"
        arch = "64-bit" if not prefix else "32-bit"
        
        return f'''// filepath: {module_name}.cpp
/**
 * POSIX Syscall Implementation: {syscall}
 * Architecture: {arch}
 * Module: {module_name}
 */

#include "{module_name}.h"
#include <iostream>
#include <cerrno>
#include <cstring>

// TODO: Implementare {syscall} per architettura {arch}

extern "C" {{

int {module_name}_impl() {{
    // TODO: Implementazione della syscall {syscall}
    std::cout << "Syscall {syscall} ({arch}) - Not implemented yet" << std::endl;
    errno = ENOSYS;
    return -1;
}}

int {module_name}_test() {{
    // TODO: Test di base per {syscall}
    std::cout << "Testing {syscall} ({arch})..." << std::endl;
    return {module_name}_impl();
}}

}} // extern "C"

#ifdef STANDALONE_BUILD
int main() {{
    std::cout << "=== Testing {module_name} ===" << std::endl;
    return {module_name}_test();
}}
#endif
'''

    def _generate_header_template(self, syscall: str, prefix: str) -> str:
        """Genera template header per syscall"""
        module_name = f"{prefix}{syscall}"
        guard = f"{module_name.upper()}_H"
        
        return f'''// filepath: {module_name}.h
/**
 * POSIX Syscall Header: {syscall}
 * Module: {module_name}
 */

#ifndef {guard}
#define {guard}

#ifdef __cplusplus
extern "C" {{
#endif

// Function prototypes
int {module_name}_impl();
int {module_name}_test();

// Constants and definitions for {syscall}
// TODO: Aggiungere definizioni specifiche

#ifdef __cplusplus
}}
#endif

#endif // {guard}
'''

    def _generate_makefile_template(self, module_name: str) -> str:
        """Genera Makefile per modulo"""
        return f'''# filepath: Makefile
# Makefile for {module_name} module

CC = gcc
CXX = g++
CFLAGS = -Wall -Wextra -std=c99 -g
CXXFLAGS = -Wall -Wextra -std=c++17 -g
LDFLAGS = 

# Target files
MODULE = {module_name}
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
'''

    def _generate_doc_template(self, syscall: str, prefix: str) -> str:
        """Genera documentazione template"""
        module_name = f"{prefix}{syscall}"
        arch = "64-bit" if not prefix else "32-bit"
        
        return f'''# filepath: {module_name}.md

# {syscall} - {arch} Implementation

## Descrizione
Implementazione della system call POSIX `{syscall}` per architettura {arch}.

## Stato Implementazione
- [ ] Implementazione base
- [ ] Gestione errori
- [ ] Test unitari
- [ ] Documentazione completa
- [ ] Ottimizzazioni specifiche

## Interfaccia

### Funzioni Esportate
- `{module_name}_impl()` - Implementazione principale
- `{module_name}_test()` - Test di funzionamento

## Dipendenze
TODO: Elencare dipendenze da altre syscall

## Note di Implementazione
TODO: Note specifiche per l'implementazione {arch}

## Test
```bash
make test
./{module_name}
```

## Build
```bash
make              # Build normale
make debug        # Build con debug
make release      # Build ottimizzato
```

## TODO
- [ ] Implementare funzionalità core
- [ ] Aggiungere test completi
- [ ] Gestione errori POSIX-compliant
- [ ] Ottimizzazioni per {arch}
'''

    def _generate_test_template(self, syscall: str, prefix: str) -> str:
        """Genera test Python template"""
        module_name = f"{prefix}{syscall}"
        class_name = f"{syscall.title()}Test"
        
        return f'''#!/usr/bin/env python3
# filepath: test.py

"""
Test suite per {syscall} ({prefix}architettura)
"""

import subprocess
import sys
import os
from pathlib import Path

class {class_name}:
    def __init__(self):
        self.module_name = "{module_name}"
        self.test_executable = f"./{{self.module_name}}"
        
    def compile_module(self):
        """Compila il modulo"""
        print(f"🔨 Compilando {{self.module_name}}...")
        try:
            result = subprocess.run(["make", "clean"], capture_output=True, text=True)
            result = subprocess.run(["make", "debug"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Errore compilazione: {{result.stderr}}")
                return False
            print(f"✅ Compilazione {{self.module_name}} completata")
            return True
        except Exception as e:
            print(f"❌ Errore durante compilazione: {{e}}")
            return False
    
    def run_basic_test(self):
        """Esegue test di base"""
        if not Path(self.test_executable).exists():
            print(f"❌ Eseguibile {{self.test_executable}} non trovato")
            return False
            
        print(f"🧪 Eseguendo test di base per {{self.module_name}}...")
        try:
            result = subprocess.run([self.test_executable], 
                                  capture_output=True, text=True, timeout=10)
            print(f"📋 Output: {{result.stdout}}")
            if result.stderr:
                print(f"⚠️  Stderr: {{result.stderr}}")
            
            # TODO: Aggiungere verifiche specifiche per {syscall}
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout durante test di {{self.module_name}}")
            return False
        except Exception as e:
            print(f"❌ Errore durante test: {{e}}")
            return False
    
    def run_all_tests(self):
        """Esegue tutti i test"""
        print(f"🚀 Avvio test completi per {{self.module_name}}")
        
        if not self.compile_module():
            return False
            
        if not self.run_basic_test():
            return False
            
        print(f"✅ Tutti i test per {{self.module_name}} completati con successo")
        return True

def main():
    """Funzione principale"""
    tester = {class_name}()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
'''

    def _create_config_files(self):
        """Crea file di configurazione del progetto"""
        
        # Project config
        config = {
            "project_name": "POSIX_Syscalls_Implementation",
            "version": "1.0.0",
            "architectures": ["x86_64", "x86_32"],
            "default_arch": "x86_64",
            "patch_directories": [],
            "build_options": {
                "debug": True,
                "optimization": "O2",
                "warnings": "all"
            }
        }
        
        config_file = self.base_dir / "project_config.json"
        config_file.write_text(json.dumps(config, indent=2))
        
        # Crea script principale di build
        self._create_build_script()
        
    def _create_build_script(self):
        """Crea script di build principale"""
        script_content = '''#!/bin/bash
# filepath: build_project.sh

python3 create_project_structure.py build "$@"
'''
        script_path = self.base_dir / "build_project.sh"
        script_path.write_text(script_content)
        script_path.chmod(0o755)

    def build_project(self, arch: Optional[str] = None, patch_dir: Optional[str] = None, full_build: bool = False):
        """Build del progetto con opzioni"""
        print(f"🚀 Avvio build del progetto...")
        
        if not arch:
            arch = self._select_architettura()
        
        if not patch_dir and self._has_patches():
            patch_dir = self._select_patch()
        
        results = self._build_modules(arch, patch_dir, full_build)
        self._print_build_report(results)
        
    def _select_architettura(self) -> str:
        """Selezione interattiva dell'architettura"""
        print("\n🏗️  Seleziona architettura:")
        print("1. x86_64 (64-bit)")
        print("2. x86_32 (32-bit)")
        print("3. Entrambe")
        
        choice = input("Scelta [1]: ").strip() or "1"
        
        if choice == "1":
            return "x86_64"
        elif choice == "2":
            return "x86_32"
        elif choice == "3":
            return "both"
        else:
            print("Scelta non valida, uso x86_64")
            return "x86_64"
    
    def _has_patches(self) -> bool:
        """Verifica se esistono patch"""
        patches_dir = self.base_dir / "patches"
        return patches_dir.exists() and any(patches_dir.iterdir())
    
    def _select_patch(self) -> Optional[str]:
        """Selezione patch"""
        patches_dir = self.base_dir / "patches"
        if not patches_dir.exists():
            return None
        
        patches = [d.name for d in patches_dir.iterdir() if d.is_dir()]
        if not patches:
            return None
        
        print("\n🔧 Patch disponibili:")
        print("0. Nessuna patch")
        for i, patch in enumerate(patches, 1):
            print(f"{i}. {patch}")
        
        choice = input("Scelta [0]: ").strip() or "0"
        try:
            idx = int(choice)
            if idx == 0:
                return None
            elif 1 <= idx <= len(patches):
                return patches[idx - 1]
        except ValueError:
            pass
        
        print("Scelta non valida, nessuna patch applicata")
        return None
    
    def _build_modules(self, arch: str, patch_dir: Optional[str], full_build: bool) -> Dict:
        """Build dei moduli"""
        results = {
            "completed": [],
            "completed_with_errors": [],
            "incomplete": [],
            "empty": []
        }
        
        arch_dirs = ["arch/x86_64", "arch/x86_32"] if arch == "both" else [f"arch/{arch}"]
        
        for arch_dir in arch_dirs:
            self._build_arch_modules(arch_dir, patch_dir, results, full_build)
        
        return results
    
    def _build_arch_modules(self, arch_dir: str, patch_dir: Optional[str], results: Dict, full_build: bool):
        """Build moduli per una specifica architettura"""
        arch_path = self.base_dir / arch_dir
        
        if not arch_path.exists():
            return
        
        for level_dir in arch_path.iterdir():
            if not level_dir.is_dir():
                continue
                
            for category_dir in level_dir.iterdir():
                if not category_dir.is_dir():
                    continue
                    
                for module_dir in category_dir.iterdir():
                    if not module_dir.is_dir():
                        continue
                    
                    self._build_single_module(module_dir, patch_dir, results, full_build)
    
    def _build_single_module(self, module_dir: Path, patch_dir: Optional[str], results: Dict, full_build: bool):
        """Build di un singolo modulo"""
        module_name = module_dir.name
        
        # Verifica completezza modulo
        required_files = [f"{module_name}.cpp", f"{module_name}.h", "Makefile", f"{module_name}.md", "test.py"]
        existing_files = []
        missing_files = []
        
        for req_file in required_files:
            file_path = module_dir / req_file
            # CORREZIONE: controlla che il file esista E abbia dimensione > 0
            if file_path.exists() and file_path.stat().st_size > 0:
                existing_files.append(req_file)
            else:
                missing_files.append(req_file)
        
        # Applica patch se necessario
        if patch_dir:
            self._apply_patch(module_dir, patch_dir)
        
        # Classifica modulo - CORREZIONE: tutti i file devono essere presenti E non vuoti
        if len(existing_files) == len(required_files):
            # Modulo completo - prova build e test
            success, error = self._compile_and_test_module(module_dir)
            if success:
                results["completed"].append({"name": module_name, "path": str(module_dir)})
            else:
                results["completed_with_errors"].append({
                    "name": module_name, 
                    "path": str(module_dir),
                    "error": error
                })
        elif len(existing_files) > 0:
            results["incomplete"].append({
                "name": module_name,
                "path": str(module_dir),
                "existing": existing_files,
                "missing": missing_files
            })
        else:
            results["empty"].append({"name": module_name, "path": str(module_dir)})

    def _apply_patch(self, module_dir: Path, patch_dir: str):
        """Applica patch a un modulo"""
        patches_base = self.base_dir / "patches" / patch_dir
        
        # Calcola path relativo del modulo rispetto ad arch/
        try:
            rel_path = module_dir.relative_to(self.base_dir / "arch")
            # Rimuovi il primo componente (x86_64 o x86_32)
            patch_path = patches_base / Path(*rel_path.parts[1:])
            
            if patch_path.exists():
                print(f"🔧 Applicando patch da {patch_path} a {module_dir}")
                
                # Copia file patchati sovrascrivendo quelli esistenti
                for patch_file in patch_path.iterdir():
                    if patch_file.is_file():
                        target_file = module_dir / patch_file.name
                        shutil.copy2(patch_file, target_file)
                        print(f"  ✓ Patch applicata: {patch_file.name}")
                        
        except ValueError:
            # Path non relativo ad arch/, ignora
            pass

    def create_patch_directory(self, patch_name: str, description: str = ""):
        """Crea una nuova directory di patch"""
        patch_dir = self.base_dir / "patches" / patch_name
        patch_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea file di descrizione patch
        patch_info = {
            "name": patch_name,
            "description": description,
            "created": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()),
            "modules": []
        }
        
        info_file = patch_dir / "patch_info.json"
        info_file.write_text(json.dumps(patch_info, indent=2))
        
        print(f"📁 Creata directory patch: {patch_name}")
        return patch_dir

    def copy_module_to_patch(self, module_path: str, patch_name: str):
        """Copia un modulo nella directory patch per modifiche"""
        module_dir = Path(module_path)
        if not module_dir.exists():
            print(f"❌ Modulo non trovato: {module_path}")
            return False
        
        # Calcola path di destinazione
        try:
            rel_path = module_dir.relative_to(self.base_dir / "arch")
            # Rimuovi il primo componente (x86_64 o x86_32)
            dest_path = self.base_dir / "patches" / patch_name / Path(*rel_path.parts[1:])
            
            dest_path.mkdir(parents=True, exist_ok=True)
            
            # Copia tutti i file del modulo
            for src_file in module_dir.iterdir():
                if src_file.is_file():
                    shutil.copy2(src_file, dest_path / src_file.name)
            
            print(f"📦 Modulo copiato in patch {patch_name}: {dest_path}")
            return True
            
        except ValueError:
            print(f"❌ Path modulo non valido: {module_path}")
            return False

    def list_patches(self):
        """Lista tutte le patch disponibili"""
        patches_dir = self.base_dir / "patches"
        if not patches_dir.exists():
            print("📂 Nessuna directory patches trovata")
            return []
        
        patches = []
        print("\n🔧 PATCH DISPONIBILI")
        print("=" * 40)
        
        for patch_dir in patches_dir.iterdir():
            if not patch_dir.is_dir():
                continue
            
            info_file = patch_dir / "patch_info.json"
            if info_file.exists():
                try:
                    patch_info = json.loads(info_file.read_text())
                    patches.append(patch_info)
                    print(f"📁 {patch_info['name']}")
                    print(f"   {patch_info.get('description', 'Nessuna descrizione')}")
                    
                    # Conta moduli nella patch
                    module_count = sum(1 for _ in patch_dir.rglob("*.cpp"))
                    print(f"   📦 Moduli: {module_count}")
                    
                except json.JSONDecodeError:
                    print(f"⚠️  {patch_dir.name} (info corrotto)")
        
        return patches

    def generate_dependency_graph(self):
        """Genera grafo delle dipendenze tra moduli"""
        print("🔗 Generando grafo delle dipendenze...")
        
        dependencies = {}
        
        # Analizza ogni modulo per trovare dipendenze
        for arch in ["x86_64", "x86_32"]:
            arch_path = self.base_dir / "arch" / arch
            if not arch_path.exists():
                continue
                
            for level_dir in arch_path.rglob("*"):
                if level_dir.name.endswith(".cpp"):
                    module_name = level_dir.stem
                    deps = self._extract_dependencies(level_dir)
                    if deps:
                        dependencies[module_name] = deps
        
        # Salva grafo
        graph_file = self.base_dir / "dependency_graph.json"
        graph_file.write_text(json.dumps(dependencies, indent=2))
        
        # Genera visualizzazione DOT
        self._generate_dot_graph(dependencies)
        
        print(f"✅ Grafo delle dipendenze salvato in {graph_file}")
        return dependencies

    def _extract_dependencies(self, cpp_file: Path) -> List[str]:
        """Estrae dipendenze da un file CPP"""
        dependencies = []
        
        try:
            content = cpp_file.read_text()
            
            # Cerca include di altri moduli
            import re
            includes = re.findall(r'#include\s+"([^"]+)"', content)
            
            for include in includes:
                if include.endswith('.h') and include != cpp_file.stem + '.h':
                    dep_name = include.replace('.h', '')
                    dependencies.append(dep_name)
            
            # Cerca chiamate a funzioni di altri moduli
            function_calls = re.findall(r'(\w+)_impl\s*\(', content)
            for call in function_calls:
                if call != cpp_file.stem:
                    dependencies.append(call)
                    
        except Exception as e:
            print(f"⚠️  Errore analisi dipendenze {cpp_file}: {e}")
        
        return list(set(dependencies))  # Rimuovi duplicati

    def _generate_dot_graph(self, dependencies: Dict):
        """Genera file DOT per visualizzazione grafo"""
        dot_content = "digraph dependencies {\n"
        dot_content += "  rankdir=LR;\n"
        dot_content += "  node [shape=box];\n\n"
        
        for module, deps in dependencies.items():
            for dep in deps:
                dot_content += f'  "{module}" -> "{dep}";\n'
        
        dot_content += "}\n"
        
        dot_file = self.base_dir / "dependency_graph.dot"
        dot_file.write_text(dot_content)
        
        # Prova a generare PNG se graphviz è disponibile
        try:
            subprocess.run(
                ["dot", "-Tpng", str(dot_file), "-o", str(self.base_dir / "dependency_graph.png")],
                check=True, capture_output=True
            )
            print("📊 Grafico PNG generato: dependency_graph.png")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ℹ️  Installa graphviz per generare visualizzazione PNG")

    def clean_project(self, arch: Optional[str] = None):
        """Pulisce tutti i file generati dal build"""
        print("🧹 Pulizia progetto...")
        
        cleaned_count = 0
        arch_dirs = []
        
        if arch == "both" or arch is None:
            arch_dirs = ["arch/x86_64", "arch/x86_32"]
        else:
            arch_dirs = [f"arch/{arch}"]
        
        for arch_dir in arch_dirs:
            arch_path = self.base_dir / arch_dir
            if not arch_path.exists():
                continue
                
            # Trova e rimuovi file generati
            for pattern in ["*.o", "*.so", "*.a", "test_*", "*.exe"]:
                for file_to_clean in arch_path.rglob(pattern):
                    if file_to_clean.is_file():
                        file_to_clean.unlink()
                        cleaned_count += 1
            
            # Esegui make clean in ogni modulo
            for module_dir in arch_path.rglob("Makefile"):
                try:
                    subprocess.run(
                        ["make", "clean"],
                        cwd=module_dir.parent,
                        capture_output=True,
                        check=True
                    )
                except subprocess.CalledProcessError:
                    pass  # Ignora errori make clean
        
        print(f"✅ Pulizia completata: {cleaned_count} file rimossi")

    def validate_project_integrity(self):
        """Valida l'integrità dell'intera struttura del progetto"""
        print("🔍 Validazione integrità progetto...")
        
        issues = []
        
        # Verifica struttura directory
        required_dirs = ["arch/x86_64", "arch/x86_32", "patches", "tools", "docs"]
        for req_dir in required_dirs:
            if not (self.base_dir / req_dir).exists():
                issues.append(f"Directory mancante: {req_dir}")
        
        # Verifica consistenza moduli tra architetture
        x64_modules = self._get_all_modules("arch/x86_64")
        x32_modules = self._get_all_modules("arch/x86_32")
        
        # Rimuovi prefisso x86_ dai moduli 32-bit per confronto
        x32_modules_normalized = [m.replace("x86_", "") for m in x32_modules]
        
        missing_in_32 = set(x64_modules) - set(x32_modules_normalized)
        missing_in_64 = set(x32_modules_normalized) - set(x64_modules)
        
        for missing in missing_in_32:
            issues.append(f"Modulo mancante in x86_32: x86_{missing}")
        
        for missing in missing_in_64:
            issues.append(f"Modulo mancante in x86_64: {missing}")
        
        # Verifica file di configurazione
        config_file = self.base_dir / "project_config.json"
        if not config_file.exists():
            issues.append("File di configurazione mancante: project_config.json")
        
        # Report validazione
        if issues:
            print(f"⚠️  Trovati {len(issues)} problemi:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ Progetto integro: nessun problema trovato")
        
        return len(issues) == 0

    def _get_all_modules(self, arch_dir: str) -> List[str]:
        """Ottieni lista di tutti i moduli per un'architettura"""
        modules = []
        arch_path = self.base_dir / arch_dir
        
        if arch_path.exists():
            for cpp_file in arch_path.rglob("*.cpp"):
                modules.append(cpp_file.stem)
        
        return modules

    def export_project_statistics(self):
        """Esporta statistiche complete del progetto"""
        print("📊 Generando statistiche progetto...")
        
        stats = {
            "timestamp": str(subprocess.run(["date"], capture_output=True, text=True).stdout.strip()),
            "architectures": {},
            "totals": {
                "modules": 0,
                "completed": 0,
                "incomplete": 0,
                "empty": 0,
                "lines_of_code": 0
            },
            "patches": len(list((self.base_dir / "patches").iterdir())) if (self.base_dir / "patches").exists() else 0
        }
        
        for arch in ["x86_64", "x86_32"]:
            arch_path = self.base_dir / "arch" / arch
            if arch_path.exists():
                arch_stats = self._calculate_arch_statistics(arch_path)
                stats["architectures"][arch] = arch_stats
                
                # Aggiorna totali
                stats["totals"]["modules"] += arch_stats["total_modules"]
                stats["totals"]["completed"] += arch_stats["completed"]
                stats["totals"]["incomplete"] += arch_stats["incomplete"]
                stats["totals"]["empty"] += arch_stats["empty"]
                stats["totals"]["lines_of_code"] += arch_stats["lines_of_code"]
        
        # Salva statistiche
        stats_file = self.base_dir / "project_statistics.json"
        stats_file.write_text(json.dumps(stats, indent=2))
        
        # Genera report leggibile
        self._generate_stats_report(stats)
        
        print(f"✅ Statistiche salvate in {stats_file}")
        return stats

    def _calculate_arch_statistics(self, arch_path: Path) -> Dict:
        """Calcola statistiche per una specifica architettura"""
        stats = {
            "total_modules": 0,
            "completed": 0,
            "incomplete": 0,
            "empty": 0,
            "lines_of_code": 0,
            "levels": {}
        }
        
        for level_dir in arch_path.iterdir():
            if not level_dir.is_dir():
                continue
            
            level_stats = {"modules": 0, "completed": 0}
            
            for category_dir in level_dir.iterdir():
                if not category_dir.is_dir():
                    continue
                
                for module_dir in category_dir.iterdir():
                    if not module_dir.is_dir():
                        continue
                    
                    stats["total_modules"] += 1
                    level_stats["modules"] += 1
                    
                    # Analizza completezza modulo
                    module_status = self._analyze_module_completeness(module_dir)
                    
                    if module_status["complete"]:
                        stats["completed"] += 1
                        level_stats["completed"] += 1
                    elif module_status["has_files"]:
                        stats["incomplete"] += 1
                    else:
                        stats["empty"] += 1
                    
                    stats["lines_of_code"] += module_status["lines_of_code"]
            
            stats["levels"][level_dir.name] = level_stats
        
        return stats

    def _analyze_module_completeness(self, module_dir: Path) -> Dict:
        """Analizza completezza di un singolo modulo con controllo contenuto"""
        module_name = module_dir.name
        required_files = [f"{module_name}.cpp", f"{module_name}.h", "Makefile", f"{module_name}.md", "test.py"]
        
        existing_files = 0
        lines_of_code = 0
        file_details = []
        actual_implementation = 0
        
        for req_file in required_files:
            file_path = module_dir / req_file
            if file_path.exists():
                file_size = file_path.stat().st_size
                if file_size > 0:
                    # Analizza contenuto per determinare se è realmente implementato
                    content_status = self._analyze_file_content(file_path, req_file)
                    
                    if content_status["has_real_content"]:
                        existing_files += 1
                        actual_implementation += 1
                        file_details.append(f"{req_file} ({file_size} bytes - IMPLEMENTED)")
                    else:
                        file_details.append(f"{req_file} ({file_size} bytes - STUB/TEMPLATE)")
                    
                    # Conta righe di codice solo se implementato
                    if req_file.endswith(('.cpp', '.h')) and content_status["has_real_content"]:
                        lines_of_code += content_status["effective_lines"]
                else:
                    file_details.append(f"{req_file} (0 bytes - VUOTO)")
            else:
                file_details.append(f"{req_file} (MANCANTE)")
        
        # Un modulo è completo solo se tutti i file esistono E contengono implementazioni reali
        is_complete = (existing_files == len(required_files) and 
                      actual_implementation == len(required_files))
        
        return {
            "complete": is_complete,
            "has_files": existing_files > 0,
            "lines_of_code": lines_of_code,
            "completeness_ratio": actual_implementation / len(required_files),
            "file_details": file_details,
            "implementation_ratio": actual_implementation / len(required_files)
        }

    def _analyze_file_content(self, file_path: Path, file_type: str) -> Dict:
        """Analizza il contenuto di un file per determinare se è implementato o solo template"""
        try:
            content = file_path.read_text()
            lines = content.splitlines()
            
            # Indicatori di template/stub non implementato
            stub_indicators = [
                "TODO:", "FIXME:", "Not implemented", "ENOSYS", 
                "errno = ENOSYS", "placeholder", "template",
                "da implementare", "da definire", "stub"
            ]
            
            # Indicatori di implementazione reale
            implementation_indicators = [
                "syscall(", "return syscall", "#ifdef __x86_64__",
                "real implementation", "actual implementation"
            ]
            
            stub_count = 0
            impl_count = 0
            effective_lines = 0
            
            for line in lines:
                line_clean = line.strip().lower()
                
                # Salta commenti e linee vuote
                if not line_clean or line_clean.startswith('//') or line_clean.startswith('/*'):
                    continue
                
                effective_lines += 1
                
                # Conta indicatori
                for indicator in stub_indicators:
                    if indicator.lower() in line_clean:
                        stub_count += 1
                        break
                
                for indicator in implementation_indicators:
                    if indicator.lower() in line_clean:
                        impl_count += 1
                        break
            
            # Logica specifica per tipo di file
            if file_type.endswith('.cpp'):
                # CPP: deve avere implementazione reale, non solo TODO/ENOSYS
                has_real_content = (impl_count > 0 and 
                                  effective_lines > 20 and 
                                  stub_count < effective_lines * 0.3)
            
            elif file_type.endswith('.h'):
                # Header: deve avere definizioni reali, non solo template
                has_real_content = (effective_lines > 10 and 
                                  stub_count < 3)
            
            elif file_type == "Makefile":
                # Makefile: deve essere funzionale
                makefile_indicators = ["$(CXX)", "$(CC)", ".cpp:", ".o:"]
                makefile_score = sum(1 for ind in makefile_indicators if ind in content)
                has_real_content = makefile_score >= 3 and effective_lines > 15
            
            elif file_type.endswith('.md'):
                # Documentazione: deve essere più di template base
                has_real_content = effective_lines > 30 and stub_count < 5
            
            elif file_type.endswith('.py'):
                # Test Python: deve avere test reali
                python_indicators = ["subprocess", "assert", "test_", "def "]
                python_score = sum(1 for ind in python_indicators if ind in content)
                has_real_content = python_score >= 3 and effective_lines > 40
            
            else:
                has_real_content = effective_lines > 10 and stub_count < effective_lines * 0.5
            
            return {
                "has_real_content": has_real_content,
                "effective_lines": effective_lines,
                "stub_count": stub_count,
                "impl_count": impl_count,
                "analysis": f"Lines: {effective_lines}, Stubs: {stub_count}, Impl: {impl_count}"
            }
            
        except Exception as e:
            return {
                "has_real_content": False,
                "effective_lines": 0,
                "stub_count": 0,
                "impl_count": 0,
                "analysis": f"Error: {str(e)}"
            }

    def _print_build_report(self, results: Dict):
        """Stampa report del build - VERSIONE FUNZIONALE"""
        print("\n" + "="*60)
        print("BUILD REPORT")
        print("="*60)
        
        print(f"\nMODULI COMPLETATI: {len(results['completed'])}")
        for i, module in enumerate(results['completed'], 1):
            print(f"  {i:3d}. {module['name']}")
        
        print(f"\nMODULI CON ERRORI: {len(results['completed_with_errors'])}")
        for i, module in enumerate(results['completed_with_errors'], 1):
            print(f"  {i:3d}. {module['name']}")
            print(f"       ERRORE: {module['error'][:100]}...")
        
        print(f"\nMODULI INCOMPLETI: {len(results['incomplete'])}")
        for i, module in enumerate(results['incomplete'], 1):
            print(f"  {i:3d}. {module['name']}")
            print(f"       Presenti: {', '.join(module['existing'])}")
            print(f"       Mancanti: {', '.join(module['missing'])}")
        
        print(f"\nMODULI VUOTI: {len(results['empty'])}")
        for i, module in enumerate(results['empty'], 1):
            print(f"  {i:3d}. {module['name']}")
        
        total = sum(len(results[key]) for key in results)
        success_rate = len(results['completed']) / total * 100 if total > 0 else 0
        
        print(f"\nSTATISTICHE:")
        print(f"  Totale moduli: {total}")
        print(f"  Completati: {len(results['completed'])} ({success_rate:.1f}%)")
        print(f"  Con errori: {len(results['completed_with_errors'])}")
        print(f"  Incompleti: {len(results['incomplete'])}")
        print(f"  Vuoti: {len(results['empty'])}")

    def _print_project_map(self, mapping: Dict):
        """Stampa mappa del progetto con distinzione tra template e implementazioni"""
        print("\n" + "="*60)
        print("PROJECT MAP - IMPLEMENTATION STATUS")
        print("="*60)
        
        for arch, arch_data in mapping["architectures"].items():
            print(f"\n{arch.upper()}:")
            
            total_modules = 0
            fully_implemented = 0
            template_only = 0
            partial_impl = 0
            
            for level, categories in arch_data.items():
                print(f"  {level}:")
                
                for category, modules in categories.items():
                    if modules:  # Solo se ci sono moduli
                        print(f"    {category}:")
                        
                        for module in modules:
                            total_modules += 1
                            impl_ratio = module.get("implementation_ratio", module.get("completeness", 0))
                            
                            if impl_ratio >= 0.9:
                                status = "IMPLEMENTED"
                                fully_implemented += 1
                            elif impl_ratio >= 0.5:
                                status = "PARTIAL"
                                partial_impl += 1
                            elif impl_ratio > 0:
                                status = "STARTED"
                                template_only += 1
                            else:
                                status = "TEMPLATE"
                                template_only += 1
                            
                            print(f"      {module['name']}: {status} ({impl_ratio*100:.0f}%)")
            
            implementation_rate = (fully_implemented / total_modules * 100) if total_modules > 0 else 0
            print(f"  TOTALE {arch}: {fully_implemented}/{total_modules} implementati ({implementation_rate:.1f}%)")
            print(f"    Implementati: {fully_implemented}, Parziali: {partial_impl}, Template: {template_only}")

    def list_all_modules(self):
        """Lista tutti i moduli con stato dettagliato"""
        print("LISTA COMPLETA MODULI")
        print("=" * 60)
        
        for arch in ["x86_64", "x86_32"]:
            arch_path = self.base_dir / "arch" / arch
            if not arch_path.exists():
                continue
                
            print(f"\n{arch.upper()}:")
            
            module_count = 0
            for level_dir in arch_path.iterdir():
                if not level_dir.is_dir():
                    continue
                
                for category_dir in level_dir.iterdir():
                    if not category_dir.is_dir():
                        continue
                    
                    for module_dir in category_dir.iterdir():
                        if not module_dir.is_dir():
                            continue
                        
                        module_count += 1
                        module_name = module_dir.name
                        analysis = self._analyze_module_completeness(module_dir)
                        
                        status = "COMPLETE" if analysis["complete"] else "PARTIAL" if analysis["has_files"] else "EMPTY"
                        
                        print(f"  {module_count:3d}. {module_name} [{status}]")
                        print(f"       Path: {module_dir}")
                        print(f"       LOC: {analysis['lines_of_code']}")
                        
                        # Mostra dettagli file solo se richiesto
                        if not analysis["complete"]:
                            for detail in analysis["file_details"]:
                                if "MANCANTE" in detail or "VUOTO" in detail:
                                    print(f"       {detail}")

    def validate_all_modules(self):
        """Valida tutti i moduli e mostra dettagliato"""
        print("VALIDAZIONE COMPLETA MODULI")
        print("=" * 60)
        
        issues = []
        total_modules = 0
        
        for arch in ["x86_64", "x86_32"]:
            arch_path = self.base_dir / "arch" / arch
            if not arch_path.exists():
                issues.append(f"Directory mancante: arch/{arch}")
                continue
            
            print(f"\nValidazione {arch}:")
            
            for level_dir in arch_path.iterdir():
                if not level_dir.is_dir():
                    continue
                
                for category_dir in level_dir.iterdir():
                    if not category_dir.is_dir():
                        continue
                    
                    for module_dir in category_dir.iterdir():
                        if not module_dir.is_dir():
                            continue
                        
                        total_modules += 1
                        module_name = module_dir.name
                        
                        # Verifica file richiesti
                        required_files = [f"{module_name}.cpp", f"{module_name}.h", "Makefile", f"{module_name}.md", "test.py"]
                        
                        for req_file in required_files:
                            file_path = module_dir / req_file
                            if not file_path.exists():
                                issues.append(f"{module_name}: File mancante {req_file}")
                            elif file_path.stat().st_size == 0:
                                issues.append(f"{module_name}: File vuoto {req_file}")
        
        print(f"\nRISULTATI VALIDAZIONE:")
        print(f"Moduli totali: {total_modules}")
        print(f"Problemi trovati: {len(issues)}")
        
        if issues:
            print("\nPROBLEMI:")
            for i, issue in enumerate(issues, 1):
                print(f"  {i:3d}. {issue}")
        else:
            print("Nessun problema trovato.")
        
        return len(issues) == 0

    def _compile_and_test_module(self, module_dir: Path) -> Tuple[bool, str]:
        """Compila e testa un singolo modulo"""
        try:
            # Clean first
            result = subprocess.run(
                ["make", "clean"],
                cwd=module_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Compile
            result = subprocess.run(
                ["make", "debug"],
                cwd=module_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return False, f"Compile error: {result.stderr[:200]}"
            
            # Check if executable exists
            module_name = module_dir.name
            executable = module_dir / module_name
            
            if not executable.exists():
                return False, "Executable not found after compilation"
            
            # Try to run
            result = subprocess.run(
                [str(executable)],
                cwd=module_dir,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # Success if runs without crashing (even if returns error codes)
            return True, "OK"
            
        except subprocess.TimeoutExpired:
            return False, "Timeout during compilation or execution"
        except Exception as e:
            return False, f"Exception: {str(e)}"

    def _generate_stats_report(self, stats: Dict):
        """Genera report testuale delle statistiche"""
        print("\n" + "="*60)
        print("PROJECT STATISTICS REPORT")
        print("="*60)
        
        # Overall stats
        totals = stats["totals"]
        print(f"\nOVERALL STATISTICS:")
        print(f"Total modules: {totals['modules']}")
        print(f"Completed: {totals['completed']}")
        print(f"Incomplete: {totals['incomplete']}")
        print(f"Empty: {totals['empty']}")
        print(f"Lines of code: {totals['lines_of_code']}")
        print(f"Available patches: {stats['patches']}")
        
        completion_rate = (totals['completed'] / totals['modules'] * 100) if totals['modules'] > 0 else 0
        print(f"Completion rate: {completion_rate:.1f}%")
        
        # Per-architecture stats
        for arch, arch_stats in stats["architectures"].items():
            print(f"\n{arch.upper()} ARCHITECTURE:")
            print(f"  Total modules: {arch_stats['total_modules']}")
            print(f"  Completed: {arch_stats['completed']}")
            print(f"  Incomplete: {arch_stats['incomplete']}")
            print(f"  Empty: {arch_stats['empty']}")
            print(f"  Lines of code: {arch_stats['lines_of_code']}")
            
            arch_completion = (arch_stats['completed'] / arch_stats['total_modules'] * 100) if arch_stats['total_modules'] > 0 else 0
            print(f"  Completion rate: {arch_completion:.1f}%")
            
            # Level breakdown
            print(f"  Level breakdown:")
            for level, level_stats in arch_stats["levels"].items():
                level_completion = (level_stats['completed'] / level_stats['modules'] * 100) if level_stats['modules'] > 0 else 0
                print(f"    {level}: {level_stats['completed']}/{level_stats['modules']} ({level_completion:.1f}%)")

    def map_project(self):
        """Genera mappa completa del progetto"""
        print("🗺️  Generando mappa del progetto...")
        
        mapping = {
            "timestamp": subprocess.run(["date"], capture_output=True, text=True).stdout.strip(),
            "architectures": {}
        }
        
        for arch in ["x86_64", "x86_32"]:
            arch_path = self.base_dir / "arch" / arch
            if not arch_path.exists():
                continue
            
            arch_mapping = {}
            
            for level_dir in arch_path.iterdir():
                if not level_dir.is_dir():
                    continue
                
                level_mapping = {}
                
                for category_dir in level_dir.iterdir():
                    if not category_dir.is_dir():
                        continue
                    
                    category_modules = []
                    
                    for module_dir in category_dir.iterdir():
                        if not module_dir.is_dir():
                            continue
                        
                        analysis = self._analyze_module_completeness(module_dir)
                        module_info = {
                            "name": module_dir.name,
                            "path": str(module_dir.relative_to(self.base_dir)),
                            "completeness": analysis["completeness_ratio"],
                            "lines_of_code": analysis["lines_of_code"],
                            "complete": analysis["complete"],
                            "has_files": analysis["has_files"]
                        }
                        category_modules.append(module_info)
                    
                    if category_modules:  # Only add if has modules
                        level_mapping[category_dir.name] = category_modules
                
                if level_mapping:  # Only add if has categories
                    arch_mapping[level_dir.name] = level_mapping
            
            mapping["architectures"][arch] = arch_mapping
        
        # Save mapping
        map_file = self.base_dir / "project_map.json"
        map_file.write_text(json.dumps(mapping, indent=2))
        
        # Print readable map
        self._print_project_map(mapping)
        
        print(f"\n✅ Mappa salvata in: {map_file}")
        return mapping

def main():
    manager = POSIXSyscallManager()
    
    if len(sys.argv) < 2:
        print("Usage: python3 create_project_structure.py <command> [options]")
        print("Commands:")
        print("  create      - Crea struttura progetto")
        print("  build       - Build progetto")
        print("  map         - Mappa progetto")
        print("  full        - Build completo")
        print("  clean       - Pulizia progetto")
        print("  validate    - Valida integrità progetto")
        print("  list        - Lista tutti i moduli")
        print("  check       - Verifica dettagliata moduli")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        manager.create_project_structure()
    elif command == "build":
        arch = sys.argv[2] if len(sys.argv) > 2 else None
        full_build = "--full" in sys.argv
        manager.build_project(arch=arch, full_build=full_build)
    elif command == "map":
        manager.map_project()
    elif command == "full":
        manager.build_project(full_build=True)
    elif command == "clean":
        arch = sys.argv[2] if len(sys.argv) > 2 else None
        manager.clean_project(arch)
    elif command == "validate":
        manager.validate_project_integrity()
    elif command == "list":
        manager.list_all_modules()
    elif command == "check":
        manager.validate_all_modules()
    else:
        print(f"Comando sconosciuto: {command}")

if __name__ == "__main__":
    main()
