#ifndef PAGEONE_H
#define PAGEONE_H

#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QStackedWidget>
#include <QLabel>
#include <QToolButton>
#include <QLineEdit>
#include <QTextEdit>
#include "typedef.h"

class PageOne : public QWidget
{
    Q_OBJECT

public:
    explicit PageOne(QWidget *parent = 0);

    void timerEvent(QTimerEvent *event);

public slots:
    void ClickButton1();

protected:
    int m_nTimerID;

private:
    QVBoxLayout *m_pageOneLayout;
    QPushButton *m_pushButton1, *m_pushButton2;
    QStackedWidget *m_stackedWidget;

    QLabel *label_choice;
    QLabel *label_result;
    QToolButton *toolButton_single, *toolButton_double, *toolButton_start, *toolButton_stop;
    QLabel *label_plus1, *label_plus2, *label_equal;
    QLineEdit *lineEdit_No1, *lineEdit_No2, *lineEdit_No3, *lineEdit_sum;
    QTextEdit *textEdit_display;
};

#endif // PAGEONE_H
