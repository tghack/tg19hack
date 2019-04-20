# Elfish flag writeup

**Points: 100**

**Author: bolzzy**

**Difficulty: easy**

**Category: reverse engineering**
   
---

First, lets try running the file to get a feel for how the program works:

```
$ chmod +x ./elfish.elf

$ ./elfish.elf
Hello and welcome to my flagcheck challenge!
Enter the flag to solve this task!
...How? That is your task to solve! Have fun!
TEST
Sorry, try harder!%
```

Alright, so we are tasked to input the flag... without knowing the flag!
Lets look at the dissasembly and decompiled code in a reverse engineering framework called Ghidra.
When we look at the `main` function, we see that some local variables are set before the text is printed and we are asked for input.


From Ghidras decompiled output:
```
..
..
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_38 = 0x9a2a21577c809ac5;
  local_30 = 0xfce49e1389a6d5f5;
  local_28 = 0xba38be3b4c1a4e8c;
  local_20 = 0x30c244b1c9dfbe9;
  local_18 = 0;
  local_78 = 0xc5d0cadf9d95abb8;
  local_70 = 0xd7c9c6c3d7ddcbcb;
  local_68 = 0xc8d2c9cdd6cac3d8;
  local_60 = 0xe1;
  puts(
      "Hello and welcome to my flagcheck challenge!\nEnter the flag to solve this task!\n...How?That is your task to solve! Have fun!"
      );
  pcVar1 = fgets(local_58,0x1a,stdin);
  if (pcVar1 == (char *)0x0) {
    puts("Woops!");
  }
  else {
    flaggy((long)local_58,(long)&local_78,(long)&local_38);
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
..
..
```

Quick interrupt: If using Ghidra, I suggest switching the default button for "cursor text hilight" to left click to easier find multiple uses of the same variable in Ghidras disassembly or decompiled view.


A good tip is to follow the user input and here we see that this is stored into the `local_58` variable. If we follow this variable, we see that this is sent to the `flaggy` function along with two other variables. The two other variables, local_78 and local_38 are actually memory pointers to these variables as they contain values from other variables as well:

&local_78 is actually: local_78 + local_70 + local_68 + local_60
&local_38 is actually: local_38 + local_30 + local_28 + local_20

However, the content of these hex encoded variables does not contain any meaningful ASCII text.
Maybe one of them contain the flag? Let's follow them into the function `flaggy`:

```
void flaggy(long param_1,long param_2,long param_3)

{
  int iVar1;
  uint uVar2;
  long in_FS_OFFSET;
  int local_24;
  int local_20;
  undefined2 local_1b;
  undefined local_19;
  byte abStack24 [8];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  local_1b = 0x4754;
  local_19 = 0;
  if (param_3 != 0) {
    local_24 = 0;
    while (iVar1 = local_24 + 1, local_24 != 0) {
      uVar2 = (uint)(iVar1 >> 0x1f) >> 0x1f;
      abStack24[(long)iVar1] =
           *(byte *)((long)&local_1b + (long)(int)((iVar1 + uVar2 & 1) - uVar2)) ^
           *(byte *)(param_3 + (long)iVar1);
      local_24 = iVar1;
    }
  }
  local_20 = 0;
  while( true ) {
    if ((uint)*(byte *)(param_1 + (long)local_20) + 100 != (uint)*(byte *)(param_2 + (long)local_20)
       ) break;
    local_20 = local_20 + 1;
  }
  if (local_20 == 0x19) {
    printf("Congratz, you found the flag!");
  }
  else {
    printf("Sorry, try harder!");
  } 
..
..
```

Here we see the text "Congratz", which seems to be printed if the input is correct. This condition is hit if `local_20` is 0x19 hex / 25 decimal.
This variable is incremented in the while loop above. It checks if the value of pointer to param_1 + local_20  + 100 decimal is equal to the value of pointer to param_2 + local_20.
To make it clearer, here is a more cleaned up version of the check:

```
  while(true) {
    if ((param_1[i] + 100) != param_2[i]){
        i++;
    } else {
        break;
    }
  } 
```

If we cross check with the input to the parameter, we see that parameter_2 actually is the user input, and parameter_1 is &local_78.
Parameter_3 is just part of code that is not used in the check itself and is included to make the task a bit harder.
This means that we write a small script that takes each hex value of the &local_78 variable minus 100 decimal and print it out:
 
```
flag = "\xb8\xab\x95\x9d\xdf\xca\xd0\xc5\xcb\xcb\xdd\xd7\xc3\xc6\xc9\xd7\xd8\xc3\xca\xd6\xcd\xc9\xd2\xc8\xe1"
out = ''
for c in flag:
    out+=(chr(ord(c)-100))
print(out)
```

We get the flag `TG19{flaggys_best_friend}`, and if we input this into the program, we get the "congratz" message and we can submit the flag :)
