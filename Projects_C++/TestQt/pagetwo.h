#ifndef PAGETWO_H
#define PAGETWO_H

#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLineEdit>
#include <QTableWidget>
#include <QTableView>
#include <QHeaderView>
#include "typedef.h"

class PageTwo : public QWidget
{
    Q_OBJECT

public:
    explicit PageTwo(QWidget *parent = 0);

public slots:
    void QueryInfo();

    void sortByColumn(int colum);

private:
    QVBoxLayout *m_pageOneLayout;
    QPushButton *pushButton_search;
    QLineEdit *lineEdit_ID, *lineEdit_name;
    QTableWidget *tableWidget;

protected:

};

#endif // PAGETWO_H
