# Writeup [Wandshop](README.md)

In this task the user has to modify the parameters sent to the server when adding items to the cart. This can be done using a variety of tools, for example Burp Suite, Fiddler, Tamperdata and so on.

The easiest way to solve the task is the following:
1. Open the webpage in Chrome or Firefox
2. Inspect the Submit-button of the Elder Wand to open a view of the source-code
3. Select the hidden price input field, and change the value to something less than 1337
4. Press the add to cart button
5. Send in the order

When you send the order, the server will reply with a congratulation-message, and the flag!

And then... Whoop whoop, I got the flag!

```
TG19{Elder wand iz best wand}
```
