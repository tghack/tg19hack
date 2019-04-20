#include <stdio.h>
#include <inttypes.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static const char *welcome_str = "Welcome! The current time is %s";
static char buf[128];

static void __attribute__((constructor)) initialize(void)
{
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);
	alarm(40);

	time_t now = time(NULL);
	struct tm *t = localtime(&now);
	snprintf(buf, sizeof(buf) - 1, welcome_str, asctime(t));
}

static void __attribute__((noinline)) do_flip(void)
{
	uint8_t *addr;
	uint32_t bit;

	printf("Enter addr:bit to flip: ");
	fscanf(stdin, "%p:%u", (void **)&addr, &bit);

	if (bit > 7)
		exit(EXIT_FAILURE);

	uint8_t tmp = *addr;
	tmp ^= (1 << bit);
	*addr = tmp;
}

int main(void)
{
	puts(buf);
	printf("I'll let you flip 5 bits, but that's it!\n");

	for (int i = 0; i < 5; i++)
		do_flip();

	printf("Thank you for flipping us off!\nHave a nice day :)\n");

	exit(EXIT_SUCCESS);
}
