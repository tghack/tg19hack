#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

struct question {
	char question[48];
	int is_magical_question;
};

static void answer_professor(void)
{
	/* Make stdout unbuffered, ensures that 
	 * all output is sent immediately. No magic here. */
	setvbuf(stdout, NULL, _IONBF, 0);

	/* Declaring variables */
	struct question student_question;
	memset(&student_question, 0, sizeof(student_question));

	/* Printing text to terminal, no magic here. */
	printf("\n\nProfessor maritio_o:\n");
	printf("> Welcome to the second class about stack overflow pwntions!\n");
	printf("> Pls don't hesitate to ask questions!\n\n");
	printf("Student:\n");
	printf("> ");

	/* Read 64 bytes of user input from terminal, 
	* and put into student_question. */
	read(STDIN_FILENO, student_question.question, 64);

	printf("%s\n", student_question.question);

	if (student_question.is_magical_question == 1) {
		printf("Professor maritio_o:\n");
		printf("> Excellent! Ten points to your house!\n");
		printf("> ");

		/* You should definitely Google the next 
		 * line if you don't know what it does */
		system("cat flag.txt");
	} else {
		printf("Professor maritio_o:\n");
		printf("> That's a good question, you should Google that!\n");
	}
}

/* You can ignore this function, it just prints the banner */
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
	print_banner();
	answer_professor();

	return 0;
}
