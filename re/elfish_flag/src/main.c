#include <stdio.h>
#include <string.h>

void flaggy(unsigned char* a, unsigned char* b, unsigned char* c){

    /* Junk code */
    unsigned char x[sizeof(c)];
    unsigned char lol[] = "TG";
    int e;

    if(c){
        for(e=0;e++;e<=sizeof(c)){
            x[e] = lol[e % 2] ^ c[e];  
        }
    }

    /* Actual flag check*/
    int i = 0;
    while(a[i] + 100 == b[i]){
        i++;
    }
    
    if(i == 25){
        printf("Congratz, you found the flag!");
    } else {
        printf("Sorry, try harder!");
    }
}

int main(int argc, char *argv[])
{
    unsigned char a[] = "\xc5\x9a\x80\x7c\x57\x21\x2a\x9a\xf5\xd5\xa6\x89\x13\x9e\xe4\xfc\x8c\x4e\x1a\x4c\x3b\xbe\x38\xba\xe9\xfb\x9d\x1c\x4b\x24\x0c\x03";
    unsigned char b[] = "\xb8\xab\x95\x9d\xdf\xca\xd0\xc5\xcb\xcb\xdd\xd7\xc3\xc6\xc9\xd7\xd8\xc3\xca\xd6\xcd\xc9\xd2\xc8\xe1";
    unsigned char input[26];

    printf("Hello and welcome to my flagcheck challenge!\nEnter the flag to solve this task!\n...How? That is your task to solve! Have fun!\n");
    if(fgets(input,sizeof(input),stdin) > 0){
        flaggy(input,b,a);
    } else {
        printf("Woops!\n");
    }
    return 0;
}
