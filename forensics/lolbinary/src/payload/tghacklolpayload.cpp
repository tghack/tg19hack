#include <winsock2.h>
#include <WS2tcpip.h>
#include <windows.h>
#include <iostream>
#pragma comment(lib,"ws2_32.lib")
using namespace std;

string crypto(const char* instring) {
	string sout = "";
	int instrlen = strlen(instring);
	for (int i = 0; i < instrlen; i++) {
		sout += instring[i] ^ instrlen;
	}
	//const char* out = sout.c_str();
	return sout;
}

int makerequest(const char* hostnstrn, const char* urlstrn) {
	WSADATA wsaData;
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		return -1;
	}

	struct addrinfo hints;
	ZeroMemory(&hints, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_protocol = IPPROTO_TCP;
	hints.ai_socktype = SOCK_STREAM;

	struct addrinfo* targetAdressInfo = NULL;
	DWORD getAddrRes = getaddrinfo(hostnstrn, NULL, &hints, &targetAdressInfo);
	if (getAddrRes != 0 || targetAdressInfo == NULL)
	{
		cout << "Error resolving hostname" << endl;
		WSACleanup();
		return -1;
	}

	SOCKADDR_IN sockAddr;
	sockAddr.sin_addr = ((struct sockaddr_in*) targetAdressInfo->ai_addr)->sin_addr;
	sockAddr.sin_family = AF_INET;
	sockAddr.sin_port = htons(80);
	freeaddrinfo(targetAdressInfo);

	SOCKET webSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (webSocket == INVALID_SOCKET)
	{
		cout << "Error creating socket" << endl;
		WSACleanup();
		return -1;
	}

	if (connect(webSocket, (SOCKADDR*)& sockAddr, sizeof(sockAddr)) != 0)
	{
		cout << "Error connecting";
		closesocket(webSocket);
		WSACleanup();
		return -1;
	}

	//bulding http request

	const char* ehttpmethod = "\x43\x41\x50\x24"; // "GET "
	const char* ehttpver = "\x29\x41\x5d\x5d\x59\x26\x38\x27\x38"; // " HTTP/1.1"
	const char* ehttphost = "\x4e\x69\x75\x72\x3c\x26"; // "Host: "
	const char* ehttpheaderua = "\x59\x7f\x69\x7e\x21\x4d\x6b\x69\x62\x78\x36\x2c"; // "User-Agent: "
	const char* euseragnt = "\x7c\x6a\x6c\x7d\x6a\x7b\x7c\x7b\x7d\x66\x61\x68\x64\x6a\x76"; // "secretstringkey"
	const char* ehttpclose = "\x52\x7e\x7f\x7f\x74\x72\x65\x78\x7e\x7f\x2b\x31\x72\x7d\x7e\x62\x74"; // "Connection: close"

	string shttpmethod = crypto(ehttpmethod);
	string shttpver = crypto(ehttpver);
	string shttphost = crypto(ehttphost);
	string shttpheaderua = crypto(ehttpheaderua);
	string suseragnt = crypto(euseragnt);
	string shttpclose = crypto(ehttpclose);

	const char* httpmethod = shttpmethod.c_str();
	const char* httpver = shttpver.c_str();
	const char* httphost = shttphost.c_str();
	const char* httpheaderua = shttpheaderua.c_str();
	const char* useragnt = suseragnt.c_str();
	const char* httpclose = shttpclose.c_str();

	char httpRequest[150];
	sprintf_s(httpRequest, "%s%s%s%s%s%s%s%s%s%s%s%s", httpmethod, urlstrn, httpver, "\r\n", httphost, hostnstrn, "\r\n", httpheaderua, useragnt, "\r\n", httpclose, "\r\n\r\n");
	cout << httpRequest;

	int sentBytes = send(webSocket, httpRequest, strlen(httpRequest), 0);
	if (sentBytes < strlen(httpRequest) || sentBytes == SOCKET_ERROR)
	{
		cout << "Error sending HTTP request" << endl;
		closesocket(webSocket);
		WSACleanup();
		return -1;
	}

	char buffer[10000];
	ZeroMemory(buffer, sizeof(buffer));
	int dataLen;
	while ((dataLen = recv(webSocket, buffer, sizeof(buffer), 0) > 0))
	{
		int i = 0;
		while (buffer[i] >= 32 || buffer[i] == '\n' || buffer[i] == '\r') {
			cout << buffer[i];
			i += 1;
		}
	}

	closesocket(webSocket);
	WSACleanup();
	return 0;
}

#pragma optimize( "", off )
int getflag() {
	const char* ehost = "\x6d\x65\x65\x6d\x66\x6f\x24\x69\x65\x67"; // "google.com"
	const char* eurl = "\x2e"; // "/"

	const char* thost = "\x61\x60\x7b\x6c\x3d\x21\x7b\x68\x67\x6e\x6c\x64\x21\x61\x60"; // "notc2.tghack.no"
	const char* turl = "\x26\x6e\x6c\x7d\x56\x6f\x65\x68\x6e"; // "/get_flag"
	
	string shost = crypto(ehost);
	string surl = crypto(eurl);
	const char* host = shost.c_str();
	const char* url = surl.c_str();

	if (makerequest(host, url))
		return 0;
	else
		return 1;
}
#pragma optimize( "", on )

int main() {
	int lol = getflag();
	return lol;
}