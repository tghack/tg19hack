# Writeup for [itsmagic](README.md)

As the hints in the task description say, this is a web page with an insecure 
direct object reference. There are other hints as well, but let's start looking
at the task page before discussing the other hints.

When "logging in" to your itsmagic page, you arrive at a page containing a table
with a few classes and the grades for the classes. The login page itself is 
present solely to make it look "real". 

So here are the additional hints:
* There is a userid in the top corner of the grade page.
* There is a number matching the userid in the web page URL.

There is a slight chance that we may change the userid number in the URL, and 
get to see the grades of another user. Lets try it out!

We change the following URL from
```
https://itsmagic.tghack.no/home/1338
```
to
```
https://itsmagic.tghack.no/home/1
```

Now, we set it to userid 1 because the admin user often has that id. However,
nothing special happened. We just got to see the user's grades.

Lets try another thing. Did you know that 1337 is a special number in the 
hacking community? And also in the programming community. In 
[leet speak](https://no.wikipedia.org/wiki/Leet), 1337 means leet. Basically, 
1338 is very close to the l33t number `1337`, so lets try changing the id to 
that number.

```
https://itsmagic.tghack.no/home/1337
```

Aww yeah! There's the flag, `TG19{Direct object reference might B insecure!}`.

Fun fact:
[OWASP Top 10](https://www.owasp.org/index.php/Top_10-2017_Top_10) is a project
where loads of data on web page vulnerabilities are gathered, and they make a
list of the ten most common vulnerabilities. The type of vulnerability we see
in this task, Insecure Direct Object Reference, is one of the vulnerabilities 
in the fifth point at OWASP Top 10 2017, Broken Access Control. In other words,
it is still a very common class of bugs.
