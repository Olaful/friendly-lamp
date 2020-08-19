import sqlite3
import datetime
import re
import pandas as pd
from baostock import query_dividend_data
from baostock import login as bao_stk_login
import util

_DB_SQLITE = {}
_DB_FILE = 'sqlite.db'


def _get_sqllite(name="test"):
    if _DB_SQLITE.get(name, None):
        return _DB_SQLITE[name]

    class SQLite:
        def __init__(self):
            self.conn = sqlite3.connect(_DB_FILE)
            self.cursor = self.conn.cursor()
            self.sql_result = ()

        def execute(self, sql):
            is_insert_sql = sql.strip().lower().startswith('select') | \
                            sql.strip().lower().startswith('replace')
            # is_insert_sql = False

            begin = "BEGIN IMMEDIATE"
            commit = "COMMIT"

            if is_insert_sql:
                self.cursor.execute(begin)

            self.cursor.execute(sql)
            self.sql_result = self.cursor.fetchall()

            if is_insert_sql:
                self.cursor.execute(commit)

        def fetchone(self):
            if len(self.sql_result) > 0:
                return self.sql_result[0]
            return ()

        def fetchall(self):
            rls = self.sql_result
            return rls

    db_instance = SQLite()

    _DB_SQLITE[name] = db_instance

    return db_instance


def get_last_dvd_info(symbol):
    db = _get_sqllite('dvd_db')

    def check_table():
        try:
            exist_sql = 'SELECT 1 FROM `tb_dvd`'
            db.execute(exist_sql)
        except:
            create_table_sql = """CREATE TABLE `tb_dvd` (
                `code` char(32) NOT NULL, -- '标的'
                `dividOperateDate` date default NULL, -- '除权除息日期'
                `dividPayDate` date default NULL, -- '	派息日'
                `dividCashPsBeforeTax` float default '0.0', -- '每股股利税前',
                `dividCashPsAfterTax` float default '0.0', -- '每股股利税后'
                `dividStocksPs` float default '0.0', -- '每股红股'
                `dividReserveToStockPs` float default '0.0', -- '每股转增资本'
                `dividCashStock` TEXT, -- '分红送转(每股派息数(税前)+每股送股数+每股转增股本数)'
                `updatetime` datetime NOT NULL, -- '更新时间'
                PRIMARY KEY (`code`, `dividOperateDate`)
            )"""
            db.execute(create_table_sql)
    check_table()

    query_sql = f"SELECT `dividPayDate`, `dividCashPsBeforeTax`, \
     `dividStocksPs`, `dividReserveToStockPs`, `updatetime` FROM `tb_dvd` WHERE \
        `code` = '{symbol}' ORDER BY `dividPayDate` DESC LIMIT 1"
    db.execute(query_sql)
    dvd_info = db.fetchone()
    re_fetch = False

    if not dvd_info:
        re_fetch = True
    else:
        update_date = datetime.datetime.strptime(dvd_info[-1][:10], '%Y-%m-%d').date()
        today = datetime.datetime.today().date()   
        if update_date != today:
            re_fetch = True

    if not re_fetch:
        divid_pay_date = dvd_info[0]
        if not divid_pay_date:
            return {}
        return {
            'divid_pay_date': divid_pay_date,
            'divid_cash_ps_before_tax': dvd_info[1],
            'divid_stocks_ps': dvd_info[2],
            'divid_reserve_to_stock_ps': dvd_info[3]
        }

    bao_stk_login()

    def to_db(rs_list, fields):
        insert_sql = """REPLACE INTO `tb_dvd`(
            `code`, `dividOperateDate`, `dividPayDate`, `dividCashPsBeforeTax`,
            `dividCashPsAfterTax`, `dividStocksPs`, `dividReserveToStockPs`,`dividCashStock`,
            `updatetime`
        ) VALUES(
            '{code}', '{dividOperateDate}', '{dividPayDate}', {dividCashPsBeforeTax},
            {dividCashPsAfterTax}, {dividStocksPs}, {dividReserveToStockPs}, '{dividCashStock}',
            '{updatetime}'
        )"""
        insert_param = {
            'code': symbol, 'dividOperateDate': None, 'dividPayDate': None, 'dividCashPsBeforeTax': 0.0,
            'dividCashPsAfterTax': 0.0, 'dividStocksPs': 0.0, 'dividReserveToStockPs': 0.0, 'dividCashStock': '',
            'updatetime': str(today)
        }

        if not rs_list:
            db.execute(insert_sql.format(**insert_param))
            return
    
        result_dividend = pd.DataFrame(rs_list, columns=fields)

        for _, row in result_dividend.iterrows():
            dividCashPsAfterTax = row.dividCashPsAfterTax
            rls = re.search('[\u4e00-\u9fa5]', dividCashPsAfterTax)
            if rls:
                start = rls.start()
                dividCashPsAfterTax = float(dividCashPsAfterTax[:start])
            else:
                dividCashPsAfterTax = float(dividCashPsAfterTax)

            insert_param.update({
                'dividOperateDate': row.dividOperateDate,
                'dividPayDate': row.dividPayDate,
                'dividCashPsBeforeTax': row.dividCashPsBeforeTax if row.dividCashPsBeforeTax else 0,
                'dividCashPsAfterTax': dividCashPsAfterTax,
                'dividStocksPs': row.dividStocksPs if row.dividStocksPs else 0,
                'dividReserveToStockPs': row.dividReserveToStockPs if row.dividReserveToStockPs else 0,
                'dividCashStock': row.dividCashStock,
            })

            db.execute(insert_sql.format(**insert_param))

    today = datetime.datetime.today()
    pre_year_today = today - datetime.timedelta(days=366)
    today_year = today.year
    pre_year = pre_year_today.year

    rs_list = []
    fields = []
    code = f"sh.{symbol}" if symbol.startswith('60') else f"sz.{symbol}"
    for year in [today_year, pre_year]:
        rs_dividend = query_dividend_data(code=code, year=year, yearType="report")

        while (rs_dividend.error_code == '0') & rs_dividend.next():
            rs_list.append(rs_dividend.get_row_data())

        if rs_list:
            fields = rs_dividend.fields

    to_db(rs_list, fields)

    db.execute(query_sql)
    dvd_info = db.fetchone()
    divid_pay_date = dvd_info[0]
    if not divid_pay_date:
        return {}
    return {
        'divid_pay_date': divid_pay_date,
        'divid_cash_ps_before_tax': dvd_info[1],
        'divid_stocks_ps': dvd_info[2],
        'divid_reserve_to_stock_ps': dvd_info[3]
    }


def get_stock_pool(pool_name):
    """
    get symbol list from pool
    :param pool_name:
    :return:
    """
    db = util.get_mysql("pool_db")
    query_sql = "SELECT `code` FROM `code_pool` " \
                f" WHERE `pool` = '{pool_name}'"
    db.execute(query_sql)

    pool_info = db.fetchall()
    code_list = [code['code'] for code in pool_info]

    return code_list
