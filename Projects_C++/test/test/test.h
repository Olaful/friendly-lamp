#include<stdlib.h>
#include<iostream>
#include<fstream>
#include<string>
#include<iomanip>
#include<sstream>
#include <windows.h>
#include "oracledb.h"

using   namespace   std;

#ifdef _WIN64
	#include "MyAPI.h"
	#pragma comment(lib, "MyAPI.lib")
#endif // _WIN64

#ifdef PI
#pragma message("PI 宏已定义")
#endif

#ifdef MAX
#pragma message("MAX 宏已定义")
#endif

class A
{
public:
	static int nNum; // 所有对象共用
	A()
	{
		m_iData = 1;
		m_pData = "hi";
		nNum++;
	}

	A(int a, char *b) // 有参构造函数
	{
		m_iData = a;
		m_pData = b;
		nNum++;
	}

	virtual int add(double a, double b)
	{	
		if(strcmp(typeid(a).name(), "int") == 0 && strcmp(typeid(b).name(), "int") == 0)
		{
			return a + b;
		}
		else
		{
			cout << "请输入正确的数字" << endl;
		}
	}

	float GetTriangleArea(float bottom, float height)
	{
		return bottom * height / 2;
	}

public:
	int m_iData;
	char *m_pData;

protected:	// 不可通过实例对象访问
	bool Check(double a, double b)
	{
		stringstream ss;
		ss << a;

		//while(a)
		//{
		//	a /= 10;
		//	iLen++;
		//}

		if(ss.str().length() >= 3)
		{
			cout << a << "长度超过3" << endl;
			return false;
		}

		ss.str("");
		ss << b;

		if(ss.str().length() > 4)
		{
			cout << b << "长度超过3" << endl;
			return false;
		}
		
		return true;
	}

	// virtual int sub() = 0;
};

class B : public A
{
public:
	B()
	{
		m_nData = 0;
		m_szData = NULL;
	};

	int add(double a, double b)
	{
		if (Check(a, b))
		{
			return a*2 + b*2;
		}
	}

	void print()	// 类中定义实现的函数会被内联处理
	{
		cout << m_nData << "," << m_nData << endl;
	}

	void oper() /*const*/  // 如加const，则报错  // 不加const只能被非const成员函数调用
	{
		m_nData = 1;
	}

	// static B obj();

	void inner();	// 此内部没有定义的函数不会被内联处理

	inline void inlinefunc()	// 编译阶段在被调用的地方会以函数体{}替代，代码俩较少且经常使用时建议内联
	{
		cout << "This is a inline func" << endl;
	}

private:
	int m_nData;
	char *m_szData;
};

class C : public B
{
public:
	int add(int a, int b)
	{	
		if(strcmp(typeid(a).name(), "int") == 0 && strcmp(typeid(b).name(), "int") == 0)
		{
			return a*3 + b*3;
		}
		else
		{
			cout << "请输入正确的数字" << endl;
		}
	}

	enum day
	{
		Monday = 1, // enum中成员默认从数字0开始的
		Tuesday = 3, // 以下的成员值从此处递增，下一个为4
		Wednesday,
		Thursday,
		Friday
	};

#define GetArea(r) 3.141576964357 * r * r;
		
};

class D
{
public:
	D() {};

	D(A *parent) : m_objA(parent)
	{}

	int add(int a, int b)
	{	
		if(strcmp(typeid(a).name(), "int") == 0 && strcmp(typeid(b).name(), "int") == 0)
		{
			return a*2 + b*2;
		}
		else
		{
			cout << "请输入正确的数字" << endl;
		}
	}

	void Print()
	{
		cout << m_objA->m_iData << "," << m_objA->m_pData << endl;
	}

	void mySprintf(char *szDst, unsigned int strlen, const char *szSrc)	// 自定义安全拷贝函数
	{
		if (szDst == NULL ||  szSrc == NULL)
		{
			return;
		}

		unsigned int len = 0;
		while (*szSrc != '\0' && len < strlen)
		{
			*szDst++ = *szSrc++;
			len++;
		}

		*szDst = '\0';
	}

private:
	A *m_objA;
};

int A::nNum;	// static成员需定义后才可以使用

struct Object
{
	class E;
};

class Object::E
{
public:
	E(A *parent) : m_objA(parent)
	{}

	int operator() (char *tmp)	// 函数对象
	{
		cout << tmp << endl;
	}

	int add(int a, int b)
	{	
		if(strcmp(typeid(a).name(), "int") == 0 && strcmp(typeid(b).name(), "int") == 0)
		{
			return a*2 + b*2;
		}
		else
		{
			cout << "请输入正确的数字" << endl;
		}
	}

	void Print()
	{
		cout << m_objA->m_iData << "," << m_objA->m_pData << "," << m_objA->nNum << "," << endl;
	}

private:
	A *m_objA;
};

template<class TYPE>
class F
{
public:
	TYPE add(TYPE a, TYPE b)
	{	
		return a*2 + b*2;
	}

	TYPE Sub(TYPE a, TYPE b);
private:
};

template<class TYPE>	// 在外部定义类模板的成员需加上虚拟类型定义
TYPE F<TYPE>::Sub(TYPE a, TYPE b)
{
	return a*2 - b*2;
}

void B::inner()
{
	cout << "This is out defined" << endl;
}