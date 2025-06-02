# // filepath: /home/sh/progetti/CIPOLLA/posix_syscalls_map.md
# Mappa Completa delle System Call POSIX

## Livello 0 - Primitive di Base del Kernel

### Gestione Memoria Base
- `brk()` - Modifica il program break
- `sbrk()` - Incrementa/decrementa il program break
- `mmap()` - Mappa memoria
- `munmap()` - Rilascia memoria mappata
- `mprotect()` - Cambia protezioni memoria
- `msync()` - Sincronizza memoria mappata

### Gestione Processi Base
- `getpid()` - ID processo corrente
- `getppid()` - ID processo padre
- `getuid()` - User ID reale
- `geteuid()` - User ID effettivo
- `getgid()` - Group ID reale
- `getegid()` - Group ID effettivo

### I/O Primitivo
- `read()` - Legge da file descriptor
- `write()` - Scrive su file descriptor
- `open()` - Apre file
- `close()` - Chiude file descriptor
- `lseek()` - Posiziona puntatore file

## Livello 1 - Operazioni di Sistema Fondamentali

### Gestione File System
- `stat()` - Informazioni file (dipende da open)
- `fstat()` - Informazioni file descriptor
- `lstat()` - Informazioni link simbolico
- `access()` - Verifica permessi accesso
- `chmod()` - Cambia permessi file
- `chown()` - Cambia proprietario file
- `link()` - Crea hard link
- `unlink()` - Rimuove file
- `rename()` - Rinomina file
- `mkdir()` - Crea directory
- `rmdir()` - Rimuove directory

### Controllo Processi
- `fork()` - Crea processo figlio
- `exec*()` - Famiglia di funzioni exec
- `wait()` - Attende terminazione processo figlio
- `waitpid()` - Attende processo specifico
- `exit()` - Termina processo
- `kill()` - Invia segnale a processo

### Segnali Base
- `signal()` - Imposta handler segnale
- `sigaction()` - Gestione avanzata segnali
- `pause()` - Sospende fino a segnale
- `alarm()` - Imposta allarme

## Livello 2 - Operazioni di Sistema Intermedie

### I/O Avanzato
- `dup()` - Duplica file descriptor
- `dup2()` - Duplica su descriptor specifico
- `pipe()` - Crea pipe
- `fcntl()` - Controllo file descriptor
- `ioctl()` - Controllo dispositivo
- `select()` - Multiplexing I/O
- `poll()` - Polling file descriptor

### Gestione Directory
- `opendir()` - Apre directory (dipende da open)
- `readdir()` - Legge entry directory
- `closedir()` - Chiude directory
- `rewinddir()` - Riposiziona directory
- `seekdir()` - Posiziona in directory
- `telldir()` - Posizione corrente directory

### Time e Clock
- `time()` - Tempo corrente
- `gettimeofday()` - Tempo con microsecondi
- `clock()` - Tempo CPU processo
- `sleep()` - Sospende esecuzione
- `nanosleep()` - Sospensione con nanosecondi

## Livello 3 - Operazioni Complesse

### Comunicazione Inter-Processo (IPC)
- `msgget()` - Crea/accede message queue
- `msgsnd()` - Invia messaggio
- `msgrcv()` - Riceve messaggio
- `msgctl()` - Controllo message queue
- `semget()` - Crea/accede semaforo
- `semop()` - Operazioni su semaforo
- `semctl()` - Controllo semaforo
- `shmget()` - Crea/accede memoria condivisa
- `shmat()` - Allega memoria condivisa
- `shmdt()` - Stacca memoria condivisa
- `shmctl()` - Controllo memoria condivisa

### Networking (Socket)
- `socket()` - Crea socket
- `bind()` - Associa indirizzo a socket
- `listen()` - Mette socket in ascolto
- `accept()` - Accetta connessione
- `connect()` - Connette a socket remoto
- `send()` - Invia dati su socket
- `recv()` - Riceve dati da socket
- `sendto()` - Invia dati UDP
- `recvfrom()` - Riceve dati UDP
- `shutdown()` - Chiude parte connessione
- `getsockopt()` - Ottiene opzioni socket
- `setsockopt()` - Imposta opzioni socket

### Controllo Sessioni e Gruppi
- `setsid()` - Crea nuova sessione
- `getsid()` - Ottiene ID sessione
- `setpgid()` - Imposta group ID processo
- `getpgid()` - Ottiene group ID processo
- `getpgrp()` - Ottiene group ID processo corrente

## Livello 4 - Operazioni di Alto Livello

### Gestione Utenti e Sicurezza
- `setuid()` - Imposta user ID
- `setgid()` - Imposta group ID
- `seteuid()` - Imposta effective user ID
- `setegid()` - Imposta effective group ID
- `getgroups()` - Ottiene gruppi supplementari
- `setgroups()` - Imposta gruppi supplementari

### File System Avanzato
- `mount()` - Monta file system
- `umount()` - Smonta file system
- `sync()` - Sincronizza buffer
- `fsync()` - Sincronizza file specifico
- `fdatasync()` - Sincronizza dati file
- `truncate()` - Tronca file
- `ftruncate()` - Tronca file descriptor

### Controllo Risorse
- `getrlimit()` - Ottiene limiti risorse
- `setrlimit()` - Imposta limiti risorse
- `getrusage()` - Utilizzo risorse
- `times()` - Tempi processo e figli

## Livello 5 - Operazioni di Sistema Avanzate

### Gestione Attributi Estesi
- `pathconf()` - Configurazione path
- `fpathconf()` - Configurazione file descriptor
- `sysconf()` - Configurazione sistema
- `confstr()` - Stringhe configurazione

### Operazioni Asincrone
- `aio_read()` - Lettura asincrona
- `aio_write()` - Scrittura asincrona
- `aio_error()` - Stato operazione asincrona
- `aio_return()` - Risultato operazione asincrona
- `aio_cancel()` - Cancella operazione asincrona
- `aio_suspend()` - Sospende per operazioni asincrone

### Threads (POSIX Threads)
- `pthread_create()` - Crea thread
- `pthread_join()` - Attende terminazione thread
- `pthread_detach()` - Stacca thread
- `pthread_exit()` - Termina thread
- `pthread_mutex_*()` - Operazioni mutex
- `pthread_cond_*()` - Operazioni condition variable
- `pthread_rwlock_*()` - Operazioni read-write lock

## Dipendenze Principali

### Catena di Dipendenze Tipica:
1. **Hardware** → **Kernel primitives** → **Memory management**
2. **Memory management** → **Process management** → **File I/O**
3. **File I/O** → **File system operations** → **Directory operations**
4. **Process management** → **IPC** → **Networking**
5. **Basic I/O** → **Advanced I/O** → **Async I/O**

### Gruppi Funzionali:
- **Core**: getpid, read, write, open, close
- **Process**: fork, exec, wait, exit
- **Memory**: mmap, munmap, brk, sbrk
- **File**: stat, chmod, link, unlink
- **IPC**: pipe, msgget, semget, shmget
- **Network**: socket, bind, listen, accept
- **Thread**: pthread_create, pthread_mutex_*