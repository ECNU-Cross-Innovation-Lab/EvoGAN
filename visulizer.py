import os
from PIL import Image
import matplotlib.pyplot as plt
import csv

def concat(path, name, size, row, col, quality = 100):

    images = []
    for name2 in os.listdir(os.path.join(path, name)):
        images.append(Image.open(os.path.join(path, name, name2)))

    target = Image.new('RGB', (size * col, size * row))

    for i in range(len(images)):
        temp = i % row
        target.paste(images[i], (size * (int(i / row)), size * temp, size * (int(i / row) + 1), size * (temp + 1)))

    target.save("concat_" + name + ".jpg", quality=quality)

def analyzegen(data):
    max = 0
    min = 100
    sum = 0
    std = 0
    for d in data:
        d = float(d)
        if d > max:
            max = d
        if d < min:
            min = d
        sum += d
    avg = sum / len(data)
    for d in data:
        d = float(d)
        std += pow(d - avg, 2)
    ret = []
    ret.append(max)
    ret.append(min)
    ret.append(std)
    ret.append(avg)
    return ret

def analyze_all(path, name, generation, life):

    csv_path = os.path.join(path, name)
    with open(csv_path, 'r') as f1:
        reader = csv.reader(f1)
        x = []
        data = []
        next(reader)
        r = []
        for row in reader:
            r.append(row)

        cnt = 0
        for i in range(generation):
            temp = []
            for j in range(life):
                x.append(i + 1)
                data.append(float(r[cnt][4]))
                cnt = cnt + 1
        plt.clf()
        print(x)
        print(data)
        plt.plot(x, data, '.')
        plt.savefig("stastic_all.pdf", format="pdf")


def analyze(path, name, interpolation, generation, life):

    csv_path = os.path.join(path, name)
    with open(csv_path, 'r') as f1:
        reader = csv.reader(f1)
        lifescore = []
        genscore = []
        score = []
        next(reader)
        r = []
        for row in reader:
            r.append(row)

        i = 0
        for i1 in range(interpolation):
            for i2 in range(generation):
                for i3 in range(life):
                    print(i)
                    lifescore.append(r[i][4])
                    i += 1
                genscore.append(lifescore)
                lifescore = []
            score.append(genscore)
            genscore = []

        max = [0 for _ in range(generation)]
        min = [0 for _ in range(generation)]
        std = [0 for _ in range(generation)]
        avg = [0 for _ in range(generation)]

        for i1 in range(generation):
            for i2 in range(interpolation):
                ret = analyzegen(score[i2][i1])
                max[i1] += ret[0]
                min[i1] += ret[1]
                std[i1] += ret[2]
                avg[i1] += ret[3]

        for j in range(generation):
            max[j] /= interpolation
            min[j] /= interpolation
            std[j] /= interpolation
            avg[j] /= interpolation

        out_csv = os.path.join(path, "stastic_" + name)
        with open(out_csv, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["generation", "max", "min", "std", "avg"])
            for i in range(generation):
                writer.writerow([i, max[i], min[i], std[i], avg[i]])
        x = [i for i in range(generation)]
        plt.clf()
        plt.plot(x, max, label="max")
        plt.plot(x, min, label="min")
        # plt.plot(x, std, label="std")
        plt.plot(x, avg, label="avg")
        plt.xticks(range(0, generation))
        plt.title("EvoGAN")
        plt.xlabel("generation")
        plt.ylabel("score")
        plt.legend()
        plt.savefig("stastic.pdf", format="pdf")



