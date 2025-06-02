# POSIX Syscalls Implementation Project

Implementazione modulare completa di tutte le system call POSIX con supporto per architetture 32 e 64 bit.

## Quick Start

### 1. Creazione Progetto
```bash
# Crea struttura completa
python3 create_project_structure.py create

# Verifica stato con distinzione template/implementazione
python3 simple_checker.py summary
```

### 2. Creazione Moduli
```bash
# Wizard interattivo per nuovi moduli
python3 project_utilities.py wizard

# Build e test
python3 create_project_structure.py build
```

### 3. Controlli e Validazione
```bash
# Controllo rapido con distinzione implementazione/template
python3 simple_checker.py full

# Mappa progetto con stato implementazione
python3 create_project_structure.py map

# Validazione completa
python3 create_project_structure.py check
```

## Comandi Principali

### Script Principale (create_project_structure.py)
```bash
python3 create_project_structure.py create      # Crea struttura
python3 create_project_structure.py build       # Build moduli
python3 create_project_structure.py full        # Build completo
python3 create_project_structure.py clean       # Pulizia
python3 create_project_structure.py check       # Validazione dettagliata
python3 create_project_structure.py list        # Lista tutti i moduli
python3 create_project_structure.py map         # Mappa progetto con stato reale
```

### Utilities Avanzate (project_utilities.py)
```bash
python3 project_utilities.py wizard             # Crea modulo interattivo
```

### Controllo Rapido (simple_checker.py)
```bash
python3 simple_checker.py                       # Lista dettagliata
python3 simple_checker.py summary               # Solo statistiche
python3 simple_checker.py full                  # Controllo funzionalità
```

## Struttura Progetto

```
CIPOLLA/
├── arch/
│   ├── x86_64/                    # Moduli 64-bit
│   └── x86_32/                    # Moduli 32-bit (prefisso x86_)
├── patches/                       # Patch di compatibilità
├── create_project_structure.py    # Script principale
├── project_utilities.py          # Utilities avanzate
├── simple_checker.py             # Controllo rapido
├── run_tests.sh                  # Test automatizzati
├── .vscode/                      # Configurazione VS Code
│   ├── launch.json              # Debug configuration
│   └── c_cpp_properties.json    # C++ IntelliSense
├── posix_syscalls_hierarchy.json # Mappa dipendenze syscall
└── README.md                     # Questa guida
```

### Struttura Modulo
Ogni modulo contiene:
```
nome_modulo/
├── nome_modulo.cpp               # Implementazione
├── nome_modulo.h                 # Header
├── Makefile                      # Build system
├── nome_modulo.md               # Documentazione
└── test.py                      # Test suite
```

## Stato del Progetto

### Analisi Contenuto Intelligente
Il sistema ora distingue tra:
- **IMPLEMENTED**: File con implementazione reale
- **PARTIAL**: Implementazione parziale con alcune funzionalità
- **TEMPLATE**: Solo template di base con TODO/stub
- **EMPTY**: File vuoti o mancanti

### Criteri di Valutazione
Per ogni tipo di file:

**File C++ (.cpp)**:
- ✅ Implementato: Contiene chiamate syscall reali, >20 righe effettive, <30% TODO/stub
- ⚠️ Template: Solo TODO, ENOSYS, "Not implemented"

**File Header (.h)**:
- ✅ Implementato: >15 righe effettive, definizioni complete, <3 TODO
- ⚠️ Template: Solo prototipi base

**Makefile**:
- ✅ Funzionale: Contiene target completi (CXX, clean, test, etc.)
- ⚠️ Template: Makefile base incompleto

**Documentazione (.md)**:
- ✅ Completa: >50 righe, documentazione dettagliata, <5 TODO
- ⚠️ Template: Solo template base

**Test Python (.py)**:
- ✅ Completi: >60 righe, test reali con subprocess, verifiche specifiche
- ⚠️ Template: Solo template base

## Workflow di Sviluppo

### 1. Creazione Nuovo Modulo
```bash
# Usa il wizard interattivo
python3 project_utilities.py wizard

# Il wizard genera:
# - Template con implementazione guidata
# - Makefile completo con tutti i target
# - Test Python funzionali
# - Documentazione strutturata
# - Header con API completa
```

### 2. Implementazione
```bash
cd arch/x86_64/level_X/categoria/modulo

# Il template include:
# - Struttura implementazione completa
# - Gestione errori POSIX
# - Debug logging opzionale
# - API informazioni modulo
# - Build system avanzato

# Sostituisci i TODO con implementazione reale:
# 1. Validazione parametri
# 2. Chiamata syscall architettura-specifica
# 3. Gestione errori e errno
# 4. Test specifici

# Test durante sviluppo
make test         # Test C++
make check        # Test completi
make analyze      # Analisi statica
```

### 3. Build e Test
```bash
# Test singolo modulo
cd modulo_directory
make check

# Test tutti i moduli con report
./run_tests.sh

# Controllo stato con implementazione reale
python3 simple_checker.py full

# Mappa progetto aggiornata
python3 create_project_structure.py map
```

## Sistema di Build Avanzato

### Makefile Targets Completi
Ogni modulo supporta:
```bash
make              # Build normale + library
make debug        # Build con debug symbols
make release      # Build ottimizzato
make test         # Esegui test C++
make check        # Test completi (C++ + Python)
make clean        # Pulizia completa
make install      # Installa nel sistema
make uninstall    # Rimuove dal sistema
make analyze      # Static analysis (cppcheck, clang-tidy)
make format       # Format codice (clang-format)
make profile      # Build per profiling
```

### Test Automatici Avanzati
I test Python verificano:
- **Compilazione**: Makefile funzionante, eseguibile generato
- **Esecuzione**: Nessun crash, gestione errori corretta
- **Target Makefile**: Tutti i target funzionano
- **Output**: Verifica output atteso
- **Performance**: Tempo esecuzione ragionevole
- **Report JSON**: Statistiche dettagliate

### Debug e Sviluppo
```bash
# Debug con VS Code configurato
# - launch.json per debug Python e C++
# - c_cpp_properties.json per IntelliSense

# Debug runtime
MODULO_DEBUG=1 ./modulo

# Memory debugging
valgrind --tool=memcheck ./modulo

# Performance profiling
make profile
gprof ./modulo gmon.out
```

## Monitoraggio Progresso Intelligente

### Stati Moduli Dettagliati
- **IMPLEMENTED (90-100%)**: Implementazione completa e funzionante
- **PARTIAL (50-89%)**: Implementazione parziale in corso
- **STARTED (1-49%)**: Sviluppo iniziato, principalmente template
- **TEMPLATE (0%)**: Solo template generati automaticamente

### Controlli Disponibili
```bash
# Riepilogo veloce con percentuali reali
python3 simple_checker.py summary

# Lista completa con stato implementazione
python3 simple_checker.py

# Controllo funzionalità (compila e testa tutto)
python3 simple_checker.py full

# Mappa progetto con stato reale
python3 create_project_structure.py map

# Validazione approfondita con dettagli file
python3 create_project_structure.py check
```

### Report e Statistiche
```bash
# Test automatizzati con report HTML
./run_tests.sh

# Genera mappa dipendenze
python3 create_project_structure.py map

# Export statistiche JSON
python3 create_project_structure.py stats
```

## Template di Implementazione Avanzato

### Struttura Generata dal Wizard
```cpp
// Esempio implementazione generata:
int modulo_impl() {
    // 1. Debug logging opzionale
    if (getenv("MODULO_DEBUG")) {
        std::cerr << "DEBUG: Executing syscall..." << std::endl;
    }
    
    // 2. Validazione parametri
    if (/* parametri non validi */) {
        errno = EINVAL;
        return -1;
    }
    
    // 3. Chiamata kernel architettura-specifica
    #ifdef __x86_64__
    result = syscall(SYS_syscall_name, params...);
    #endif
    
    // 4. Gestione errori
    if (result == -1) {
        // errno già impostato da syscall()
        return -1;
    }
    
    return result;
}
```

### API Modulo Completa
Ogni modulo espone:
```cpp
int modulo_impl();                              // Implementazione principale
int modulo_test();                              // Test di funzionamento
const char* modulo_get_description();           // Descrizione
const char* modulo_get_arch();                  // Architettura
int modulo_get_dependencies(char** deps, int max); // Dipendenze
```

## Gerarchia Syscall e Dipendenze

### Livelli di Implementazione (dal file posix_syscalls_hierarchy.json)

**Level 0 - Primitive**:
- `memory_management`: brk, sbrk, mmap, munmap, mprotect, msync
- `process_identity`: getpid, getppid, getuid, geteuid, getgid, getegid
- `basic_io`: read, write, open, close, lseek

**Level 1 - Fondamentali**:
- `filesystem_ops`: stat, fstat, access, chmod, mkdir, etc.
- `process_control`: fork, execve, wait, waitpid, exit, kill
- `signal_handling`: signal, sigaction, pause, alarm

**Level 2 - Intermedie**:
- `advanced_io`: dup, dup2, pipe, fcntl, select, poll
- `directory_ops`: opendir, readdir, closedir
- `time_ops`: time, gettimeofday, clock, sleep

**Level 3+ - Complesse**:
- `ipc_sysv`: System V IPC (msg, sem, shm)
- `networking`: socket, bind, listen, accept, connect
- `posix_threads`: pthread_create, pthread_join, etc.

### Strategia di Implementazione
1. **Iniziare da Level 0**: Primitive di base senza dipendenze
2. **Procedere per livelli**: Rispettare grafo dipendenze
3. **Test incrementali**: Verificare ogni livello prima del successivo
4. **Focus architettura**: Completare x86_64 prima di x86_32

## Stato Attuale del Progetto

Per verificare lo stato corrente:

```bash
# Statistiche rapide con implementazione reale
python3 simple_checker.py summary

# Controllo completo con test funzionalità
python3 simple_checker.py full

# Mappa dettagliata con stato implementazione
python3 create_project_structure.py map
```

### Obiettivi di Qualità
- **Zero warning** in compilazione
- **Zero memory leak** verificati con valgrind
- **100% test coverage** per moduli implementati
- **Documentazione completa** per ogni API
- **Conformità POSIX** verificata

## Contributing

### Implementare un Modulo
1. **Scegli modulo** dal livello appropriato
2. **Esegui wizard**: `python3 project_utilities.py wizard`
3. **Implementa logica** sostituendo TODO
4. **Aggiungi test** specifici
5. **Documenta** comportamento
6. **Verifica**: `make check`

### Code Quality
- Segui standard POSIX per comportamento syscall
- Gestisci tutti i casi di errore con errno appropriato
- Includi test per edge cases
- Mantieni documentazione aggiornata
- Usa static analysis (`make analyze`)

Il progetto è configurato per sviluppo efficiente con VS Code, include tutti gli strumenti necessari per implementazione sistematica delle syscall POSIX.
