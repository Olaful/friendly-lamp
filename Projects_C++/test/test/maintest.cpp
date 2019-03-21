#include"test.h"

	template <typename T>
	inline T const& Max (T const& a, T const& b) 
	{ 
    return a < b ? b:a; 
	}

	void *pthdsendMsg(void *args)
	{
		try
		{
			myWinsocket objmyWinsocket;

			objmyWinsocket = *((myWinsocket*)args);

			int nRevbufsize = 1024;

			string strSend;

			while (true)
			{
				strSend = "";
				// 清除错误状态
				cin.clear();
				// 清除输入缓冲区
				cin.sync();

				cout << "发送的信息:";
				// cin输入中含有空格的话，会以空格为分隔符把输入的内容分段，下一次cin的时候就自动把未送到缓存区的分段信息输入到缓存区
				//cin >> szSendbuf;
				getline(cin, strSend);
				objmyWinsocket.sendMsg(strSend.c_str(), nRevbufsize);
			}
		}
		catch (const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}

		return NULL;
	}

	void *pthdRecvMsg(void *args)
	{
		try
		{
			myWinsocket objmyWinsocket;

			objmyWinsocket = *((myWinsocket*)args);

			char szRevbuf[1024];
			szRevbuf[0] = '\0';
			int nRevbufsize = sizeof(szRevbuf);

			while (true)
			{
				cout << "客户端消息:";
				objmyWinsocket.revMsg(szRevbuf, nRevbufsize);
				cout << szRevbuf << endl;
				szRevbuf[0] = '\0';
			}
		}
		catch (const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}

		return NULL;
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

	char cSwitch = 'a';

	if (cSwitch == 'a')
	{
			int i = 39;
			int j = 20;
			cout << "Max(i, j): " << Max(i, j) << endl;

			int p4[5] = {1, 2, 3, 4, 5};
			char *p = "ppppp";
			char c = 0xff;
			// 根据ascii表，十六进制的a对应LF(换行键) 不可显示字符
			unsigned char cc = 0xa;
			// 7 ->BEL(响铃)
			char ccc = 0x7;
			// 21->! 可显示字符
			char cccc = 0x21;
			// '\0'结尾，所以最多为4个字符
			char p1[5] = "Dddd"; 
			char p2[5] = "dddd";
			char sz[] = "abcdf";
			char *szPtr[] = {"you", "me", "him"};
			unsigned int a = 1;
			int b = 10;
			// 0xff转换成十进制255
			int a2 = 0xff;
		
			cout << "get cc:" << cc << endl;
			cout << "get ccc:" << ccc << endl;
			cout << "get cccc:" << cccc << endl;
			cout << "get c:" << c << endl;
			cout << "get a:" << a2 << endl;
			// -2的补码1.....10, 其中int转换成unsigned int 符号位1被当作数值位
			cout << "a*(-2):" << a * (-2) << endl;
			// 位运算符 b*2^1
			cout << "b << 1:" <<  (b<<1 )<< endl;	
			cout << "b >> 1:" << (b >> 1) << endl;
			cout << szPtr[0] << endl;
			// 指针从它指向的首地址开始读取内容
			cout << "get p content:" << p << endl; 
			cout << "get p adress :" << &p << endl;
			cout << "get *p:" << *p << endl;
			cout << "get p+1 adress :" << &p+1 << endl;
			cout << "get p+2 adress :" << &p+2 << endl;
			cout << "get p head+1 :" << p+1 << endl;
			cout << "get p head-1 :" << p-1 << endl;
			cout << "get sizeof(p4) :" << sizeof(p4) << endl;
			cout << "get sizeof(*p4) :" << sizeof(*p4) << endl;
			// 获取指针变量的长度
			cout << "get sizeof(*p) :" << sizeof(*p) << endl; 
			// 获取占用的内存长度 32位编译器下结果是4，64位是8
			cout << "get sizeof(p) :" << sizeof(p) << endl; 
			// 获取内容长度
			cout << "get strlen(p) :" << strlen(p) << endl; 
			cout << "get sizeof(p1) :" << sizeof(p1) << endl;
			cout << "get strlen(p1) :" << strlen(p1) << endl;
			cout << "get sizeof(sz) :" << sizeof(sz) << endl;

			cout << "get p1+1:" << p1+1 << endl;
			cout << "get p1-1:" << p1 - 1 << endl;
			cout << "get p1[4]:" << p1[4] << endl;
			cout << "get *p1+1:" << *p1+1 << endl;
			cout << "get *p2+1:" << *p2+1 << endl;
			cout << "get type p4:" << typeid(p4).name() << endl;

			// 'a' ascii转换成十进制97后加1
			cout << "get ascii++:" << 'a'+1 << endl; 
			// 相当于指针向右移动一位
			cout << "get str++:" << "dddd"+1 << endl; 

			char *p3 = p1;
			cout << "get p3:" << p3 << endl; 
	}
	
	if (cSwitch == 'b')
	{
		A *objA;

		B objB;
		// 指针地址传值才能实现虚函数多态
		objA = &objB;	
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

		// 调用有参构造函数
		A objA2(5, "hello");
		Object::E objE(&objA2);
		objE.Print();

		// 把类模板F实例化为F类, 如何不加<参数类型>则无法实例化F类
		F<int> objF;	
		cout << objF.add(2,3) << endl;

		// 把类模板F实例化为F类
		F<float> objF1;	
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
		// 以输出方式打开(内存到文件) 打开并清空文件
		ofstream destfile("E:\\C++\\myfile\\3.txt", ios::out|ios::trunc); 
	
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
				// strcmp 返回值  参数1>参数2 1  参数1<参数2 -1 参数1=参数2 0
				if(strcmp(temp1.c_str(), temp2.c_str()) == 0) 
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

		sourcefile1.close();
		sourcefile2.close();
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
 
			if (cAtion == 'Q') 
			{
				strcpy_s(sql, "select* from test");
				//pRst = dbOper.ExecuteSql(sql);

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
						// 0表示第一个字段
					    vSno = pRst->GetCollect(_variant_t((long)0)); 
					    vName = pRst->GetCollect(_variant_t("name"));
 
					    printf("%s\t%s\n",(LPSTR)(LPCSTR)(_bstr_t)vSno, (LPSTR)(LPCSTR)_bstr_t(vName));
					    pRst->MoveNext();
					}
				}
			}
			else if (cAtion == 'A')
			{
				// 开始事务
				dbOper.TransBegin(); 
				strcpy_s(sql, "insert into test(ID, NAME) values(7, '你好')");
				//pRst = dbOper.ExecuteSql(sql);

				_RecordsetPtr pRst1;
				//pRst1 = dbOper.ExecuteSql("insert into test(ID, NAME) values(7, '你好')");

				if (NULL !=pRst && NULL != pRst1)
				{
					printf("插入数据成功\n");
				}
				else
				{
					// 回滚事务
					dbOper.RollbakTrans(); 
				}
				// 检查未提交事务并提交
				dbOper.CheckCommit(); 
			}
			else if (cAtion == 'D')
			{
				sprintf_s(sql, "deletefrom test where id = '%d'",1);
				//pRst = dbOper.ExecuteSql(sql);
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

	if (cSwitch == 'i')
	{
		char *strTest = new char[1];
		int i = 0;
		while (*strTest++)
		{
			i++;
		}
		//strTest = new char[1];
		cout << "size:" << i<< endl;
		// 使用到了隐式转换， 相当于myString str("hello");
		myString str = "hello"; 
		cout << "myString output:" << str.c_str() << endl;
	}

	if (cSwitch == 'j')
	{
		WSADATA wsaData;
		int port = 5099;
		char buf[] = "服务器: 欢迎登录......\n";

		// 加载套接字
		if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		{
			printf("加载套接字失败：%d......\n", WSAGetLastError());
			return 1;
		}

		// socket()
		SOCKET sockSrv = socket(AF_INET, SOCK_STREAM, 0);

		// 初始化IP和端口信息
		SOCKADDR_IN addrSrv;
		addrSrv.sin_family = AF_INET;
		addrSrv.sin_port = htons(port); // 1024以上的端口号
		addrSrv.sin_addr.S_un.S_addr = htonl(INADDR_ANY);

		// bind()
		if (bind(sockSrv, (LPSOCKADDR)&addrSrv, sizeof(SOCKADDR_IN)) == SOCKET_ERROR)
		{
			printf("套接字绑定失败：%d......\n", WSAGetLastError());
			return 1;
		}

		// listen()
		if (listen(sockSrv, 10) == SOCKET_ERROR) {
			printf("套接字监听失败：%d......\n", WSAGetLastError());
			return 1;
		}

		// 客户端信息
		SOCKADDR_IN addrClient;
		int len = sizeof(SOCKADDR);

		// 开始监听
		printf("服务端启动成功......开始监听...\n");
		while (1)
		{
			// 等待客户请求到来  
			// acccept阻塞，有结果返回代码才会往下走, cin也是阻塞的
			SOCKET sockConn = accept(sockSrv, (SOCKADDR *)&addrClient, &len);
			if (sockConn == SOCKET_ERROR) {
				printf("建立连接失败：%d......\n", WSAGetLastError());
				break;
			}

			printf("与客户端建立连接......IP：[%s]\n", inet_ntoa(addrClient.sin_addr));

			// 发送数据
			if (send(sockConn, buf, sizeof(buf), 0) == SOCKET_ERROR) {
				printf("发送数据失败......\n");
				break;
			}

			char recvBuf[100];
			memset(recvBuf, 0, sizeof(recvBuf));
			// 接收数据
			recv(sockConn, recvBuf, sizeof(recvBuf), 0);
			printf("收到数据：%s\n", recvBuf);

			closesocket(sockConn);
		}

		// 关闭套接字
		closesocket(sockSrv);
		WSACleanup();
		system("pause");

		return 0;
	}

	if (cSwitch == 'k')
	{
		WSADATA wsaData;
		int port = 5099;
		char buff[1024];
		memset(buff, 0, sizeof(buff));

		// 加载套接字
		if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
		{
			printf("加载套接字失败：%d......\n", WSAGetLastError());
			return 1;
		}

		// 初始化IP和端口信息
		SOCKADDR_IN addrSrv;
		addrSrv.sin_family = AF_INET;
		addrSrv.sin_port = htons(port);
		addrSrv.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");

		// socket()
		SOCKET sockClient = socket(AF_INET, SOCK_STREAM, 0);
		if (SOCKET_ERROR == sockClient) {
			printf("创建套接字失败：%d......\n", WSAGetLastError());
			return 1;
		}

		// 向服务器发出连接请求
		if (connect(sockClient, (struct  sockaddr*)&addrSrv, sizeof(addrSrv)) == INVALID_SOCKET)
		{
			printf("连接服务器失败：%d......\n", WSAGetLastError());
			return 1;
		}
		else
		{
			// 接收数据
			recv(sockClient, buff, sizeof(buff), 0);
			printf("收到数据：%s\n", buff);

			// 发送数据
			char buf[] = "客户端：请求登录......";
			send(sockClient, buf, sizeof(buf), 0);
		}

		// 关闭套接字
		closesocket(sockClient);
		WSACleanup();

		return 0;
	}

	if(cSwitch == 'l')
	{
		try
		{
			int nPort = 5099;
			char *szIP = "";
			myWinsocket objmyWinsocket(nPort, szIP, '0');

			char szRevbuf[1024];
			szRevbuf[0] = '\0';
			int nRevbufsize = sizeof(szRevbuf);

			string strSend;

			while (true)
			{
				cout << "客户端消息:";
				objmyWinsocket.revMsg(szRevbuf, nRevbufsize);
				cout << szRevbuf << endl;
				szRevbuf[0] = '\0';

				strSend = "";
				// 清除错误状态
				cin.clear();
				// 清除输入缓冲区
				cin.sync();

				cout << "发送的信息:";
				// cin输入中含有空格的话，会以空格为分隔符把输入的内容分段，下一次cin的时候就自动把未送到缓存区的分段信息输入到缓存区
				//cin >> szSendbuf;
				getline(cin, strSend);
				objmyWinsocket.sendMsg(strSend.c_str(), nRevbufsize);
			}
		}
		catch(const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}
	}

	if (cSwitch == 'm')
	{
		try
		{
			int nPort = 5099;
			char *szIP = (argv[1] != NULL ? argv[1] :  "127.0.0.1");
			myWinsocket objmyWinsocket(nPort, szIP, '1');

			char szRevbuf[1024];
			szRevbuf[0] = '\0';
			int nRevbufsize = sizeof(szRevbuf);

			string strSend;

			while (true)
			{
				strSend = "";
				cout << "发送的信息:";
				getline(cin, strSend);
				objmyWinsocket.sendToSrv(strSend.c_str(), nRevbufsize);

				cout << "服务端消息:";
				objmyWinsocket.revSrvMsg(szRevbuf, nRevbufsize);
				cout << szRevbuf << endl;
				szRevbuf[0] = '\0';
			}
		}
		catch (const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}
	}

	if (cSwitch == 'n')
	{
		try
		{
			int nPort = 5099;
			char *szIP = "";
			myWinsocket objmyWinsocket(nPort, szIP, '2');

			char szRevbuf[1024];
			szRevbuf[0] = '\0';
			int nRevbufsize = sizeof(szRevbuf);

			string strSend;

			while (true)
			{
				cout << "客户端消息:";
				objmyWinsocket.recvMsgFrom(szRevbuf, nRevbufsize);
				cout << szRevbuf << endl;
				szRevbuf[0] = '\0';

				strSend = "";
				// 清除错误状态
				cin.clear();
				// 清除输入缓冲区
				cin.sync();

				cout << "发送的信息:";
				// cin输入中含有空格的话，会以空格为分隔符把输入的内容分段，下一次cin的时候就自动把未送到缓存区的分段信息输入到缓存区
				//cin >> szSendbuf;
				getline(cin, strSend);
				objmyWinsocket.sendMsgTo(strSend.c_str(), nRevbufsize);
			}
		}
		catch (const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}
	}

	if (cSwitch == 'o')
	{
		try
		{
			int nPort = 5099;
			char *szIP = (argv[1] != NULL ? argv[1] : "127.0.0.1");
			myWinsocket objmyWinsocket(nPort, szIP, '3');

			char szRevbuf[1024];
			szRevbuf[0] = '\0';
			int nRevbufsize = sizeof(szRevbuf);

			string strSend;

			while (true)
			{
				strSend = "";
				cout << "发送的信息:";
				getline(cin, strSend);
				objmyWinsocket.sendMsgToSrv(strSend.c_str(), nRevbufsize);

				cout << "服务端消息:";
				objmyWinsocket.recvMsgFromSrv(szRevbuf, nRevbufsize);
				cout << szRevbuf << endl;
				szRevbuf[0] = '\0';
			}
		}
		catch (const std::exception& e)
		{
			cout << "错误信息:" << e.what() << endl;
		}
	}

	if (cSwitch == 'p')
	{
		//pthread_t pthsend, pthrecv;

		//try
		//{
		//	int nPort = 5099;
		//	char *szIP = "";
		//	myWinsocket objmyWinsocket(nPort, szIP, '0');

		//// 把函数加入线程中 发送与接受消息各开启一个线程
		//pthread_create(&pthrecv, NULL, pthdRecvMsg, (void*)&objmyWinsocket);
		//pthread_create(&pthsend, NULL, pthdsendMsg, (void*)&objmyWinsocket);

		//// Pthread创建线程后必须使用join或detach释放线程资源
		//pthread_join(pthrecv, NULL);
		//pthread_join(pthsend, NULL);
		//}
		//catch (const std::exception& e)
		//{
		//	cout << "错误信息:" << e.what() << endl;
		//}

		return true;
	}

	if (cSwitch == 'q')
	{
		int sz[] = { 8, 9, 8, 1, 4, 7, 6, 5, 3, 2, 10 };
		int nLen = sizeof(sz) / sizeof(sz[0]);
		int temp;
		for (size_t i = 0; i < nLen; i++)
		{
			for (size_t j = 0; j < nLen - i - 1; j++)
			{
				if (sz[j] > sz[j+1])
				{
					temp = sz[j + 1];
					sz[j + 1] = sz[j];
					sz[j] = temp;
				}
			}
		}
		for (size_t i = 0; i < nLen; i++)
		{
			cout << sz[i] << ",";
		}
	}

	system("pause");
}