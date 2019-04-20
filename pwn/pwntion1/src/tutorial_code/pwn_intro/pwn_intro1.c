#include <stdio.h>
#include <unistd.h>

int main(void)
{
	/* Declare variables */
	char secret_message[] = "TG19{This_is_a_dummy_flag}";
	char magical_buffer[64];
	
	/* Send output to terminal */
	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Give me some magical spell!\n");
	
	/* Fetch input */
	read(STDIN_FILENO, magical_buffer, 128);
	
	/* Print name to terminal */
	printf("%s\n", magical_buffer);
	
	return 0;
}
