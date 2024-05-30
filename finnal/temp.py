import matplotlib.pyplot as plt

data = {
    0: {"pass@1": 65.9, "pass@5": 65.9},
    0.25: {"pass@1": 62.2, "pass@5": 73.8},
    0.5: {"pass@1": 64.6, "pass@5": 75.6},
    0.75: {"pass@1": 61.6, "pass@5": 79.3},
    1: {"pass@1": 63.4, "pass@5": 82.3}
}

temperature = list(data.keys())
pass1 = [data[temp]["pass@1"] for temp in temperature]
pass5 = [data[temp]["pass@5"] for temp in temperature]

plt.plot(temperature, pass1, label='pass@1')
plt.plot(temperature, pass5, label='pass@5')
plt.xlabel('Temperature')
plt.ylabel('%')
plt.legend()
plt.show()
