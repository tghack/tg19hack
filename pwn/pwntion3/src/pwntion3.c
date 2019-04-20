#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void brew_pwntion(void)
{
	system("cat flag.txt");
}

void answer_professor(void)
{
	char pwntion[32];

	printf("\nProfessor maritio_o:\n");
	printf("> I've made a function for you, my magnificent students! Do ");
	printf("a little brewing and show me what you are good for!\n\n");
	printf("Student: ");

	read(STDIN_FILENO, pwntion, 128);
}

/* Don't mind me, I just print the banner*/
static void print_banner(void)
{
	FILE *fp;
	char *buf;
	size_t size;

	fp = fopen("banner.txt", "r");
	if (!fp) {
		perror("fopen(banner.txt)");
		exit(EXIT_FAILURE);
	}

	fseek(fp, 0, SEEK_END);
	size = ftell(fp);
	buf = calloc(1, size);
	rewind(fp);

	/* -1 to drop newline */
	if (fread(buf, size - 1, 1, fp) < 1) {
		perror("fread()");
		exit(EXIT_FAILURE);
	}

	fclose(fp);

	printf("%s\n", buf);
	free(buf);
}

int main(void) 
{
	setvbuf(stdout, NULL, _IONBF, 0);
	print_banner();
	answer_professor();

	return 0;
}
