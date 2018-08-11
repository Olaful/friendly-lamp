#include"test.h"


	template <typename T>
	inline T const& Max (T const& a, T const& b) 
	{ 
    return a < b ? b:a; 
	}

//void main()	// main中无return的话编译器会自动在目标文件中加入return 0，不过最好在编码时就使用int main(int argc, char *argv[])
int main(int argc, char *argv[])
{
	cout << "welcome" << endl;
	cout << "参数个数:" << argc << endl;

	for (size_t i = 0; i < argc; i++)
	{
		cout << "参数值：" << argv[i] << endl;
	}

	SYSTEMTIME st;
	::GetLocalTime(&st);
	char szTime[32];
	sprintf_s(szTime, "systemtime: %d/%d/%d %d:%d:%d\n", st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
	cout << szTime << endl;

	char cSwitch = 'b';

	if (cSwitch == 'a')
	{
			int i = 39;
			int j = 20;
			cout << "Max(i, j): " << Max(i, j) << endl;

			int p4[5] = {1, 2, 3, 4, 5};
			char *p = "pppp";
			char p1[5] = "Dddd"; // '\0'结尾，所以最多为4个字符
			char p2[5] = "dddd";
			char sz[] = "abcdf";
			char *szPtr[] = {"you", "me", "him"};
			unsigned int a = 1;
			int b = 10;

			cout << "a*(-2):" << a * (-2) << endl;	// -2的补码1.....10, 其中int转换成unsigned int 符号位1被当作数值位
			cout << "b << 1:" <<  (b<<1 )<< endl;	// 位运算符 b*2^1
			cout << "b >> 1:" << (b >> 1) << endl;
			cout << szPtr[0] << endl;
			cout << "get p content:" << p << endl; // 指针从它指向的首地址开始读取内容
			cout << "get p adress :" << &p << endl;
			cout << "get *p:" << *p << endl;
			cout << "get p+1 adress :" << &p+1 << endl;
			cout << "get p+2 adress :" << &p+2 << endl;
			cout << "get p head+1 :" << p+1 << endl;
			cout << "get p head-1 :" << p-1 << endl;
			cout << "get sizeof(p4) :" << sizeof(p4) << endl;
			cout << "get sizeof(*p4) :" << sizeof(*p4) << endl;
			cout << "get sizeof(*p) :" << sizeof(*p) << endl; // 获取指针变量的长度
			cout << "get sizeof(p) :" << sizeof(p) << endl; // 获取占用的内存长度 32位编译器下结果是4，64位是8
			cout << "get strlen(p) :" << strlen(p) << endl; // 获取内容长度
			cout << "get sizeof(p1) :" << sizeof(p1) << endl;
			cout << "get strlen(p1) :" << strlen(p1) << endl;
			cout << "get sizeof(sz) :" << sizeof(sz) << endl;

			cout << "get p1+1:" << p1+1 << endl;
			cout << "get p1-1:" << p1 - 1 << endl;
			cout << "get p1[4]:" << p1[4] << endl;
			cout << "get *p1+1:" << *p1+1 << endl;
			cout << "get p2:" << *p2+1 << endl;
			cout << "get type p4:" << typeid(p4).name() << endl;

			cout << "get ascii++:" << 'a'+1 << endl;   // 'a' ascii转换成十进制97后加1
			cout << "get str++:" << "dddd"+1 << endl; // 相当于指针向右移动一位

			char *p3 = p1;
			cout << "get p3:" << p3 << endl; 
	}
	
	if (cSwitch == 'b')
	{
		A *objA;

		B objB;
		objA = &objB;	// 指针地址传值才能实现虚函数多态
		int sum = objA->add(1234, 2);
		cout << "a+b:" << sum << endl;

		float fArea = objB.GetTriangleArea(1.0, 3.0);
		cout << "triarea:" << fixed << setprecision(2) << fArea << endl;

		//A objA1;
		//B objB1();
		//objA1 = objB1;
		//int sum1 = objA1.add(1, 2);
		//cout << "a+b:" << sum1 << endl;

		//C objC;
		//A *objA2 = &objC;
		//cout << "a+b:" << objA2->add(1, 2) << endl;

		//B objB2;
		//D objD(&objB2);
		//objD.Print();

		A objA2(5, "hello");	// 调用有参构造函数
		Object::E objE(&objA2);
		objE.Print();

		F<int> objF;	// 把类模板F实例化为F类, 如何不加<参数类型>则无法实例化F类
		cout << objF.add(2,3) << endl;

		F<float> objF1;	// 把类模板F实例化为F类
		cout << objF1.add(2.1f,3.1f) << endl;

		F<float> objF2;
		cout << objF2.Sub(2.1,3.1) << endl;

		B objB1;
		objB1.inlinefunc();
		objB1.inner();

		cout << C::Monday << endl;
		cout << C::Tuesday << endl;
		cout << C::Wednesday << endl;

		D objD;
		char szDst[3];
		char *szSrc = "source";

		objD.mySprintf(szDst, sizeof(szDst) - 1, szSrc);
		cout << "mySprintf:" << szDst << endl;
	}

	if (cSwitch == 'c')
	{
		ifstream sourcefile("E:\\C++\\myfile\\1.txt");
		ofstream destfile("E:\\C++\\myfile\\2.txt", ofstream::app);

		string temp;
		if (!sourcefile.is_open())
		{
			cout << "文件E:\\C++\\myfile\\1.txt不能成功打开" << endl; 
		}

		while (getline(sourcefile, temp))
		{
			destfile << temp;
		}
	}

	// 使用外部dll
	if (cSwitch == 'd')
	{
#ifdef _WIN64
		cout << "Sub:" << Sub(10, 5) << endl;
#endif // _WIN64
		//cout << "Add:" << Add(10, 5) << endl;
	}

	if (cSwitch == 'e')
	{
		float fData = GetArea(2);
		cout << "data:" << fData << endl;
	}

	if(cSwitch == 'f')
	{
		// fstream 继承于iostream, iostream 同时继承于istream与ostream， ifstream继承于istream，ofstream继承于ostream
		ifstream sourcefile1("E:\\C++\\myfile\\1.txt");
		ifstream sourcefile2("E:\\C++\\myfile\\2.txt");
		ofstream destfile("E:\\C++\\myfile\\3.txt", ios::out|ios::trunc); // 以输出方式打开(内存到文件) 打开并清空文件
	
		string temp1;
		string temp2;
		string temp3 = "";

		if (!sourcefile1.is_open())
		{
			cout << "文件E:\\C++\\myfile\\1.txt不能成功打开" << endl; 
		}
		if (!sourcefile2.is_open())
		{
			cout << "文件E:\\C++\\myfile\\2.txt不能成功打开" << endl; 
		}
		
		while (getline(sourcefile1, temp1))
		{
			while(getline(sourcefile2, temp2))
			{
				if(strcmp(temp1.c_str(), temp2.c_str()) == 0) // strcmp 返回值  参数1>参数2 1  参数1<参数2 -1 参数1=参数2 0
				{
					temp3 = "";
					break;
				}
				else
				{
					temp3 = temp1;
				}
			}

			if (!temp3.empty())
				destfile << temp3 + "\n";

			// 清楚流标志位并定位到开头
			sourcefile2.clear();
			sourcefile2.seekg(0);
		}
	}

	if (cSwitch == 'g')
	{
		DBOper dbOper;
   
		bool bConn=dbOper.ConnToDB("Provider=OraOLEDB.Oracle;Persist Security Info=True;DataSource=ORCLss","tbq","tbq");
		if (false == bConn)
		{
		    printf("连接数据库出现错误\n");
		}
		else
		{
			printf("连接数据库成功!\n");

			_RecordsetPtr pRst;

			char cAtion = 'Q';
			char sql[255] = { 0 };
 
			if (cAtion == 'Q') // 查询数据
			{
				strcpy_s(sql, "select* from test");
				pRst = dbOper.ExecuteSql(sql);

				if (NULL == pRst)
				{
				    printf("查询数据出现错误！\n");
				}
				else if(pRst->adoEOF)
				{
				    pRst->Close();
				    printf("Thereis no records in this table\n");
				}
				else
				{
					printf("正在查询...\n");
					printf("ID\tNAME\n");
					_variant_t vSno, vName;
					while(!pRst->adoEOF)
					{
					    //pRst->MoveFirst();//记录集指针移动到查询结果集的前面
					    vSno = pRst->GetCollect(_variant_t((long)0)); // 0表示第一个字段
					    vName = pRst->GetCollect(_variant_t("name"));
 
					    printf("%s\t%s\n",(LPSTR)(LPCSTR)(_bstr_t)vSno, (LPSTR)(LPCSTR)_bstr_t(vName));
					    pRst->MoveNext();
					}
				}
			}
			else if (cAtion == 'A')	// 插入数据
			{
				dbOper.TransBegin(); // 开始事务
				strcpy_s(sql, "insert into test(ID, NAME) values(7, '你好')");
				pRst = dbOper.ExecuteSql(sql);

				_RecordsetPtr pRst1;
				pRst1 = dbOper.ExecuteSql("insert into test(ID, NAME) values(7, '你好')");

				if (NULL !=pRst && NULL != pRst1)
				{
					printf("插入数据成功\n");
				}
				else
				{
					dbOper.RollbakTrans(); // 回滚事务
				}
				dbOper.CheckCommit(); // 检查未提交事务并提交
			}
			else if (cAtion == 'D')	// 删除数据
			{
				sprintf_s(sql, "deletefrom test where id = '%d'",1);
				pRst = dbOper.ExecuteSql(sql);
				if (NULL !=pRst)
				{
					printf("删除数据成功\n");
				}
			}
		}
	}

	if (cSwitch == 'h')
	{
		DBOper dbOper("tbq","tbq");

		string sql = "select * from test";

		int nID = 0;
		char szName[16] = "";

		dbOper.Open(sql);
		dbOper.Execute();
		cout << "id" << "\t" << "name" << endl;
		while(!dbOper.Eof())
		{
			dbOper.GetValue("id", nID);
			dbOper.GetValue("name", szName);
			cout << nID << "\t";
			cout << szName << endl;
			dbOper.MoveNext();
		}

		dbOper.Close();

		dbOper.Open(sql);

	}

	system("pause");
}