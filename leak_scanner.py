import os
import re
import sys

# Arjumand Labs - Terminal Colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

LEAK_TARGETS = {
    "StreamController": "close",
    "TextEditingController": "dispose",
    "AnimationController": "dispose",
    "ScrollController": "dispose",
    "FocusNode": "dispose",
    "Timer": "cancel"
}

def scan_dart_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    leaks_found = []

    for target, cleanup_method in LEAK_TARGETS.items():
        # Find variable names instantiated with the target (e.g., StreamController _controller = ...)
        pattern = rf"{target}(?:<[^>]+>)?\s+([a-zA-Z0-9_]+)\s*(?:=|;)"
        matches = re.finditer(pattern, content)
        
        for match in matches:
            var_name = match.group(1)
            # Check if the cleanup method is called on this variable (e.g., _controller.close())
            cleanup_pattern = rf"{var_name}\.{cleanup_method}\(\)"
            if not re.search(cleanup_pattern, content):
                leaks_found.append(f"{var_name} (Missing .{cleanup_method}())")

    return leaks_found

def main(directory="lib"):
    print(f"\n{Colors.BOLD}{Colors.BLUE}🚀 [Arjumand Labs] Flutter Memory Leak Scanner{Colors.ENDC}")
    print("-" * 50)

    if not os.path.exists(directory):
        print(f"{Colors.FAIL}❌ Error: Directory '{directory}' not found. Run this in a Flutter project root.{Colors.ENDC}\n")
        sys.exit(1)

    total_files = 0
    leaky_files = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.dart'):
                total_files += 1
                filepath = os.path.join(root, file)
                leaks = scan_dart_file(filepath)

                if leaks:
                    leaky_files += 1
                    print(f"{Colors.FAIL}⚠️  LEAK DETECTED: {filepath}{Colors.ENDC}")
                    for leak in leaks:
                        print(f"   ↳ {Colors.WARNING}{leak}{Colors.ENDC}")

    print("-" * 50)
    if leaky_files == 0:
        print(f"{Colors.GREEN}🎉 SUCCESS: Scanned {total_files} files. No obvious memory leaks found!{Colors.ENDC}\n")
    else:
        print(f"{Colors.FAIL}🚨 SCAN COMPLETE: Found missing dispose/close calls in {leaky_files} out of {total_files} files.{Colors.ENDC}\n")

if __name__ == "__main__":
    scan_dir = sys.argv[1] if len(sys.argv) > 1 else "lib"
    main(scan_dir)