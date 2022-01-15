cat Lab3_$1_tests/inp*.txt | grep -v "^$" | sed 's/$/\"/' | sed 's/^/\"/' | xargs -l1 python3 Lab3_$1.py
