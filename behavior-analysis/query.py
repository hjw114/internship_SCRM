import apriori
import reader
import pandas

def write_csv(sql_data):
    file_name = 'conf.csv'
    save = pandas.DataFrame(list(sql_data))
    save.columns =["freqSet - conseq","conseq","conf"]
    save.sort_values("conf",inplace=True,ascending=False)
    try:
        save.to_csv(file_name)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

if __name__ == '__main__':
    dataSet = reader.data_reader()
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    write_csv(rule)