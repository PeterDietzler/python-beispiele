
#include <stdio.h>
#include <stdlib.h>



void connect(void)
{
	printf("connect() return: hallo_Welt\n");
}

int HalloWelt(void)
{
	return 66;
}

int randNum()
{
	return rand() % 50;
}

int addNum( int a, int b)
{
	return a+b;
}

void printText( char* text)
{
	printf("%s\n", text);
}


char* getText( char* text)
{
	printf("%s",text);
	return text;
}

