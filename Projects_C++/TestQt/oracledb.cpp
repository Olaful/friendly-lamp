#include "oracledb.h"
 
DBOper::DBOper()
{
    CoInitialize(NULL); // 初始化com组件

}

DBOper::DBOper(const char *szUserID, const char *szPwd)
{
	CoInitialize(NULL); // 初始化com组件

    m_pConnection = CreateConnPtr();
    m_pCommand = CreateCommPtr();
	m_cRollbackFlag = '0';
	m_strSql = "";
	m_pRst = NULL;
	m_pRst.CreateInstance("ADODB.Recordset");
	//m_pRst->CursorLocation = adUseClient;

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
 
bool DBOper::ConnToDB(const char *strConn,const char *szUserID, const char*szPwd)
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
		throw;	// 重新抛出异常
    }
}
 
void DBOper::ExecuteSql(const string strSql)
{
    try
    {
		//m_pCommand->CommandText =_bstr_t(strSql.c_str());
  //      _RecordsetPtr pRst = m_pCommand->Execute(NULL, NULL, adCmdText);
  //      return pRst;
			m_pRst->Open(_variant_t(strSql.c_str()),
			m_pConnection.GetInterfacePtr(),
			adOpenStatic,
			adLockOptimistic,
			adCmdText);
    }
    catch(_com_error &e)
    {
        PrintErrorInfo(e);
		throw;
        //return NULL;
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
	if (m_pRst->State != adStateClosed)
	{
		myDbException objmyDbException("sql已经open，请先close");
		throw objmyDbException;
	}
	m_strSql = strSql;
}

void DBOper::Execute()
{
	//m_pRst = ExecuteSql(m_strSql);
	ExecuteSql(m_strSql);
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

int DBOper::RecordCnt()
{
	return m_pRst->GetRecordCount();
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
