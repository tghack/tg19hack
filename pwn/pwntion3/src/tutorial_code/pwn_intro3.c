#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

void print_secret_message(void)
{
	system("cat flag.txt");
}

void answer_professor(void)
{
	char spell_name[20];

	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Professor maritio_o:\n");
	printf("Does anyone remember the name of the spell we made last lecture?\n");

	read(STDIN_FILENO, spell_name, 64);
}

int main(void)
{
	answer_professor();

	return 0;
}
