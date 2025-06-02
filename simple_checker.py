#!/usr/bin/env python3

"""
Controllo semplice e veloce dello stato del progetto
"""

import subprocess
import sys
from pathlib import Path

def check_module_status(module_dir):
    """Controlla stato di un singolo modulo con analisi contenuto"""
    module_name = module_dir.name
    required_files = [f"{module_name}.cpp", f"{module_name}.h", "Makefile", f"{module_name}.md", "test.py"]
    
    status = {
        "name": module_name,
        "path": str(module_dir),
        "files": {},
        "complete": True,
        "has_content": True,
        "has_implementation": True
    }
    
    implemented_files = 0
    
    for req_file in required_files:
        file_path = module_dir / req_file
        
        if file_path.exists():
            size = file_path.stat().st_size
            if size > 0:
                # Analizza se è implementato o solo template
                is_implemented = analyze_file_implementation(file_path, req_file)
                
                status["files"][req_file] = {
                    "exists": True, 
                    "size": size, 
                    "empty": False,
                    "implemented": is_implemented
                }
                
                if is_implemented:
                    implemented_files += 1
                else:
                    status["has_implementation"] = False
            else:
                status["files"][req_file] = {"exists": True, "size": 0, "empty": True, "implemented": False}
                status["complete"] = False
                status["has_content"] = False
                status["has_implementation"] = False
        else:
            status["files"][req_file] = {"exists": False, "size": 0, "empty": True, "implemented": False}
            status["complete"] = False
            status["has_content"] = False
            status["has_implementation"] = False
    
    # Aggiorna stato basato su implementazione reale
    status["implementation_ratio"] = implemented_files / len(required_files)
    status["complete"] = status["complete"] and status["has_implementation"]
    
    return status

def analyze_file_implementation(file_path, file_type):
    """Analizza se un file contiene implementazione reale o solo template"""
    try:
        content = file_path.read_text()
        
        # Indicatori di template/stub
        stub_indicators = [
            "TODO:", "FIXME:", "Not implemented", "ENOSYS", 
            "errno = ENOSYS", "da implementare", "stub"
        ]
        
        # Indicatori di implementazione
        impl_indicators = [
            "syscall(", "return syscall", "#ifdef __x86_64__",
            "real implementation"
        ]
        
        # Conta linee effettive (non commenti/vuote)
        lines = [line.strip() for line in content.splitlines() 
                if line.strip() and not line.strip().startswith('//')]
        
        if len(lines) < 10:  # Troppo piccolo per essere implementato
            return False
        
        # Cerca indicatori
        stub_count = sum(1 for line in lines 
                        for indicator in stub_indicators 
                        if indicator.lower() in line.lower())
        
        impl_count = sum(1 for line in lines 
                        for indicator in impl_indicators 
                        if indicator.lower() in line.lower())
        
        # Logica basata su tipo file
        if file_type.endswith('.cpp'):
            return impl_count > 0 and stub_count < len(lines) * 0.2
        elif file_type.endswith('.h'):
            return len(lines) > 15 and stub_count < 3
        elif file_type == "Makefile":
            return "$(CXX)" in content and ".cpp:" in content
        elif file_type.endswith('.md'):
            return len(lines) > 50 and stub_count < 5
        elif file_type.endswith('.py'):
            return "subprocess" in content and len(lines) > 60
        
        return len(lines) > 20 and stub_count < len(lines) * 0.3
        
    except Exception:
        return False

def check_module_functionality(module_dir):
    """Verifica funzionalità effettiva del modulo"""
    module_name = module_dir.name
    
    # Verifica se può compilare
    makefile = module_dir / "Makefile"
    can_compile = False
    compile_error = ""
    
    if makefile.exists():
        try:
            result = subprocess.run(
                ["make", "clean"], 
                cwd=module_dir, 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            result = subprocess.run(
                ["make", "debug"], 
                cwd=module_dir, 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            
            if result.returncode == 0:
                executable = module_dir / module_name
                can_compile = executable.exists()
                
                if can_compile:
                    # Prova esecuzione
                    exec_result = subprocess.run(
                        [str(executable)],
                        cwd=module_dir,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    # Se esegue senza crash, è funzionale
                    can_compile = exec_result.returncode in [0, -1]  # -1 per ENOSYS va bene
            else:
                compile_error = result.stderr[:100]
                
        except Exception as e:
            compile_error = str(e)[:100]
    
    return can_compile, compile_error

def comprehensive_check():
    """Controllo completo con distinzione implementazione/template"""
    project_root = Path("/home/sh/progetti/CIPOLLA")
    
    print("CONTROLLO COMPLETO PROGETTO - IMPLEMENTAZIONI REALI")
    print("=" * 60)
    
    stats = {
        "total": 0,
        "fully_implemented": 0,
        "partially_implemented": 0,
        "template_only": 0,
        "empty": 0,
        "compile_errors": []
    }
    
    for arch in ["x86_64", "x86_32"]:
        arch_path = project_root / "arch" / arch
        if not arch_path.exists():
            print(f"{arch}: DIRECTORY MANCANTE")
            continue
        
        print(f"\n{arch}:")
        module_count = 0
        
        for module_dir in arch_path.rglob("*"):
            if module_dir.is_dir() and any(module_dir.iterdir()):
                cpp_files = list(module_dir.glob("*.cpp"))
                if cpp_files:
                    module_count += 1
                    stats["total"] += 1
                    
                    status = check_module_status(module_dir)
                    impl_ratio = status["implementation_ratio"]
                    
                    if impl_ratio >= 0.9:
                        state = "IMPLEMENTED"
                        stats["fully_implemented"] += 1
                    elif impl_ratio >= 0.5:
                        state = "PARTIAL_IMPL"
                        stats["partially_implemented"] += 1
                    elif impl_ratio > 0:
                        state = "TEMPLATE_ONLY"
                        stats["template_only"] += 1
                    else:
                        state = "EMPTY"
                        stats["empty"] += 1
                    
                    print(f"  {module_count:3d}. {status['name']:<25} [{state} - {impl_ratio*100:.0f}%]")
    
    # Riepilogo finale
    print(f"\nRIEPILOGO FINALE:")
    print(f"Totale moduli: {stats['total']}")
    print(f"Completamente implementati: {stats['fully_implemented']}")
    print(f"Parzialmente implementati: {stats['partially_implemented']}")
    print(f"Solo template: {stats['template_only']}")
    print(f"Vuoti: {stats['empty']}")
    
    if stats["total"] > 0:
        impl_rate = stats["fully_implemented"] / stats["total"] * 100
        partial_rate = (stats["fully_implemented"] + stats["partially_implemented"]) / stats["total"] * 100
        print(f"Percentuale implementazione completa: {impl_rate:.1f}%")
        print(f"Percentuale con implementazione parziale: {partial_rate:.1f}%")

def main():
    project_root = Path("/home/sh/progetti/CIPOLLA")
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "summary":
            # Solo riepilogo
            total = 0
            complete = 0
            partial = 0
            empty = 0
            
            for arch in ["x86_64", "x86_32"]:
                arch_path = project_root / "arch" / arch
                if not arch_path.exists():
                    continue
                
                for module_dir in arch_path.rglob("*"):
                    if module_dir.is_dir() and any(module_dir.iterdir()):
                        # Se la directory ha file, considerala un modulo
                        cpp_files = list(module_dir.glob("*.cpp"))
                        if cpp_files:
                            total += 1
                            status = check_module_status(module_dir)
                            
                            if status["complete"] and status["has_content"]:
                                complete += 1
                            elif any(f["exists"] and not f["empty"] for f in status["files"].values()):
                                partial += 1
                            else:
                                empty += 1
            
            print(f"RIEPILOGO RAPIDO:")
            print(f"Totale moduli: {total}")
            print(f"Completi: {complete}")
            print(f"Parziali: {partial}")
            print(f"Vuoti: {empty}")
            print(f"Percentuale completamento: {complete/total*100:.1f}%" if total > 0 else "0%")
            
        elif sys.argv[1] == "full":
            comprehensive_check()
        else:
            print("Opzioni: summary, full")
    else:
        # Lista dettagliata
        print("CONTROLLO RAPIDO MODULI")
        print("=" * 50)
        
        for arch in ["x86_64", "x86_32"]:
            arch_path = project_root / "arch" / arch
            if not arch_path.exists():
                print(f"ARCH {arch}: MANCANTE")
                continue
            
            print(f"\nARCH {arch}:")
            count = 0
            
            for module_dir in arch_path.rglob("*"):
                if module_dir.is_dir() and any(module_dir.iterdir()):
                    cpp_files = list(module_dir.glob("*.cpp"))
                    if cpp_files:
                        count += 1
                        status = check_module_status(module_dir)
                        
                        if status["complete"] and status["has_content"]:
                            state = "OK"
                        elif any(f["exists"] and not f["empty"] for f in status["files"].values()):
                            state = "PARTIAL"
                        else:
                            state = "EMPTY"
                        
                        print(f"  {count:3d}. {status['name']:<20} [{state}]")
                        
                        # Mostra problemi
                        problems = []
                        for fname, finfo in status["files"].items():
                            if not finfo["exists"]:
                                problems.append(f"{fname}:MISSING")
                            elif finfo["empty"]:
                                problems.append(f"{fname}:EMPTY")
                        
                        if problems:
                            print(f"       Issues: {', '.join(problems)}")

if __name__ == "__main__":
    main()
