#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

static void answer_professor(void)
{
	char flag[] = "TG19{This is a dummy flag. Real flag on server.}";
	char student_answer[32] = { 0 };

	/* Printing intro text, no magic here*/
	printf("\n\nProfessor maritio_o:\n");
	printf("\"As there is little foolish wand-waving here, many of you will\n"
		"hardly believe this is magic. I don't expect you will really\n"
		"understand the beauty of the softly simmering cauldron with\n"
		"its shimmering fumes, the delicate power of liquids that\n"
		"creep through the human veins, bewitching the minds, ensnaring\n"
		"the senses... I can teach you how to bottle fame, brew glory,\n"
		"and even stopper death - if you aren't as big a bunch of\n"
		"dunderheads as I usually have to teach.\"\n\n");
	printf("Student:\n");

	/* Read 48 bytes of user input from terminal, and put into student_answer*/
	read(STDIN_FILENO, student_answer, 48);

	printf("%s\n", student_answer);
}

/* Just for printing banner, no magic here*/
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
}

int main(void) 
{
	setvbuf(stdout, NULL, _IONBF, 0);
	print_banner();
	answer_professor();

	return 0;
}
