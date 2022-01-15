import timeit

print(
    timeit.timeit('import Lab4_1\nLab4_1.convert(open("Wednesday.xml", encoding="UTF-8"), open("tmp.yaml", encoding="UTF-8", mode="w+"))', number=10)
)
print(
    timeit.timeit('import Lab4_2\nLab4_2.convert(open("Wednesday.xml", encoding="UTF-8"), open("tmp.yaml", encoding="UTF-8", mode="w+"))', number=10)
)
print(
    timeit.timeit('import Lab4_3\nLab4_3.convert(open("Wednesday.xml", encoding="UTF-8"), open("tmp.yaml", encoding="UTF-8", mode="w+"))', number=10)
)