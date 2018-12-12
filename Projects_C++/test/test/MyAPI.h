#ifndef _DLL_API
#define _DLL_API _declspec(dllexport)
#else
#define _DLL_API _declspec(dllimport)
#endif

_DLL_API int Sub(int a, int b);

int Add(int a, int b);