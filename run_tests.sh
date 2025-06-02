#!/bin/bash

# Script per eseguire test automatizzati del progetto POSIX Syscalls

set -e

PROJECT_ROOT="/home/sh/progetti/CIPOLLA"
cd "$PROJECT_ROOT"

echo "🧪 POSIX Syscalls - Test Runner Automatizzato"
echo "=============================================="

# Funzione per test di un'architettura
test_architecture() {
    local arch=$1
    echo ""
    echo "🏗️  Testing architettura: $arch"
    echo "--------------------------------"
    
    local arch_path="arch/$arch"
    if [ ! -d "$arch_path" ]; then
        echo "❌ Directory $arch_path non trovata"
        return 1
    fi
    
    local passed=0
    local failed=0
    local total=0
    
    # Trova tutti i moduli
    find "$arch_path" -name "test.py" | while read test_file; do
        module_dir=$(dirname "$test_file")
        module_name=$(basename "$module_dir")
        
        echo "🔍 Testing modulo: $module_name"
        
        cd "$module_dir"
        
        # Esegui test
        if python3 test.py > test_output.log 2>&1; then
            echo "  ✅ $module_name: PASSED"
            ((passed++))
        else
            echo "  ❌ $module_name: FAILED"
            echo "     Log: $module_dir/test_output.log"
            ((failed++))
        fi
        
        ((total++))
        cd "$PROJECT_ROOT"
    done
    
    echo ""
    echo "📊 Risultati $arch: $passed/$total test passati"
}

# Funzione per generare report HTML
generate_html_report() {
    echo "📄 Generando report HTML..."
    
    cat > test_report.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>POSIX Syscalls - Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f0f0f0; padding: 10px; border-radius: 5px; }
        .passed { color: green; }
        .failed { color: red; }
        .architecture { margin: 20px 0; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 POSIX Syscalls Test Report</h1>
        <p>Generato il: $(date)</p>
    </div>
EOF
    
    # Aggiungi risultati per ogni architettura
    for arch in x86_64 x86_32; do
        if [ -d "arch/$arch" ]; then
            echo "<div class='architecture'>" >> test_report.html
            echo "<h2>🏗️ Architettura: $arch</h2>" >> test_report.html
            echo "<table>" >> test_report.html
            echo "<tr><th>Modulo</th><th>Stato</th><th>Dettagli</th></tr>" >> test_report.html
            
            find "arch/$arch" -name "test.py" | while read test_file; do
                module_dir=$(dirname "$test_file")
                module_name=$(basename "$module_dir")
                
                if [ -f "$module_dir/test_output.log" ]; then
                    if grep -q "completati con successo" "$module_dir/test_output.log"; then
                        status="<span class='passed'>✅ PASSED</span>"
                    else
                        status="<span class='failed'>❌ FAILED</span>"
                    fi
                else
                    status="<span class='failed'>❓ NOT TESTED</span>"
                fi
                
                echo "<tr><td>$module_name</td><td>$status</td><td><a href='$module_dir/test_output.log'>Log</a></td></tr>" >> test_report.html
            done
            
            echo "</table>" >> test_report.html
            echo "</div>" >> test_report.html
        fi
    done
    
    echo "</body></html>" >> test_report.html
    echo "✅ Report salvato in: test_report.html"
}

# Main execution
echo "🚀 Avvio test automatizzati..."

# Test architetture
test_architecture "x86_64"
test_architecture "x86_32"

# Genera statistiche finali
echo ""
echo "📊 STATISTICHE FINALI"
echo "===================="

python3 create_project_structure.py stats

# Genera report HTML
generate_html_report

echo ""
echo "✅ Test automatizzati completati!"
echo "📄 Report disponibile in: test_report.html"
