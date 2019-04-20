# Magical Glyphs Writeup

In the picture we're given, it looks like there's a bunch of weird characters
that we have to decode to get the flag. The shape might be familiar if you've
seen a lot of avatars on Github. If you google for "Github avatars", you'll find
[this article](https://github.blog/2013-08-14-identicons/), which tells us that
these avatars are actually called identicons. Here's a description from the blog
post:

```
Our Identicons are simple 5×5 "pixel" sprites that are generated using a hash
of the user’s ID. The algorithm walks through the hash and turns pixels on or
off depending on even or odd values.
```

Since the identicons on the picture are spaced out evenly, we can probably
assume that they represent single characters. Thus, we can try to generate
identicons for every single character, and then match them up with the
identicons in the flag picture.

First, we need a tool that can convert an md5 hash of a letter to identicon. By googling, we
find the following tool on github: https://github.com/dgraham/identicon.

We can use it to create a pictures of all the letters in the alphabet, for
example by patching the Rust program:

```rust
fn gen_alphabet() {
    // printable ascii characters
    for c in 32u8..127 {
        let s = (c as char).to_string();
        let digest = Md5::digest_str(&s);
        let mut bytes = [0; 16];
        bytes.copy_from_slice(&digest);

        print_hex(&bytes);
        let filename = format!("{}.png", c);
        println!("filename: {}", filename);

        match generate_png_file(&bytes, &filename) {
            Ok(_) => (),
            Err(e) => {
                println!("error! {}", e);
                exit(1);
            }
         }
     }
 }
```

You could also use a simple for-loop in Python/bash etc. After running the loop,
every letters has a corresponding file that is named after the decimal ascii
value of that character. A, for example, has the decimal value 65, so 65.png is
the identicon for A. We know that the flag probably starts with `TG19{`, so
let's put together a picture containing these letters as identicons.

![](./src/tg19.png)

It's a match! Now, all that's left is to do this for the remaining characters.
We can speed up the process by looking for characters that appear often in
flags, like `_`. Also, after figuring out the first word, we see that all of
the letters are lower case.

In the end, we find the flag: `TG19{all_these_beautiful_pictures_make_me_happy}`
