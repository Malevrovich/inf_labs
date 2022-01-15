def add_spaces_to_begin(deep, func, *args, **kwargs):
    def res(*args, **kwargs):
        print('  ' * deep, end='')
        func(*args, **kwargs)
    return res

print_with_space = add_spaces_to_begin(1, print)
print_with_space("abs", end='bs')