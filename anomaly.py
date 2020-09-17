import pandas
from pathlib import Path
import argparse
import json
from datetime import datetime, timedelta
import typing as T
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def load_data(file: Path) -> T.Dict[str, pandas.DataFrame]:

    temperature = {}
    occupancy = {}
    co2 = {}

    with open(file, "r") as f:
        for line in f:
            r = json.loads(line)
            room = list(r.keys())[0]
            time = datetime.fromisoformat(r[room]["time"])

            temperature[time] = {room: r[room]["temperature"][0]}
            occupancy[time] = {room: r[room]["occupancy"][0]}
            co2[time] = {room: r[room]["co2"][0]}

    data = {
        "temperature": pandas.DataFrame.from_dict(temperature, "index").sort_index(),
        "occupancy": pandas.DataFrame.from_dict(occupancy, "index").sort_index(),
        "co2": pandas.DataFrame.from_dict(co2, "index").sort_index(),
    }

    return data

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="load and analyse IoT JSON data")
    p.add_argument("file", help="path to JSON data file")
    P = p.parse_args()

    file = Path(P.file).expanduser()

    data = load_data(file)
    
    temperature = data['temperature']['office'].dropna()

    std = np.std(temperature)
    mean = np.mean(temperature)
    newTemps = []
    for j in temperature:
        if not j > mean + std or j < mean + std:
            newTemps.append(j)

    diff = len(temperature) - len(newTemps)

    percent = (100 * diff/len(temperature))

    print("Percentage of Anomalies: " + str(percent))

    print("Median of Temperature in Office (No anomalies): " + str(np.median(newTemps)))

    print("Variance of Temperature in Office (No anomalies): " + str(np.var(newTemps)))

    
