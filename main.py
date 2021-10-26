import random
import time
import csv
from options import Options
from tqdm import tqdm
import os
from EC.GA import GA
from visulizer import concat, analyze, analyze_all


def main():

    os.system("rm -rf results/*")
    os.system("mkdir results")
    starttime = time.time()
    random.seed(64)

    opt = Options().parse()
    # tar = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    tar = [0, 0, 0, 0, 0, 1, 0]
    iter = 1

    namelist = []
    for a,b,c in os.walk(opt.data_root + "/imgs"):
        namelist = c
    for name in tqdm(namelist):
        with open(opt.data_root + "/test_ids.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow([name])
        for i in tqdm(range(iter)):
            name = name.split(".")[0] + "_" + str(i)
            ga = GA(opt, name, tar)
            ga.run()
        break
    names = os.listdir(opt.results)
    for name in names:
        if name.endswith(".csv"):
            analyze(opt.results, name, iter, opt.generation_count, opt.life_count)
            analyze_all(opt.results, name, opt.generation_count, opt.life_count)
        else:
            concat(opt.results, name, 128, opt.generation_count, opt.life_count)
    print("time cost: " + str(round(time.time() - starttime, 2)) + " seconds")


if __name__ == "__main__":
    main()
