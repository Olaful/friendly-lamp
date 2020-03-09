import pandas as pd
from sqlalchemy import create_engine
from pypinyin import pinyin


def main():
    param = {'host': 'localhost', 'port': 3306, 'user': 'root',
             'password': '123', 'database': 'test', 'charset': 'utf8mb4'}
    url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'.format(**param)
    engine = create_engine(url)

    df = pd.read_excel(r'F:\file\2020-03-09 (1).xls', encoding='utf8')

    cols = df.columns
    cols = [pinyin(c) for c in cols]
    cols = list(map(lambda x: ''.join([i[0][0] for i in x]), cols))
    cols = [c.replace('(', '_').replace(')', '_').replace(' ', '') for c in cols]
    df.columns = cols
    df = df.applymap(lambda x: None if x == '--' else x)

    df.to_sql('iwencai_basic_ind', con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    main()
