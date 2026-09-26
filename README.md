# 🔍 Flutter Memory Leak Scanner

> A static analysis Python script that scans Flutter codebases to detect orphaned controllers, unclosed streams, and zombie timers. Built by **Arjumand Labs**.

### 🛑 The Problem
Flutter memory leaks usually happen when a widget is destroyed, but its background processes are not. If you forget to call `.dispose()` on a `TextEditingController` or `.close()` on a `StreamController`, the Dart Garbage Collector cannot clear it from memory. Over time, these orphaned listeners stack up, draining battery and eventually crashing the app (OOM).

### 💡 The Solution
Instead of manually hunting through the Flutter DevTools memory profiler, drop this lightweight Python script into your project. It uses regex to traverse your entire `lib/` directory, identifying exactly which files instantiated controllers/streams but forgot to clean them up.

### ⚙️ What It Detects
*   `StreamController` missing `.close()`
*   `TextEditingController`, `AnimationController`, `ScrollController`, `FocusNode` missing `.dispose()`
*   `Timer` missing `.cancel()`

### 🛠️ Quickstart

**1. Run the Scanner**
Run the script from the root of any Flutter project:
```bash
python leak_scanner.py