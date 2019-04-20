#include <stdio.h>
#include <linux/kvm.h>
#include <sys/ioctl.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <inttypes.h>
#include <memory.h>
#include "bank.h"

#define DEBUG

#ifdef DEBUG
#define DPRINT(args...) fprintf(stderr,"%10s:%-3d - ", __FILE__, __LINE__); fprintf(stderr, args);
#else
#define DPRINT(args...)
#endif

static void check_kvm_version(int kvmfd) {
    int ret = ioctl(kvmfd, KVM_GET_API_VERSION, NULL);

    if (ret == -1) {
        perror("ioctl");
        exit(-1);
    }

    if (ret != 12) {
        fprintf(stderr, "KVM_GET_API_VERSION %d expected 12\n", ret);
        exit(-1);
    }

    DPRINT("KVM version check: %d\n", ret);
}

static void check_kvm_extension(int kvmfd, int extension) {
    int ret = ioctl(kvmfd, KVM_CHECK_EXTENSION, extension);
    if (ret == -1) {
        perror("ioctl check_extension");
        exit(-1);
    }

    if (!ret) {
        fprintf(stderr, "Missing critical extension %d\n", extension);
        exit(-1);
    }
}

static void* vmstack;

void print_regs(int vcpufd) {
    struct kvm_sregs sregs;
    struct kvm_regs regs;
    ioctl(vcpufd, KVM_GET_SREGS, &sregs);
    ioctl(vcpufd, KVM_GET_REGS, &regs);

		uint32_t* stackptr = (uint32_t*)(((uint8_t*)vmstack)+(regs.rsp-0xF000));

    fprintf(stderr, "CS=%llx, DS=%llx, SS=%llx, ES=%llx\n",
            sregs.cs.base, sregs.ds.base, sregs.ss.base, sregs.es.base);
    fprintf(stderr, "AX=%llx CX=%llx DX=%llx SI=%llx IP=%llx SP=%llx\n",
            regs.rax, regs.rcx, regs.rdx, regs.rsi, regs.rip, regs.rsp);
		fprintf(stderr, "Stack: [%x, %x, %x, %x, %x, %x, %x, %x,]\n", 
stackptr[0], stackptr[1], stackptr[2], stackptr[3], stackptr[4], stackptr[5], stackptr[6], stackptr[7]);
	fprintf(stderr, "PrevStack: [%x, %x, %x, %x]\n", *(stackptr-1), *(stackptr-2), *(stackptr-3), *(stackptr-4));
	
		uint32_t rip = regs.rip;
		if(rip > 0xFF00 && rip < 0xFFFF) {
			uint8_t *rips = (uint8_t*)(((uint8_t*)vmstack)+(regs.rip-0xF000));
			fprintf(stderr, "INSTRS: [%02x%02x%02x%02x]\n", rips[0], rips[1], rips[2], rips[3]);
		}
}



static void setup_stack(int vmfd) {
    void *vmpage = mmap(NULL, 0x2000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    struct kvm_userspace_memory_region region = {
            .slot = 1,
            .guest_phys_addr = 0xF000,
            .memory_size = 0x1000,
            .userspace_addr = (uint64_t) vmpage
    };
    ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region);
		vmstack = vmpage;
}

static void setup_secure_data(int vmfd) {
	char buf[100];
	FILE* flag = fopen("./flag.txt", "r");
    if(!flag) {
        fprintf(stderr, "Could not open flag.txt!\n");
        exit(-1);
    }
	fgets(buf, 100, flag);
	fclose(flag);

	void *vmpage = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
	memset(vmpage, 0, 0x1000);
	memcpy(vmpage, buf, strlen(buf));
	struct kvm_userspace_memory_region region = {
            .slot = 2,
            .guest_phys_addr = 0xEE000,
            .memory_size = 0x1000,
            .userspace_addr = (uint64_t) vmpage
    };
    ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region);
}

static void trigger_singlestep(int vcpu) {
	fprintf(stderr, "Triggering singlestep\n");
	struct kvm_guest_debug dbg = {
		.control = KVM_GUESTDBG_ENABLE | KVM_GUESTDBG_SINGLESTEP
	};
	int ret = ioctl(vcpu, KVM_SET_GUEST_DEBUG, &dbg);
	if(ret != 0) {
		perror("singlestep");
	}
}

int main() {
    int kvm = open("/dev/kvm", O_RDWR | O_CLOEXEC);

    if (kvm == -1) {
        perror("open /dev/kvm");
    }

    check_kvm_version(kvm);
    check_kvm_extension(kvm, KVM_CAP_USER_MEMORY);

    int vmfd = ioctl(kvm, KVM_CREATE_VM, (unsigned long) 0);
    if (vmfd == -1) {
        perror("ioctl");
        exit(-1);
    }

    void *vmpage = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    memcpy(vmpage, bank, bank_len);

    struct kvm_userspace_memory_region region = {
            .slot = 0,
            .guest_phys_addr = 0x1000,
            .memory_size = 0x1000,
            .userspace_addr = (uint64_t) vmpage
    };

    ioctl(vmfd, KVM_SET_USER_MEMORY_REGION, &region);
    setup_stack(vmfd);
	setup_secure_data(vmfd);

    int vcpufd = ioctl(vmfd, KVM_CREATE_VCPU, (unsigned long) 0);
    int mmap_size = ioctl(kvm, KVM_GET_VCPU_MMAP_SIZE, NULL);
    struct kvm_run *run = mmap(NULL, (size_t) mmap_size, PROT_READ | PROT_WRITE, MAP_SHARED, vcpufd, 0);
    if (run == MAP_FAILED) {
        perror("mmap");
        exit(-1);
    }

    struct kvm_sregs sregs;
    ioctl(vcpufd, KVM_GET_SREGS, &sregs);
    sregs.cs.base = 0;
    sregs.cs.selector = 0;
    ioctl(vcpufd, KVM_SET_SREGS, &sregs);

    struct kvm_regs regs = {
            .rip = 0x1000,
            .rax = 2,
            .rbx = 2,
            .rflags = 0x2
    };

    ioctl(vcpufd, KVM_SET_REGS, &regs);

    char recvd[100];
    recvd[0] = 0;
    char tmp[2];
    tmp[1] = 0;
	int tmpchar;
	int shiftcnt = 0;

    while (1) {
        ioctl(vcpufd, KVM_RUN, NULL);
        //fprintf(stderr, "\n\n----EXIT----\nExit-reason=%d\n", run->exit_reason);
        //print_regs(vcpufd);
        switch (run->exit_reason) {
            case KVM_EXIT_HLT:
                fprintf(stderr, "KVM_EXIT_HLT\n");
                return 0;
            case KVM_EXIT_IO:
				if(run->io.size != 1 || run->io.port != 0x3f8 || run->io.count != 1)
					break;
                if (run->io.direction == KVM_EXIT_IO_OUT) {
                    tmp[0] = *(((char *) run) + run->io.data_offset);
					printf("%c", tmp[0]);
					fflush(stdout);
				} else if(run->io.direction == KVM_EXIT_IO_IN) {
					tmpchar = getchar();
					if(tmpchar == EOF) { fprintf(stderr, "Got EOF, exiting\n"); exit(-1); }
					memcpy(((uint8_t*)run)+run->io.data_offset, (char*)&tmpchar, 1);
                } else
                    fprintf(stderr, "unhandled KVM_EXIT_IO\n");
                break;
            case KVM_EXIT_FAIL_ENTRY:
                fprintf(stderr, "KVM_EXIT_FAIL_ENTRY: hardware_entry_failure_reason = 0x%llx\n",
                        (unsigned long long) run->fail_entry.hardware_entry_failure_reason);
								exit(-1);
            case KVM_EXIT_INTERNAL_ERROR:
                fprintf(stderr, "KVM_EXIT_INTERNAL_ERROR: suberror = 0x%x\n",
                        run->internal.suberror);
                exit(-1);
            case KVM_EXIT_MMIO:
                fprintf(stderr, "MMIO-exit phys_addr=%llx, is_write=%d, data=%p, len=%d\n",
                        run->mmio.phys_addr,
                        run->mmio.is_write,
                        (void *) run->mmio.data,
                        run->mmio.len);
				exit(-1);
			case KVM_EXIT_DEBUG:
				fprintf(stderr, "Debug\n");
				trigger_singlestep(vcpufd);
				break;
        }
    }

    return 0;
}
