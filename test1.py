from s13_predict import predict
from collections import Counter
c = []
for i in range(10000):
    a = predict.predict()
    c.append(a)
result = Counter(c)
print(result)
