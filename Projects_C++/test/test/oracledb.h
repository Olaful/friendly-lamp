
#pragma once
//pragma 设定编译器的状态或指示编译器完成一些特定的动作
#import "C:\Program Files\Common Files\System\ado\msado15.dll" no_namespace rename("EOF","adoEOF")
//当编译器遇到#import语句时，它会为引用组件类型库中的接口生成包装类，#import语句实际上相当于执行了API涵数LoadTypeLib()。
//#import语句会在工程可执行程序输出目录中产生两个文件，分别为*.tlh(类型库头文件)及*.tli(类型库实现文件)，
//它们分别为每一个接口产生智能指针，并为各种接口方法、枚举类型，CLSID等进行声明，创建一系列包装方法。
//在没有经过编译器编译之前，文件还没有生成，所以，会出现错误提示。

#define PI 3.14
//#define MAX (x > y ? x : y)

#include<string>
using namespace std;
 
class DBOper
{
public:
    //初始化数据库操作需要的对象
    DBOper();
	DBOper(char *szUserID, char *szPwd);
    ~DBOper();

    //连接至数据库
    bool ConnToDB(char *strConn,char *szUserID, char*szPwd);
 
    //数据库操作函数
    //查询操作删除以及添加
    _RecordsetPtr ExecuteSql(const string strSql);

	// 开启事务
	void TransBegin();

	// 提交事务
	void CheckCommit();

	// 回滚事务
	void RollbakTrans();

	// 打开sql语句
	void Open(string strSql);

	// 执行sql
	void Execute();

	// 设置入参
	void SetValue();

	// 结果集是否为空
	bool Eof();

	void Close();

	// 结果集移动至下一行
	void MoveNext();

	// 根据关键字获取对应字段值
	//template <typename T>
	//void GetValue(char *szKey, T &result);
	void GetValue(char *szKey, int &nValue) // 类体实现相当于自动内联了
	{
		_variant_t varResult;
		varResult = m_pRst->GetCollect(_variant_t(szKey));
		nValue = varResult.intVal;
	}
	
	inline void GetValue(char *szKey, char *szValue) // inline只在当前单元有效,所以不能在CPP文件中实现
	{
		_variant_t varResult;
		varResult = m_pRst->GetCollect(_variant_t(szKey));
		strcpy(szValue, (LPSTR)(LPCSTR)_bstr_t(varResult));
	}
	
	inline void GetValue(char *szKey, float &fValue)
	{
		_variant_t varResult;
		varResult = m_pRst->GetCollect(_variant_t(szKey));
		fValue = varResult.fltVal;
	}
	
	inline void GetValue(char *szKey, double &dValue)
	{
		_variant_t varResult;
		varResult = m_pRst->GetCollect(_variant_t(szKey));
		dValue = varResult.dblVal;
	}
	
	inline void GetValue(char *szKey, string &strValue)
	{
		_variant_t varResult;
		varResult = m_pRst->GetCollect(_variant_t(szKey));
		strValue = varResult.pcVal;
	}
 
private:
	// 打印连接错误信息
    void PrintErrorInfo(_com_error &);
 
private:
    //初始化数据库连接、命令、记录集
    _ConnectionPtr CreateConnPtr();
    _CommandPtr CreateCommPtr();
    //_RecordsetPtr CreateRecsetPtr();
 
private:
    //数据库连接需要的连接、命令操作对象
    _ConnectionPtr m_pConnection;
    _CommandPtr m_pCommand;
	
private:
	// 是否已经回滚事务标志
	char m_cRollbackFlag;

	// 待执行的sql语句
	string m_strSql;

	// 结果集
	_RecordsetPtr m_pRst;
};