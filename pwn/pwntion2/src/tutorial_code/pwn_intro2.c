#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

struct magical_spell {
    char name[32];
    int age;
    int is_awesome;
};

int main() 
{
    setvbuf(stdout, NULL, _IONBF, 0);

    /* Declaring variables */
    struct magical_spell pwntion_spell;
    memset(&pwntion_spell, 0, sizeof(pwntion_spell));
    pwntion_spell.age = 1337000000;
    pwntion_spell.is_awesome = 0;
    
    /* Printing text to terminal */
    printf("Professor maritio_o:\n");
    printf("Tell me a pwntion spell name!\n");
    printf("Pwntion spell name:\n");
    printf("> ");
     
    /* Read 64 bytes of user input from terminal, 
	 * and put into pwntion.spell_name */
    read(STDIN_FILENO, pwntion_spell.name, 64);
    
    /* Printing text to terminal*/
    printf("%s\n", pwntion_spell.name);
    printf("%d\n", pwntion_spell.age);
    printf("%d\n", pwntion_spell.is_awesome);
    
    /* if statement*/
    if (pwntion_spell.age == 1337000000 && pwntion_spell.is_awesome == 1) {
        printf("Amazing! You did it, awesome student at school of wizardry!\n");
        system("cat flag.txt");
    } else {
        printf("Hmm, look's like Pwnie isn't telling you a word...\n");
    }
     
    return 0;
}
