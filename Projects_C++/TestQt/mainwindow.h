#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QVBoxLayout>
#include <QStackedLayout>
#include <QPushButton>
#include "pageone.h"

#if _MSC_VER >= 1600

#pragma execution_character_set("utf-8")

#endif

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0); // 显示转换
    ~MainWindow();

private:
    Ui::MainWindow *ui;

public slots:       // 信号槽
    void ClickButton1();
    void SwitchPage();

public:
    void timerEvent(QTimerEvent *event);
protected:
    int m_nTimerID;
private:
};

#endif // MAINWINDOW_H
