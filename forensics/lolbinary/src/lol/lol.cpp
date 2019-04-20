#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <windows.h>

using namespace std;

string someotherfunc() {
	string lol = "";
	int a = 108;
	int b = 111;
	int c = 1;
	if (a * b / c > 41) {
		lol += static_cast<char>(a);
		lol += static_cast<char>(b);
		lol += static_cast<char>(a);
	}
	return lol;
}

//junk func
int somefunc() {
	Sleep(500);
	srand(21);
	Sleep(500);
	int w = 0;
	int x = 0;
	while (w == 0){
		Sleep(100);
		x = rand() % 123 + 1;
		int y = rand();
		int z = rand() % 10;

		if (x < y) {
			if (z + 1000 > y) {
				w += 1;
			}
		}
	}
	return x;
}

int main(void) {
	int thonk = somefunc();
	Sleep(500);

	if (thonk > 1) {
		string ret = someotherfunc();
		cout << ret;
		Sleep(500);
		return 0;
	} else {
		return 1;
	}
}