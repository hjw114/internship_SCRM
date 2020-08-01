import reader
import pandas as pd
import os

def analysis():
    thing = []
    data = {}
    for i in range(len(reader.data_reader())):
        for j in range(len(reader.data_reader()[i])):
            if (type(reader.data_reader()[i][j]) != float):
                if reader.data_reader()[i][j] in thing:
                    data[reader.data_reader()[i][j]] += 1
                else:
                    data[reader.data_reader()[i][j]] = 1
                    thing.append(reader.data_reader()[i][j])
    return data


def save(dict):
    file_name = 'analysis.csv'
    df = pd.DataFrame.from_dict(dict,orient='index')
    df.columns = ["number"]
    df.sort_values("number", inplace=True, ascending=False)
    try:
        df.to_csv(file_name)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

if __name__ == '__main__':
    save(analysis())