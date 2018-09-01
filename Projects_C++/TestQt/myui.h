#ifndef MY_UI_H
#define MY_UI_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QToolButton>
#include <QtWidgets/QWidget>
#include <QVBoxLayout>
#include <QStackedLayout>
#include <QPushButton>
#include <QSplitter>
#include "pageone.h"
#include "pagetwo.h"
#include <QStackedWidget>

QT_BEGIN_NAMESPACE

class Myui
{
public:
    QAction *actionenjoy;
    QWidget *centralWidget;
    QLabel *label;
    QToolButton *toolButton_1;
    QToolButton *toolButton_2;
    QTextEdit *textEdit_1;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLineEdit *lineEdit_1;
    QLineEdit *lineEdit_2;
    QLabel *label_5;
    QLineEdit *lineEdit_3;
    QLabel *label_6;
    QLineEdit *lineEdit_4;
    QToolButton *toolButton_3;
    QToolButton *toolButton_4;
    QTextEdit *textEdit_2;
    QMenuBar *menuBar;
    QMenu *menu;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    QSplitter *splitterMain;
    QVBoxLayout *mainLayout; // 主layout
    QVBoxLayout *rightLayout; // 右边layout
    QStackedLayout *stackedLayout; // 堆layout
    QStackedWidget *stackedWidget; // 堆Widget
    QPushButton *pushButton1, *pushButton2;

    PageOne *pageOne;
    PageTwo *pageTwo;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(667, 476);
        actionenjoy = new QAction(MainWindow);
        actionenjoy->setObjectName(QStringLiteral("actionenjoy"));
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));

        mainLayout = new QVBoxLayout(centralWidget);
        rightLayout = new QVBoxLayout;
        stackedLayout = new QStackedLayout;
        stackedWidget = new QStackedWidget;
        pageOne = new PageOne;
        pageTwo = new PageTwo;
        pushButton1 = new QPushButton;
        pushButton2 = new QPushButton;
        pushButton1->setFixedSize(50, 20);
        pushButton2->setFixedSize(50, 20);
        pushButton1->setObjectName(QStringLiteral("pushButton1"));
        pushButton2->setObjectName(QStringLiteral("pushButton2"));

        rightLayout->setMargin(2); // 与窗口间隙
        rightLayout->setSpacing(0);   // Layout内部控件间隙
        rightLayout->addWidget(pushButton1); // 把btn1加入到layout中
        rightLayout->addWidget(pushButton2); // 把btn2加入到layout中
        //stackedLayout->addWidget(pageOne);
        stackedLayout->addWidget(pageTwo);
        stackedLayout->setCurrentIndex(0);

        mainLayout->setMargin(0);
        mainLayout->setSpacing(0);
        mainLayout->addLayout(rightLayout);
        mainLayout->addLayout(stackedLayout);

        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QStringLiteral("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 667, 23));
        menu = new QMenu(menuBar);
        menu->setObjectName(QStringLiteral("menu"));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QStringLiteral("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QStringLiteral("statusBar"));
        MainWindow->setStatusBar(statusBar);

        menuBar->addAction(menu->menuAction());
        menu->addAction(actionenjoy);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "\344\275\240\345\245\275", nullptr));
        actionenjoy->setText(QApplication::translate("MainWindow", "enjoy", nullptr));
        menu->setTitle(QApplication::translate("MainWindow", "\350\217\234\345\215\225", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Myui {};
} // namespace Ui

QT_END_NAMESPACE

#endif // MY_UI_H
