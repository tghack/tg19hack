asm (".code16gcc\n"
     "movw $0x0000, %ax\n"
     "movw %ax, %ss\n"
     "movw $0xFFFF,%sp\n"
     "call  _start\n"
     "hlt\n");

void print(char* arg) {
	static const short port = 0x3f8;
	while(*arg != 0) {
		asm volatile("outb %0, %1\n" 
                 : : "a"(*arg), "d"(port));	
		arg++;
	}
}

void read_line(char* buf) {
	static const short port = 0x3f8;	
	char inp;
	do {
		asm volatile("inb %1, %0" : "=a"(inp) : "d"(port));
		*buf = inp;
	} while(*(buf++) != '\n');

	buf -= 1;
	*buf = 0;
}

int strcmp(char* buf, char* cmp) {
	while(*buf) {
		if(*buf != *cmp) {
			break;
		}
		buf++;
		cmp++;
	}

	return *buf - *cmp;
}

int atoi(char* buf) {
	int val = 0;
	while(*buf) {
		val *= 10;
		int tmpval = *buf - '0';
		if(tmpval < 0 || tmpval > 9) {
			return -1;
		}
		val += tmpval;
		buf++;
	}

	return val;
}

int get_account_no() {
	char acnt[16];
	print("Enter account no: ");
	read_line(acnt);
	int accn = atoi(acnt);
	return accn;
}

void handle_cmd(char* buf) {
	if(strcmp(buf, "help") == 0) {
		print("COMMAND LIST: \n");
		print("- help: lists all available commands\n");
		print("- status: system status\n");
		print("- balance: check account balance\n");
	} else if(strcmp(buf, "status") == 0) {
		print("System status: OK\n");
	} else if(strcmp(buf, "balance") == 0) {
		int acnt = get_account_no();
		if(acnt == 1337) {
			print("Balance: 1337\n");
		} else {
			print("Account not found\n");
		}
	} else {
		print("Unrecognized command '");
		print(buf);
		print("' try 'help'\n");
	}
}

char asciiart[] = ""
" ######   ########  #### ##    ##  ######    #######  ######## ########  ###### \n"
"##    ##  ##     ##  ##  ###   ## ##    ##  ##     ##    ##       ##    ##    ##\n"
"##        ##     ##  ##  ####  ## ##        ##     ##    ##       ##    ##      \n"
"##   #### ########   ##  ## ## ## ##   #### ##     ##    ##       ##     ###### \n"
"##    ##  ##   ##    ##  ##  #### ##    ##  ##     ##    ##       ##          ##\n"
"##    ##  ##    ##   ##  ##   ### ##    ##  ##     ##    ##       ##    ##    ##\n"
" ######   ##     ## #### ##    ##  ######    #######     ##       ##     ###### \n";


void _start() {
	char buf[64];
	print(asciiart);
	print("Central bank mainframe system v1.3.3.7\n");
	while(1) {
		print("CMD> ");
		read_line(buf);
		handle_cmd(buf);
	}
}

