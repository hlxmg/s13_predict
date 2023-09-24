import s13_predict
from collections import Counter
c = []
for i in range(10000):
    a = s13_predict.predict()
    c.append(a)
result = Counter(c)
print(result)
