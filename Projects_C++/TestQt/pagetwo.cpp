#include "pagetwo.h"
#include <QMessageBox>
#include <QIntValidator>
#include <QTextCodec>
#include<sstream>
#include"oracledb.h"

#if _MSC_VER >= 1600

#pragma execution_character_set("utf-8")

#endif

PageTwo::PageTwo(QWidget *parent) : QWidget(parent)
{
    //m_pageOneLayout = new QVBoxLayout(this);

	QTextCodec::setCodecForLocale(QTextCodec::codecForName("GBK"));

    pushButton_search = new QPushButton(this);
    pushButton_search->setText(tr("搜索"));
    pushButton_search->setGeometry(QRect(260, 35, 51, 21));

    lineEdit_name = new QLineEdit(this);
    lineEdit_name->setObjectName(QStringLiteral("lineEdit_name"));
    lineEdit_name->setPlaceholderText("name");
    lineEdit_name->setGeometry(QRect(130, 35, 51, 21));

    lineEdit_ID = new QLineEdit(this);
    lineEdit_ID->setObjectName(QStringLiteral("lineEdit_ID"));
    lineEdit_ID->setPlaceholderText("ID");
	lineEdit_ID->setValidator(new QIntValidator(0, 10000, this));
    lineEdit_ID->setGeometry(QRect(200, 35, 51, 21));

    tableWidget = new QTableWidget(this);
    tableWidget->setObjectName(QStringLiteral("tableWidget"));
    tableWidget->setGeometry(QRect(130, 70, 203, 250));
    tableWidget->setColumnCount(2);
    //tableWidget->setRowCount(4);
    tableWidget->verticalHeader()->setVisible(false);
    tableWidget->setHorizontalHeaderLabels(QStringList() << "id" << "name");
    tableWidget->setSelectionBehavior(QAbstractItemView::SelectItems);
    tableWidget->setSelectionMode(QAbstractItemView::ExtendedSelection);

    //for (int i = 0; i < 2; i++)
    //{
    //    for (int j = 0; j < 2; j++)
    //    {
    //        QTableWidgetItem *item = new QTableWidgetItem();
    //        item->setBackground(QBrush(QColor(Qt::lightGray)));
    //        item->setFlags(item->flags() & (~Qt::ItemIsEditable));
    //        item->setText(QString::number(i+j));

    //        tableWidget->setItem(i, j, item);
    //    }
    //}

	//int nRowCnt = tableWidget->rowCount();
	//tableWidget->insertRow(nRowCnt); // 插入新行

    connect(tableWidget->horizontalHeader(), SIGNAL(sectionClicked(int)), this, SLOT(sortByColumn(int)));
	connect(pushButton_search, SIGNAL(clicked()), this, SLOT(QueryInfo()));


    //m_pageOneLayout->addWidget(m_pushButton);
}

void PageTwo::QueryInfo()
{
	vector<string> vetData;
	map<int, string> mapData;

	try
	{
		DBOper dbOper("tbq", "tbq");

		string sql = "select * from test where 1=1";

		int nId = lineEdit_ID->text().toInt();

		QString  str = lineEdit_name->text();
		string  szNe;
		QByteArray ba = str.toLocal8Bit();     //  toLoacl8Bit支持中文
		szNe = ba.data();


		if (nId)
		{
			stringstream ss;
			ss << nId;
			sql += " and id = "+ ss.str();
		}
		if (szNe.length() != 0)
		{
			sql += " and name = '"+szNe+"'";
		}

		sql += " order by id";

		int nID = 0;
		char szName[16] = "";
		string strName;
		char szTmp[] = "";
		size_t nIndex = 0;

		dbOper.Open(sql);
		dbOper.Execute();
		int nRowCnt = 0;
		nRowCnt = dbOper.RecordCnt();
		tableWidget->setRowCount(nRowCnt);
		while (!dbOper.Eof())
		{
			dbOper.GetValue("id", nID);
			sprintf(szTmp, "%d", nID);
			mapData[nIndex] = szTmp;
			nIndex++;
			dbOper.GetValue("name", strName);
			mapData[nIndex] = strName;
			dbOper.MoveNext();
			nIndex++;
		}

		int nIdx = 0;

		for (size_t i = 0; i < nRowCnt; i++)
		{
			for (size_t j = 0; j < 2; j++)
			{
				QTableWidgetItem *item = new QTableWidgetItem();
				item->setText(QString::fromLocal8Bit(mapData[nIdx].c_str()));
				tableWidget->setItem(i, j, item);
				nIdx++;
			}
		}
	}
	catch (_com_error &e)
	{
		QMessageBox::information(this, QObject::tr("你好"), QObject::tr((char *)e.ErrorMessage()), QMessageBox::Yes | QMessageBox::No);
	}
	catch (const std::exception& e)
	{
		QMessageBox::information(this, QObject::tr("你好"), QString::fromLocal8Bit(e.what()), QMessageBox::Yes | QMessageBox::No);
	}
}

void PageTwo::sortByColumn(int colum)
{
    static bool bSortFlag = true;
    tableWidget->sortByColumn(colum, bSortFlag ? Qt::AscendingOrder : Qt::DescendingOrder);
    bSortFlag = !bSortFlag;
}
