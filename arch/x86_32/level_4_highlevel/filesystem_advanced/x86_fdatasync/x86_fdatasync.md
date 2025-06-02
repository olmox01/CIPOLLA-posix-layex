# filepath: x86_fdatasync.md

# fdatasync - 32-bit Implementation

## Descrizione
Implementazione della system call POSIX `fdatasync` per architettura 32-bit.

## Stato Implementazione
- [ ] Implementazione base
- [ ] Gestione errori
- [ ] Test unitari
- [ ] Documentazione completa
- [ ] Ottimizzazioni specifiche

## Interfaccia

### Funzioni Esportate
- `x86_fdatasync_impl()` - Implementazione principale
- `x86_fdatasync_test()` - Test di funzionamento

## Dipendenze
TODO: Elencare dipendenze da altre syscall

## Note di Implementazione
TODO: Note specifiche per l'implementazione 32-bit

## Test
```bash
make test
./x86_fdatasync
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
- [ ] Ottimizzazioni per 32-bit
