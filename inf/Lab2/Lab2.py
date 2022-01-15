res = list(map(int, input()))
print("input msg: ", *res)

if len(res) != 7:
        print("Wrong num of bits")
        exit()

s1 = res[0] ^ res[2] ^ res[4] ^ res[6]
s2 = res[1] ^ res[2] ^ res[5] ^ res[6]
s3 = res[3] ^ res[4] ^ res[5] ^ res[6]

ind = int(str(s3 * 100 + s2 * 10 + s1), 2) - 1
if ind == -1:
	print("no error")
else:
	res[ind] = 0 if res[ind] == 1 else 1
	print("correct message: ", *res)
	print("error at ind: ", ind)
print("information : ", res[2],  res[4],  res[5], res[6])
