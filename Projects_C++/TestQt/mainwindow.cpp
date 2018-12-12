#include "mainwindow.h"
#include "myui.h"
#include <QMessageBox>
#include <QtGlobal>
#include <iostream>
#include <QIntValidator>
#include <QPalette>

#if _MSC_VER >= 1600

#pragma execution_character_set("utf-8")

#endif

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this); // 初始化界面
    connect(ui->pushButton1, SIGNAL(clicked()), this, SLOT(SwitchPage()));
    connect(ui->pushButton2, SIGNAL(clicked()), this, SLOT(SwitchPage()));

    ui->pushButton1->setText(tr("页面一"));
    ui->pushButton2->setText(tr("页面二"));

    //setLayout(m_mainLayout);

}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::ClickButton1()
{
    //QMessageBox::information(this, QObject::tr("你好"), QString::fromLocal8Bit("恭喜你"), QMessageBox::Yes | QMessageBox::No);

    QToolButton* btn= qobject_cast<QToolButton*>(sender());

    if( "toolButton_1" == btn->objectName()) // 获取界面被点击的对象
    {
        if (ui->toolButton_1->styleSheet().isEmpty())
        {
            //ui->textEdit_1->setText(QString::number(ui->toolButton_1->isChecked(), 10));
            ui->toolButton_1->setStyleSheet(QStringLiteral("background-color: rgb(255, 85, 0);"));
            ui->toolButton_2->setStyleSheet(QStringLiteral(""));
        }
        else
        {
            ui->toolButton_1->setStyleSheet(QStringLiteral(""));    // 清除背景颜色
        }
    }
    else if( "toolButton_2" == btn->objectName())
    {
        if (ui->toolButton_2->styleSheet().isEmpty())
        {
            ui->toolButton_2->setStyleSheet(QStringLiteral("background-color: rgb(255, 85, 0);"));
            ui->toolButton_1->setStyleSheet(QStringLiteral(""));
        }
        else
        {
            ui->toolButton_2->setStyleSheet(QStringLiteral(""));
        }
    }
    else if ("toolButton_3" == btn->objectName())  // 定时器开启
    {
        if (m_nTimerID == 0)
        {
            m_nTimerID = startTimer(3000);
        }
    }
    else if ("toolButton_4" == btn->objectName())  // 定时器关闭
    {
        if (m_nTimerID != 0)
        {
            killTimer(m_nTimerID);
            m_nTimerID = 0;
        }
    }

}

void MainWindow::timerEvent(QTimerEvent *event)
{
    //srand((unsigned)time(NULL));   // 设定随机数seed值 使用time作为随机种子几乎每次nRandom1隔几秒才会改变，而后面其它的没出现这种情况

    int nRandom1 = rand() % 10;
    int nRandom2 = rand() % 10;
    int nRandom3 = rand() % 10;
    int nRandom4 = nRandom1 + nRandom2 + nRandom3;

    QString strRandom1 = QString::number(nRandom1);
    QString strRandom2 = QString::number(nRandom2);
    QString strRandom3 = QString::number(nRandom3);
    QString strRandom4 = QString::number(nRandom4);

    ui->lineEdit_1->setText(strRandom1);
    ui->lineEdit_2->setText(strRandom2);
    ui->lineEdit_3->setText(strRandom3);
    ui->lineEdit_4->setText(strRandom4);

    ui->textEdit_2->insertPlainText(strRandom4+tr("\n"));
    ui->textEdit_2->moveCursor(QTextCursor::Start); // 焦点移动到开头
}

void MainWindow::SwitchPage()
{
    QPushButton* btn= qobject_cast<QPushButton*>(sender());

    if( "pushButton1" == btn->objectName())
    {
        ui->stackedLayout->setCurrentIndex(0);
        //ui->stackedWidget->setCurrentIndex(0);
    }
    else if( "pushButton2" == btn->objectName())
    {
        ui->stackedLayout->setCurrentIndex(1);
        //ui->stackedWidget->setCurrentIndex(1);
    }
}
