#include "pageone.h"
#include <QFont>
#include <QIntValidator>
#include <QPalette>

PageOne::PageOne(QWidget *parent) : QWidget(parent)
{
    //m_pageOneLayout = new QVBoxLayout(this);
    //m_stackedWidget = new QStackedWidget(this);

    m_nTimerID = 0;

    QFont font;
    font.setFamily(QStringLiteral("Adobe Arabic"));
    font.setPointSize(18);
    font.setBold(true);
    font.setWeight(75);

    label_choice = new QLabel(this);
    label_choice->setObjectName(QStringLiteral("label_choice"));
    label_choice->setGeometry(QRect(133, 30, 51, 31));
    //label_choice->setGeometry(QRect(133, 120, 51, 31));
    label_choice->setText(tr("chioce:"));
    label_choice->setFont(font);

    label_result = new QLabel(this);
    label_result->setObjectName(QStringLiteral("label_result"));
    label_result->setGeometry(QRect(135, 70, 51, 31));
    label_result->setText(tr("result:"));
    label_result->setFont(font);

    toolButton_single = new QToolButton(this);
    toolButton_single->setObjectName(QStringLiteral("toolButton_single"));
    toolButton_single->setGeometry(QRect(200, 35, 51, 21));
    toolButton_single->setText(tr("single"));

    toolButton_double = new QToolButton(this);
    toolButton_double->setObjectName(QStringLiteral("toolButton_double"));
    toolButton_double->setGeometry(QRect(270, 35, 51, 21));
    toolButton_double->setText(tr("double"));

    label_plus1 = new QLabel(this);
    label_plus1->setObjectName(QStringLiteral("label_4"));
    label_plus1->setGeometry(QRect(250, 70, 16, 31));
    label_plus1->setFont(font);
    label_plus1->setText(tr("+"));

    lineEdit_No1 = new QLineEdit(this);
    lineEdit_No1->setObjectName(QStringLiteral("lineEdit_1"));
    lineEdit_No1->setGeometry(QRect(200, 76, 41, 20));
    lineEdit_No1->setStyleSheet(QStringLiteral(""));

    lineEdit_No2 = new QLineEdit(this);
    lineEdit_No2->setObjectName(QStringLiteral("lineEdit_2"));
    lineEdit_No2->setGeometry(QRect(270, 76, 41, 20));

    label_plus2 = new QLabel(this);
    label_plus2->setObjectName(QStringLiteral("label_5"));
    label_plus2->setGeometry(QRect(321, 70, 16, 31));
    label_plus2->setFont(font);
    label_plus2->setText(tr("+"));

    lineEdit_No3 = new QLineEdit(this);
    lineEdit_No3->setObjectName(QStringLiteral("lineEdit_3"));
    lineEdit_No3->setGeometry(QRect(340, 76, 41, 20));

    label_equal = new QLabel(this);
    label_equal->setObjectName(QStringLiteral("label_6"));
    label_equal->setGeometry(QRect(391, 70, 16, 31));
    label_equal->setFont(font);
    label_equal->setText(tr("="));

    lineEdit_sum = new QLineEdit(this);
    lineEdit_sum->setObjectName(QStringLiteral("lineEdit_4"));
    lineEdit_sum->setGeometry(QRect(410, 76, 41, 20));

    toolButton_start = new QToolButton(this);
    toolButton_start->setObjectName(QStringLiteral("toolButton_start"));
    toolButton_start->setGeometry(QRect(132, 110, 51, 21));
    toolButton_start->setStyleSheet(QStringLiteral(""));
    toolButton_start->setText(tr("start"));

    toolButton_stop = new QToolButton(this);
    toolButton_stop->setObjectName(QStringLiteral("toolButton_stop"));
    toolButton_stop->setGeometry(QRect(193, 110, 51, 21));
    toolButton_stop->setStyleSheet(QStringLiteral(""));
    toolButton_stop->setText(tr("stop"));

    textEdit_display = new QTextEdit(this);
    textEdit_display->setObjectName(QStringLiteral("textEdit_2"));
    textEdit_display->setGeometry(QRect(135, 140, 104, 111));
    textEdit_display->setLineWrapMode(QTextEdit::WidgetWidth);

    connect(toolButton_single, SIGNAL(clicked()), this, SLOT(ClickButton1()));
    connect(toolButton_double, SIGNAL(clicked()), this, SLOT(ClickButton1()));
    connect(toolButton_start, SIGNAL(clicked()), this, SLOT(ClickButton1()));
    connect(toolButton_stop, SIGNAL(clicked()), this, SLOT(ClickButton1()));

    // 设置颜色，限制
    lineEdit_No1->setValidator(new QIntValidator(0, 9, this));  // 限定只能输入整数
    lineEdit_No2->setValidator(new QIntValidator(0, 9, this));
    lineEdit_No3->setValidator(new QIntValidator(0, 9, this));
    lineEdit_sum->setValidator(new QIntValidator(0, 27, this));

    QPalette pal;
    pal.setColor(QPalette::Text, QColor(253, 91, 112));
    lineEdit_No1->setPalette(pal);
    pal.setColor(QPalette::Text, QColor(47, 54, 189));
    lineEdit_No2->setPalette(pal);
    pal.setColor(QPalette::Text, QColor(175, 61, 126));
    lineEdit_No3->setPalette(pal);
    pal.setColor(QPalette::Text, QColor(235, 13, 1));
    lineEdit_sum->setPalette(pal);

}

void PageOne::ClickButton1()
{
    QToolButton* btn= qobject_cast<QToolButton*>(sender());

    if( "toolButton_single" == btn->objectName()) // 获取界面被点击的对象
    {
        if (toolButton_single->styleSheet().isEmpty())
        {
            toolButton_single->setStyleSheet(QStringLiteral("background-color: rgb(255, 85, 0);"));
            toolButton_double->setStyleSheet(QStringLiteral(""));
        }
        else
        {
            toolButton_single->setStyleSheet(QStringLiteral(""));    // 清除背景颜色
        }
    }
    else if( "toolButton_double" == btn->objectName())
    {
        if (toolButton_double->styleSheet().isEmpty())
        {
            toolButton_double->setStyleSheet(QStringLiteral("background-color: rgb(255, 85, 0);"));
            toolButton_single ->setStyleSheet(QStringLiteral(""));
        }
        else
        {
            toolButton_double->setStyleSheet(QStringLiteral(""));
        }
    }
    else if ("toolButton_start" == btn->objectName())  // 定时器开启
    {
        if (m_nTimerID == 0)
        {
            m_nTimerID = startTimer(3000);
        }
    }
    else if ("toolButton_stop" == btn->objectName())  // 定时器关闭
    {
        if (m_nTimerID != 0)
        {
            killTimer(m_nTimerID);
            m_nTimerID = 0;
        }
    }

}

void PageOne::timerEvent(QTimerEvent *event)
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

    lineEdit_No1->setText(strRandom1);
    lineEdit_No2->setText(strRandom2);
    lineEdit_No3->setText(strRandom3);
    lineEdit_sum->setText(strRandom4);

    textEdit_display->insertPlainText(strRandom4+tr("\n"));
    textEdit_display ->moveCursor(QTextCursor::Start); // 焦点移动到开头
}
