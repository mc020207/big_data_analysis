import psycopg2
import pandas as pd
import numpy as np
from tqdm import tqdm

if __name__ == '__main__':

    conn = psycopg2.connect(host="127.0.0.1",
                            database="bigdata_demo",
                            user="postgres",
                            password="psql")
    cur = conn.cursor()

    file_base = "./output/"
    file_names = os.listdir(file_base)
    for file_name in file_names:
        filename = file_base+file_name
        print(i,'now is file: ',filename)
        df = pd.read_csv(filename)
        arr = np.array(df)
        for i in tqdm(arr):
            cur.execute("insert into modesearch(key, value, confidence,lift,support) values(%(key)s, %(value)s, %(confidence)s,%(lift)s,%(support)s)",
                        {'key': i[0], 'value': i[1], 'confidence': i[2], 'lift': i[3], 'support': i[4]})
            # 向数据库中插入数据即可
            conn.commit()
