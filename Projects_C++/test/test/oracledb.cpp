#include "oracledb.h"
 
DBOper::DBOper()
{
    CoInitialize(NULL); // 初始化com组件

}

DBOper::DBOper(char *szUserID, char *szPwd)
{
	CoInitialize(NULL); // 初始化com组件

    m_pConnection = CreateConnPtr();
    m_pCommand = CreateCommPtr();
	m_cRollbackFlag = '0';
	m_strSql = "";
	m_pRst = NULL;

	ConnToDB("Provider=OraOLEDB.Oracle;Persist Security Info=True;DataSource=ORCLss", szUserID, szPwd);
}
 
DBOper::~DBOper()
{
	if (m_pConnection->State != adStateClosed) // 状态不等于close才关闭
	{
		m_pConnection->Close();
	}
	CoUninitialize();
}

_ConnectionPtr DBOper::CreateConnPtr()
{
    HRESULT hr;
    _ConnectionPtr connPtr;
    hr = connPtr.CreateInstance(__uuidof(Connection));
    if(FAILED(hr) == TRUE)
    {
        return NULL;
    }
    return connPtr;
}
 
_CommandPtr DBOper::CreateCommPtr()
{
    HRESULT hr;
    _CommandPtr commPtr;
    hr = commPtr.CreateInstance(__uuidof(Command));
    if(FAILED(hr) == TRUE)
    {
        return NULL;
    }
    return commPtr;
}
 
bool DBOper::ConnToDB(char *strConn,char *szUserID, char*szPwd)
{
	if (NULL == m_pConnection)
	{
		printf("创建数据库连接实例失败");
		return false;
	}

    try
    {
		m_pConnection->ConnectionTimeout = 10; // 连接超时为10秒
        HRESULT hr = m_pConnection->Open(strConn, szUserID, szPwd, NULL);
        if (TRUE == FAILED(hr))
        {
            return false;
        }
		m_pCommand->ActiveConnection = m_pConnection;
		return true;
    }
    catch(_com_error &e)
    {
        PrintErrorInfo(e);
        return false;
    }
}
 
_RecordsetPtr DBOper::ExecuteSql(const string strSql)
{
    try
    {
		m_pCommand->CommandText =_bstr_t(strSql.c_str());
        _RecordsetPtr pRst = m_pCommand->Execute(NULL, NULL, adCmdText);
        return pRst;
    }
    catch(_com_error &e)
    {
        PrintErrorInfo(e);
        return NULL;
    }
}
 
void DBOper::PrintErrorInfo(_com_error &e)
{
	printf("错误信息如下:\n");
	printf("序号:%d\n错误信息:%s\n错误源:%s\n错误描述:%s\n", e.Error(), e.ErrorMessage(), (LPCTSTR)e.Source(), (LPCTSTR)e.Description());
    //printf("Errorinfomation are as follows\n");
    //printf("ErrorNo:%d\nError Message:%s\nError Source:%s\nError Description:%s\n",e.Error(), e.ErrorMessage(), (LPCTSTR)e.Source(), (LPCTSTR)e.Description());
}

void DBOper::TransBegin()
{
	if (NULL != m_pConnection)
	{
		m_pConnection->BeginTrans();
	}
}

void DBOper::CheckCommit()
{
	if (NULL != m_pConnection && m_cRollbackFlag == '0')
	{
		m_pConnection->CommitTrans();
	}
}

void DBOper::RollbakTrans()
{
	if (NULL != m_pConnection)
	{
		m_pConnection->RollbackTrans();
		m_cRollbackFlag = '1';
	}
}

void DBOper::Open(string strSql)
{
	if (m_pRst == NULL)
	{
		m_strSql = strSql;
	}
	else if (m_pRst->State != adStateClosed)
	{
		printf("已经open，请先close");
	}
}

void DBOper::Execute()
{
	m_pRst = ExecuteSql(m_strSql);
}

bool DBOper::Eof()
{
	if (NULL == m_pRst)
	{
		printf("数据查询出现错误");
		return true;
	}

	return m_pRst->adoEOF;
}

void DBOper::MoveNext()
{
	m_pRst->MoveNext();
}

void DBOper::Close()
{
	if (m_pRst->State != adStateClosed)
	{
		m_pRst->Close();
	}
}

//template <typename T>
//void DBOper::GetValue(char *szKey, T &result)
//{
//	_variant_t varResult;
//	varResult = pRst->GetCollect(_variant_t(szKey));
//}
 
//_RecordsetPtr DBOper::CreateRecsetPtr()
//{
//    HRESULT hr;
//    _RecordsetPtr recsetPtr;
//    hr = recsetPtr.CreateInstance(__uuidof(Command));
//    if(FAILED(hr) == TRUE)
//    {
//        return NULL;
//    }
//    return recsetPtr;
//}
