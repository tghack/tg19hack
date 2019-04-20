#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define SERIAL_LEN 24

static int check_pair(char a, char b)
{
	return ((a ^ b ^ 0x42) < 70);
}

static int check_pair_part2(char a, char b)
{
	return ((a ^ b ^ 0x13) > 30);
}

static int is_alphanum(const char *buf)
{
	for (size_t i = 0; i < strlen(buf); i++) {
		if (!isalnum(buf[i]))
			return 0;
	}

	return 1;
}

static int valid_serial(const char *buf)
{
	size_t len = strlen(buf);

	if (len != SERIAL_LEN)
		return 0;

	if (!is_alphanum(buf))
		return 0;

	for (size_t i = 0; i < (len / 2); i += 2) {
		if (!check_pair(buf[i], buf[i + 1]))
			return 0;
	}

	for (size_t i = (len / 2); i < len; i += 2) {
		if (!check_pair_part2(buf[i], buf[i + 1]))
			return 0;
	}

	return 1;
}

int main(void)
{
	char buf[SERIAL_LEN + 2] = { 0 };

	setvbuf(stdout, NULL, _IONBF, 0);
	printf("Serial please: ");

	if (!fgets(buf, sizeof(buf), stdin)) {
		perror("fgets()");
		exit(EXIT_FAILURE);
	}

	buf[strcspn(buf, "\n")] = '\0';

	if (valid_serial(buf)) {
		printf("yay!\n");
		return 0;
	}

	printf("nay!\n");
	
	return 1;
}
