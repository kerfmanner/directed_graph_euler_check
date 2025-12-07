# Вимоги до середовища

## C++ Компіляція

- **Компілятор:** gcc/g++ з підтримкою C++17
- **CMake:** версія 3.20 або новіша
- **Система:** Linux/macOS/Windows

## Python (для benchmark та порівняння)

- **Python:** 3.8+
- **Бібліотеки:**
  ```bash
  pip install networkx pandas matplotlib
  ```

## Збірка проекту

```bash
mkdir -p build && cd build
cmake ..
cmake --build .
```

## Запуск

```bash
./build/euler_main

./build/benchmark

python3 compare_benchmark.py

python3 visualize_benchmark.py all
```
