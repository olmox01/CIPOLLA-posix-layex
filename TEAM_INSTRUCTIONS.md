# POSIX Syscalls Implementation - Complete Team Instructions

Istruzioni complete per implementazione sistematica delle system call POSIX con pattern specifici per ogni modulo.

## 📋 Organizzazione del Lavoro

### Struttura Team per Livelli
- **Team Level 0** (Primitive): 3-4 sviluppatori senior
- **Team Level 1** (Fondamentali): 4-5 sviluppatori esperti  
- **Team Level 2** (Intermedie): 3-4 sviluppatori intermedi
- **Team Level 3** (Complesse): 5-6 sviluppatori senior
- **Team Level 4** (High-level): 3-4 sviluppatori esperti
- **Team Level 5** (Specializzate): 4-5 sviluppatori specialisti

### Workflow Generale
1. **Iniziare sempre da Level 0** - nessuna dipendenza
2. **Completare tutti i moduli di un livello** prima di passare al successivo
3. **Test completo per ogni syscall** prima di segnarla come implementata
4. **Validazione POSIX compliance** per ogni implementazione
5. **Code review obbligatorio** tra membri del team

---

## 🎯 TEAM LEVEL 0 - PRIMITIVE FOUNDATIONS

**Responsabile**: Senior Developer con esperienza kernel/assembly
**Priorità**: MASSIMA - tutti gli altri livelli dipendono da questi

### 🧠 memory_management (3 sviluppatori)

#### brk - Program Break Control
```bash
# Path: arch/x86_64/level_0_primitives/memory_management/brk/
```

**Pattern Implementazione**:
```cpp
int brk_impl(void *addr) {
    // 1. Validazione indirizzo
    if (addr == NULL) {
        errno = EINVAL;
        return -1;
    }
    
    // 2. Ottieni break attuale per validazione
    void *current_brk = (void*)syscall(SYS_brk, 0);
    if (current_brk == (void*)-1) {
        return -1;
    }
    
    // 3. Validazione range (addr deve essere >= break iniziale)
    if (addr < current_brk && addr != 0) {
        // Permettiamo solo espansione o reset
        errno = EINVAL;
        return -1;
    }
    
    // 4. Chiamata syscall
    #ifdef __x86_64__
    void *result = (void*)syscall(SYS_brk, addr);
    #elif defined(__i386__)
    void *result = (void*)syscall(SYS_brk, addr);
    #endif
    
    // 5. Verifica successo
    if (result == addr) {
        return 0;  // Successo
    } else {
        errno = ENOMEM;
        return -1;
    }
}
```

**Test Pattern**:
```cpp
int brk_test() {
    // Test 1: Query current break
    void *initial_brk = (void*)syscall(SYS_brk, 0);
    if (initial_brk == (void*)-1) return -1;
    
    // Test 2: Expand heap
    void *new_brk = (char*)initial_brk + 4096;
    if (brk_impl(new_brk) != 0) return -1;
    
    // Test 3: Verify expansion
    void *verify_brk = (void*)syscall(SYS_brk, 0);
    if (verify_brk != new_brk) return -1;
    
    // Test 4: Reset to original
    if (brk_impl(initial_brk) != 0) return -1;
    
    return 0;  // All tests passed
}
```

---

#### sbrk - Increment Program Break
```bash
# Path: arch/x86_64/level_0_primitives/memory_management/sbrk/
```

**Pattern Implementazione**:
```cpp
void* sbrk_impl(intptr_t increment) {
    // 1. Ottieni program break attuale
    void* old_brk = (void*)syscall(SYS_brk, 0);
    if (old_brk == (void*)-1) {
        return (void*)-1;
    }
    
    // 2. Se increment è 0, ritorna solo il valore attuale
    if (increment == 0) {
        return old_brk;
    }
    
    // 3. Calcola nuovo break
    void* new_brk = (char*)old_brk + increment;
    
    // 4. Validazione overflow
    if (increment > 0 && new_brk < old_brk) {
        errno = ENOMEM;  // Overflow
        return (void*)-1;
    }
    
    if (increment < 0 && new_brk > old_brk) {
        errno = ENOMEM;  // Underflow
        return (void*)-1;
    }
    
    // 5. Imposta nuovo break
    void* result_brk = (void*)syscall(SYS_brk, new_brk);
    if (result_brk != new_brk) {
        errno = ENOMEM;
        return (void*)-1;
    }
    
    // 6. Ritorna vecchio valore
    return old_brk;
}
```

**Test Pattern**:
```cpp
int sbrk_test() {
    // Test 1: Query (increment = 0)
    void *current = sbrk_impl(0);
    if (current == (void*)-1) return -1;
    
    // Test 2: Positive increment
    void *after_inc = sbrk_impl(4096);
    if (after_inc == (void*)-1) return -1;
    if (after_inc != current) return -1;
    
    // Test 3: Verify new break
    void *new_current = sbrk_impl(0);
    if (new_current != (char*)current + 4096) return -1;
    
    // Test 4: Negative increment (contraction)
    void *after_dec = sbrk_impl(-4096);
    if (after_dec != new_current) return -1;
    
    return 0;
}
```

---

#### mmap - Memory Mapping
```bash
# Path: arch/x86_64/level_0_primitives/memory_management/mmap/
```

**Pattern Implementazione Complessa**:
```cpp
void* mmap_impl(void *addr, size_t length, int prot, int flags, int fd, off_t offset) {
    // 1. Validazioni parametri
    if (length == 0) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 2. Validazione flags obbligatori
    if (!(flags & MAP_SHARED) && !(flags & MAP_PRIVATE)) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 3. Validazione per file mapping
    if (!(flags & MAP_ANONYMOUS)) {
        if (fd < 0) {
            errno = EBADF;
            return MAP_FAILED;
        }
        
        // Verifica che il file descriptor sia valido
        if (fcntl(fd, F_GETFD) == -1) {
            errno = EBADF;
            return MAP_FAILED;
        }
        
        // Validazione allineamento offset
        long page_size = sysconf(_SC_PAGESIZE);
        if (offset % page_size != 0) {
            errno = EINVAL;
            return MAP_FAILED;
        }
    }
    
    // 4. Validazione protezioni
    if (prot & ~(PROT_READ | PROT_WRITE | PROT_EXEC | PROT_NONE)) {
        errno = EINVAL;
        return MAP_FAILED;
    }
    
    // 5. Chiamata syscall
    #ifdef __x86_64__
    void* result = (void*)syscall(SYS_mmap, addr, length, prot, flags, fd, offset);
    #elif defined(__i386__)
    // Su i386 mmap ha una calling convention diversa
    void* result = (void*)syscall(SYS_mmap2, addr, length, prot, flags, fd, offset >> 12);
    #endif
    
    // 6. Gestione errori
    if (result == MAP_FAILED) {
        // errno già impostato dal kernel
        return MAP_FAILED;
    }
    
    return result;
}
```

**Test Pattern Completo**:
```cpp
int mmap_test() {
    size_t page_size = sysconf(_SC_PAGESIZE);
    
    // Test 1: Anonymous mapping
    void *anon_map = mmap_impl(NULL, page_size, PROT_READ | PROT_WRITE, 
                              MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (anon_map == MAP_FAILED) return -1;
    
    // Test 2: Write to mapped memory
    *(char*)anon_map = 'A';
    if (*(char*)anon_map != 'A') return -1;
    
    // Test 3: Unmap
    if (munmap(anon_map, page_size) != 0) return -1;
    
    // Test 4: File mapping
    int fd = open("/dev/zero", O_RDONLY);
    if (fd == -1) return -1;
    
    void *file_map = mmap_impl(NULL, page_size, PROT_READ, 
                              MAP_PRIVATE, fd, 0);
    close(fd);
    
    if (file_map == MAP_FAILED) return -1;
    
    // Test 5: Read from file mapping
    char test_byte = *(char*)file_map;
    if (test_byte != 0) return -1;  // /dev/zero should give zero
    
    // Test 6: Unmap file mapping
    if (munmap(file_map, page_size) != 0) return -1;
    
    return 0;
}
```

---

#### munmap - Unmap Memory
#### mprotect - Change Memory Protection
#### msync - Synchronize Memory Mapping

*[Pattern simili con validazioni specifiche]*

---

### 🆔 process_identity (2 sviluppatori)

#### getpid - Process ID
```bash
# Path: arch/x86_64/level_0_primitives/process_identity/getpid/
```

**Pattern Implementazione**:
```cpp
pid_t getpid_impl(void) {
    // getpid non può mai fallire secondo POSIX
    #ifdef __x86_64__
    pid_t result = (pid_t)syscall(SYS_getpid);
    #elif defined(__i386__)
    pid_t result = (pid_t)syscall(SYS_getpid);
    #endif
    
    // Non dovrebbe mai essere necessario, ma per sicurezza
    if (result <= 0) {
        // Questo non dovrebbe mai accadere
        errno = ESRCH;
        return -1;
    }
    
    return result;
}
```

**Test Pattern**:
```cpp
int getpid_test() {
    // Test 1: Basic functionality
    pid_t pid1 = getpid_impl();
    if (pid1 <= 0) return -1;
    
    // Test 2: Consistency
    pid_t pid2 = getpid_impl();
    if (pid1 != pid2) return -1;
    
    // Test 3: Compare with system getpid
    pid_t sys_pid = getpid();
    if (pid1 != sys_pid) return -1;
    
    return 0;
}
```

#### getppid - Parent Process ID
#### getuid - User ID  
#### geteuid - Effective User ID
#### getgid - Group ID
#### getegid - Effective Group ID

*[Pattern identici con syscall specifiche]*

---

### 📁 basic_io (2 sviluppatori)

#### read - Read from File Descriptor
```bash
# Path: arch/x86_64/level_0_primitives/basic_io/read/
```

**Pattern Implementazione**:
```cpp
ssize_t read_impl(int fd, void *buf, size_t count) {
    // 1. Validazioni parametri
    if (buf == NULL && count > 0) {
        errno = EFAULT;
        return -1;
    }
    
    if (fd < 0) {
        errno = EBADF;
        return -1;
    }
    
    // 2. Caso speciale count = 0
    if (count == 0) {
        return 0;
    }
    
    // 3. Validazione che fd sia aperto per lettura
    int flags = fcntl(fd, F_GETFL);
    if (flags == -1) {
        errno = EBADF;
        return -1;
    }
    
    int access_mode = flags & O_ACCMODE;
    if (access_mode == O_WRONLY) {
        errno = EBADF;
        return -1;
    }
    
    // 4. Chiamata syscall con restart su EINTR
    ssize_t result;
    do {
        #ifdef __x86_64__
        result = syscall(SYS_read, fd, buf, count);
        #elif defined(__i386__)
        result = syscall(SYS_read, fd, buf, count);
        #endif
    } while (result == -1 && errno == EINTR);
    
    return result;
}
```

**Test Pattern Completo**:
```cpp
int read_test() {
    // Test 1: Read from /dev/zero
    int fd = open("/dev/zero", O_RDONLY);
    if (fd == -1) return -1;
    
    char buffer[100];
    ssize_t bytes_read = read_impl(fd, buffer, sizeof(buffer));
    if (bytes_read != sizeof(buffer)) {
        close(fd);
        return -1;
    }
    
    // Verify all zeros
    for (size_t i = 0; i < sizeof(buffer); i++) {
        if (buffer[i] != 0) {
            close(fd);
            return -1;
        }
    }
    close(fd);
    
    // Test 2: Read with count = 0
    fd = open("/dev/null", O_RDONLY);
    if (fd == -1) return -1;
    
    bytes_read = read_impl(fd, buffer, 0);
    if (bytes_read != 0) {
        close(fd);
        return -1;
    }
    close(fd);
    
    // Test 3: Invalid fd
    bytes_read = read_impl(-1, buffer, sizeof(buffer));
    if (bytes_read != -1 || errno != EBADF) return -1;
    
    // Test 4: NULL buffer with count > 0
    bytes_read = read_impl(0, NULL, 10);
    if (bytes_read != -1 || errno != EFAULT) return -1;
    
    return 0;
}
```

#### write - Write to File Descriptor
#### open - Open File  
#### close - Close File Descriptor
#### lseek - Seek in File

*[Pattern simili con validazioni specifiche]*

---

## 🏗️ TEAM LEVEL 1 - FUNDAMENTAL OPERATIONS

### 📂 filesystem_ops (3 sviluppatori)

#### stat - File Status
```bash
# Path: arch/x86_64/level_1_fundamental/filesystem_ops/stat/
```

**Pattern Implementazione**:
```cpp
int stat_impl(const char *pathname, struct stat *statbuf) {
    // 1. Validazioni parametri
    if (pathname == NULL) {
        errno = EFAULT;
        return -1;
    }
    
    if (statbuf == NULL) {
        errno = EFAULT;
        return -1;
    }
    
    if (strlen(pathname) == 0) {
        errno = ENOENT;
        return -1;
    }
    
    // 2. Validazione lunghezza path
    if (strlen(pathname) >= PATH_MAX) {
        errno = ENAMETOOLONG;
        return -1;
    }
    
    // 3. Chiamata syscall
    #ifdef __x86_64__
    int result = syscall(SYS_stat, pathname, statbuf);
    #elif defined(__i386__)
    int result = syscall(SYS_stat64, pathname, statbuf);
    #endif
    
    return result;
}
```

#### fstat - File Status by Descriptor
#### lstat - Link Status
#### access - Check Access Permissions
#### chmod - Change File Permissions
#### chown - Change File Ownership
#### link - Create Hard Link
#### unlink - Remove Link
#### rename - Rename File
#### mkdir - Create Directory
#### rmdir - Remove Directory

---

### ⚙️ process_control (3 sviluppatori)

#### fork - Create Child Process
```bash
# Path: arch/x86_64/level_1_fundamental/process_control/fork/
```

**Pattern Implementazione Critica**:
```cpp
pid_t fork_impl(void) {
    // 1. Pre-fork preparation
    fflush(NULL);  // Flush all open streams
    
    // 2. Chiamata syscall
    #ifdef __x86_64__
    pid_t result = syscall(SYS_fork);
    #elif defined(__i386__)
    pid_t result = syscall(SYS_fork);
    #endif
    
    // 3. Post-fork handling
    if (result == 0) {
        // Child process
        // Reset certain signal handlers if needed
        // Child-specific initialization
        return 0;
    } else if (result > 0) {
        // Parent process
        return result;  // Child PID
    } else {
        // Error occurred
        return -1;
    }
}
```

**Test Pattern Ultra-Completo**:
```cpp
int fork_test() {
    // Test 1: Basic fork
    pid_t child_pid = fork_impl();
    
    if (child_pid == 0) {
        // Child process
        exit(42);  // Exit with specific code
    } else if (child_pid > 0) {
        // Parent process
        int status;
        pid_t waited = wait(&status);
        
        if (waited != child_pid) return -1;
        if (!WIFEXITED(status)) return -1;
        if (WEXITSTATUS(status) != 42) return -1;
    } else {
        return -1;  // Fork failed
    }
    
    // Test 2: Memory separation
    int shared_var = 100;
    child_pid = fork_impl();
    
    if (child_pid == 0) {
        shared_var = 200;
        exit(shared_var & 0xFF);
    } else if (child_pid > 0) {
        int status;
        wait(&status);
        
        // Parent's variable should be unchanged
        if (shared_var != 100) return -1;
        if (WEXITSTATUS(status) != 200) return -1;
    } else {
        return -1;
    }
    
    return 0;
}
```

#### execve - Execute Program
#### wait - Wait for Child
#### waitpid - Wait for Specific Child
#### exit - Terminate Process
#### kill - Send Signal

---

### 📡 signal_handling (2 sviluppatori)

#### signal - Set Signal Handler
#### sigaction - Advanced Signal Handling
#### pause - Wait for Signal
#### alarm - Set Alarm

---

## 🔧 TEAM LEVEL 2 - INTERMEDIATE OPERATIONS

### 📨 advanced_io (2 sviluppatori)

#### dup - Duplicate File Descriptor
```bash
# Path: arch/x86_64/level_2_intermediate/advanced_io/dup/
```

**Pattern Implementazione**:
```cpp
int dup_impl(int oldfd) {
    // 1. Validazione fd
    if (oldfd < 0) {
        errno = EBADF;
        return -1;
    }
    
    // 2. Verifica che oldfd sia valido
    if (fcntl(oldfd, F_GETFD) == -1) {
        errno = EBADF;
        return -1;
    }
    
    // 3. Chiamata syscall
    #ifdef __x86_64__
    int result = syscall(SYS_dup, oldfd);
    #elif defined(__i386__)
    int result = syscall(SYS_dup, oldfd);
    #endif
    
    return result;
}
```

#### dup2 - Duplicate to Specific FD
#### pipe - Create Pipe
#### fcntl - File Control
#### ioctl - I/O Control
#### select - Synchronous I/O Multiplexing
#### poll - Poll File Descriptors

---

### 📁 directory_ops (2 sviluppatori)

#### opendir - Open Directory Stream
#### readdir - Read Directory Entry
#### closedir - Close Directory Stream
#### rewinddir - Rewind Directory Stream
#### seekdir - Seek in Directory
#### telldir - Tell Directory Position

---

### ⏰ time_ops (1 sviluppatore)

#### time - Get Current Time
#### gettimeofday - Get Time with Microseconds
#### clock - Get Process Time
#### sleep - Sleep for Seconds
#### nanosleep - High Precision Sleep

---

## 🌐 TEAM LEVEL 3 - COMPLEX OPERATIONS

### 📬 ipc_sysv (3 sviluppatori)

#### Message Queues
```bash
# msgget - arch/x86_64/level_3_complex/ipc_sysv/msgget/
```

**Pattern msgget**:
```cpp
int msgget_impl(key_t key, int msgflg) {
    // 1. Validazione key
    if (key == (key_t)-1) {
        errno = EINVAL;
        return -1;
    }
    
    // 2. Validazione flags
    int valid_flags = IPC_CREAT | IPC_EXCL | 0777;
    if (msgflg & ~valid_flags) {
        errno = EINVAL;
        return -1;
    }
    
    // 3. Chiamata syscall
    #ifdef __x86_64__
    int result = syscall(SYS_msgget, key, msgflg);
    #elif defined(__i386__)
    int result = syscall(SYS_msgget, key, msgflg);
    #endif
    
    return result;
}
```

#### msgsnd - Send Message
#### msgrcv - Receive Message  
#### msgctl - Message Control

#### Semaphores
#### semget - Get Semaphore Set
#### semop - Semaphore Operations
#### semctl - Semaphore Control

#### Shared Memory
#### shmget - Get Shared Memory
#### shmat - Attach Shared Memory
#### shmdt - Detach Shared Memory
#### shmctl - Shared Memory Control

---

### 🌍 networking (3 sviluppatori)

#### socket - Create Socket
```bash
# Path: arch/x86_64/level_3_complex/networking/socket/
```

**Pattern Implementazione**:
```cpp
int socket_impl(int domain, int type, int protocol) {
    // 1. Validazione domain
    switch (domain) {
        case AF_UNIX:
        case AF_INET:
        case AF_INET6:
            break;
        default:
            errno = EAFNOSUPPORT;
            return -1;
    }
    
    // 2. Validazione type
    int base_type = type & ~(SOCK_CLOEXEC | SOCK_NONBLOCK);
    switch (base_type) {
        case SOCK_STREAM:
        case SOCK_DGRAM:
        case SOCK_RAW:
            break;
        default:
            errno = EINVAL;
            return -1;
    }
    
    // 3. Chiamata syscall
    #ifdef __x86_64__
    int result = syscall(SYS_socket, domain, type, protocol);
    #elif defined(__i386__)
    int result = syscall(SYS_socketcall, SYS_SOCKET, 
                        (unsigned long[]){domain, type, protocol});
    #endif
    
    return result;
}
```

#### bind - Bind Socket to Address
#### listen - Listen for Connections
#### accept - Accept Connection
#### connect - Connect to Remote Address
#### send - Send Data
#### recv - Receive Data
#### sendto - Send Data to Address
#### recvfrom - Receive Data from Address
#### shutdown - Shutdown Socket Connection

---

### 👥 session_control (1 sviluppatore)

#### setsid - Create Session
#### getsid - Get Session ID
#### setpgid - Set Process Group
#### getpgid - Get Process Group ID
#### getpgrp - Get Process Group

---

## 🔒 TEAM LEVEL 4 - HIGH-LEVEL OPERATIONS

### 🛡️ security (2 sviluppatori)

#### setuid - Set User ID
#### setgid - Set Group ID
#### seteuid - Set Effective User ID
#### setegid - Set Effective Group ID
#### getgroups - Get Group List
#### setgroups - Set Group List

---

### 💾 filesystem_advanced (2 sviluppatori)

#### mount - Mount Filesystem
#### umount - Unmount Filesystem
#### sync - Synchronize Filesystems
#### fsync - Synchronize File
#### fdatasync - Synchronize File Data
#### truncate - Truncate File to Length
#### ftruncate - Truncate File by FD

---

### 📊 resource_control (1 sviluppatore)

#### getrlimit - Get Resource Limits
#### setrlimit - Set Resource Limits
#### getrusage - Get Resource Usage
#### times - Get Process Times

---

## 🎯 TEAM LEVEL 5 - SPECIALIZED OPERATIONS

### ⚙️ configuration (1 sviluppatore)

#### pathconf - Get Path Configuration
#### fpathconf - Get FD Configuration
#### sysconf - Get System Configuration
#### confstr - Get Configuration String

---

### ⚡ async_io (2 sviluppatori)

#### aio_read - Asynchronous Read
#### aio_write - Asynchronous Write
#### aio_error - Check Async I/O Error
#### aio_return - Get Async I/O Return
#### aio_cancel - Cancel Async I/O
#### aio_suspend - Suspend for Async I/O

---

### 🧵 posix_threads (3 sviluppatori)

#### pthread_create - Create Thread
#### pthread_join - Join Thread
#### pthread_detach - Detach Thread
#### pthread_exit - Exit Thread
#### pthread_mutex_init - Initialize Mutex
#### pthread_mutex_lock - Lock Mutex
#### pthread_mutex_unlock - Unlock Mutex

---

## 📋 PATTERN GENERALI PER TUTTI I MODULI

### Template Struttura Implementazione
```cpp
return_type syscall_impl(parameters...) {
    // 1. VALIDAZIONE PARAMETRI
    if (/* invalid params */) {
        errno = APPROPRIATE_ERROR;
        return ERROR_VALUE;
    }
    
    // 2. PRE-PROCESSING
    // - Conversioni necessarie
    // - Setup stato interno
    
    // 3. CHIAMATA SYSCALL ARCHITETTURA-SPECIFICA
    #ifdef __x86_64__
    result_type result = syscall(SYS_syscall_name, params...);
    #elif defined(__i386__)
    result_type result = syscall(SYS_syscall_name, params...);
    #endif
    
    // 4. POST-PROCESSING
    // - Gestione valore ritorno
    // - Cleanup se necessario
    
    // 5. GESTIONE ERRORI
    if (result == ERROR_INDICATOR) {
        // errno già impostato dal kernel in molti casi
        return ERROR_VALUE;
    }
    
    return result;
}
```

### Template Test Completo
```cpp
int syscall_test() {
    // Test 1: Caso normale (happy path)
    result = syscall_impl(valid_params);
    if (result != expected) return -1;
    
    // Test 2: Parametri invalidi
    result = syscall_impl(invalid_params);
    if (result != -1 || errno != EXPECTED_ERROR) return -1;
    
    // Test 3: Edge cases
    // - Valori limite
    // - Casi speciali
    
    // Test 4: Integrazione con altre syscall
    // - Verifica funzionamento in contesto reale
    
    // Test 5: Performance basic
    // - Verifica che non sia irragionevolmente lenta
    
    return 0;  // Tutti i test passati
}
```

### Pattern Gestione Errori Comune
```cpp
// Errori POSIX standard per validazione parametri:
errno = EINVAL;   // Invalid argument
errno = EFAULT;   // Bad address
errno = EBADF;    // Bad file descriptor
errno = ENOENT;   // No such file or directory
errno = EACCES;   // Permission denied
errno = ENOMEM;   // Out of memory
errno = ENOSYS;   // Function not implemented
errno = EAGAIN;   // Resource temporarily unavailable
errno = EINTR;    // Interrupted system call
```

### Pattern Documentazione Modulo
```markdown
# syscall_name - Descrizione Breve

## Implementazione
- [x] Validazione parametri completa
- [x] Chiamata syscall architettura-specifica
- [x] Gestione errori POSIX-compliant
- [x] Test coverage completo

## Test Coperti
- Funzionalità base
- Parametri invalidi
- Edge cases
- Integrazione

## Note POSIX
- Standard: POSIX.1-2017
- Comportamento: [Descrizione conforme POSIX]
- Limitazioni: [Se esistenti]
```

---

## 🚨 REGOLE CRITICHE PER OGNI MODULO

### ❌ BLOCKERS ASSOLUTI
1. **NON** implementare senza pattern completo di validazione
2. **NON** saltare test di edge cases
3. **NON** ignorare gestione errori errno
4. **NON** usare syscall non standard
5. **NON** omettere controlli architettura-specifici

### ✅ QUALITY GATES PER MODULO
1. **Compilazione clean** (`make debug`)
2. **Test completi** (`make check`)
3. **Valgrind clean** (nessun leak)
4. **Pattern conforme** (validazione + syscall + errori)
5. **Documentazione** (template completato)

### 🔄 WORKFLOW PER OGNI SYSCALL
```bash
# 1. Setup modulo
python3 project_utilities.py wizard

# 2. Implementa pattern specifico
# - Copia pattern dalla guida
# - Adatta parametri specifici
# - Completa validazioni

# 3. Test completo
make check

# 4. Validazione
make analyze
valgrind ./modulo_name

# 5. Documentazione
# - Aggiorna .md con stato reale
# - Note implementazione specifiche

# 6. Review e commit
# - Code review obbligatorio
# - Commit solo dopo approvazione
```

Ogni sviluppatore deve seguire esattamente questi pattern per garantire consistenza e qualità nell'intero progetto.
