# Writeup [Fortune cookie](./README.md)

There are a few hints for this task:

* Task title is called "Fortune _cookie_"
* The second paragraph says you are going to learn about "fortune _cookies_"

Experienced CTFers will recognize this task at once. They will quite quickly, 
probably just by reading the task title, understand that they should take a
look at the browser cookie. There are many ways of checking the browser cookie:

1. Inspect the web page, and write `document.cookie` into the console.
2. Inspect the web page, go to the `Application` tab, and look under `Storage`.
3. Inspect the web page, go to the `Network` tab, refresh the page to get 
incoming and outgoing traffic. Check out the cookie header in the calls.
4. Download a cookie extension.
5. Probably many more!

When finding the cookie on the page, we see that a part of the cookie says
`divination:student`. Tokens are commonly used to give access on web pages. 

Divination is according to [Harry Potter fandom](https://harrypotter.fandom.com/wiki/Divination) 
as following:

_"Divination is a branch of magic[1] that involves attempting to foresee the 
future, or gather insights into past, present and future events, through 
various rituals and tools."_

As the cookie contains `student`, and we know that `professor` is superior to 
student at a school, we may try changing from `student` to `professor`. Try
refreshing the page. This is also written in the hint.

Aaaand... Flag is `TG19{what_a_fortune_my_lucky_one}`!

The lesson here is to be aware of the information you put in the cookies 
or any of the headers!
