#!/usr/bin/env python3
"""
This example assumes the JSON data is saved one line per timestamp (message from server).

It shows how to read and process a text file line-by-line in Python, converting JSON fragments
to per-sensor dictionaries indexed by time.
These dictionaries are immediately put into Pandas DataFrames for easier processing.

Feel free to save your data in a better format--I was just showing what one might do quickly.
"""
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
    occupancy = data['occupancy']['office'].dropna()
    co2 = data['co2']['office'].dropna()

    print("Median temperature in office: " + str(np.median(temperature)))
    print("Variance of temperature in office: " + str(np.var(temperature)))
    print("Median occupancy in office: " + str(np.median(occupancy)))
    print("Variance of occupancy in office: " + str(np.var(occupancy)))

    plt.hist(temperature, bins = 100)
    plt.show()

    plt.hist(occupancy, bins = 100)
    plt.show()

    plt.hist(co2, bins = 100)
    plt.show()

    interval = []
    for i in range(1,len(data['co2'])):
        x = data['co2']['office'].index[i-1]
        y = data['co2']['office'].index[i]
        interval.append((y-x).seconds + ((y-x).microseconds/(1*10**6)))

    
    
    print("Mean time interval: " + str(np.mean(interval)))
    print("Variance of time interval: " + str(np.var(interval)))
    plt.hist(interval, bins = 100)
    plt.show()

    
    for k in data:
        # data[k].plot()
        time = data[k].index
        data[k].hist()
        plt.figure()
        plt.hist(np.diff(time.values).astype(np.int64) // 1000000000)
        plt.xlabel("Time (seconds)")

    plt.show()

