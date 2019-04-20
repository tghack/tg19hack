# Writeup [Wand scanner](./README)

**Points: 150**

**Author: maritio_o**

**Difficulty: easy**

**Category: AFK** 

---

In the TG:Hack area, there is a computer running what seems to be a system for 
looking up wands. The table in the middle of the page outputs the wand ID, 
wand name and a description of the wand. Next to the monitor is a barcode 
scanner. Scan a wand's barcode, get the information about it. 

The table is a hint that this system has a database holding the wand data. To 
solve this task, you need to google and read about barcodes. Simply put, a 
barcode is just a machine-readable representation of data made of parallel lines. 
When scanning a barcode, the text from the barcode is inserted to the system. 
It works just like writing input through the keyboard. Except there is no
keyboard attached to the wand scanner system.
If the system does not have input validation (or bad input validation), it is 
an easy task to do an injection.

Knowing that the system is connected to a database, and that the barcode
scanner is a place to input text, we may try to get unintended information out
of the database. 

The first step in this task is to play around with the table.
If you haven't tried doing SQL queries before, we recommend you to read 
about SQL queries. You may do that from 
[this](https://sqlbolt.com/lesson/select_queries_introduction) page for 
instance. 

By looking at the table on the page, we may assume that the columns in the 
database table might have the same names, or similar names. Let's look for 
an ID, name or description having the content `flag`, or try to make the 
webpage output all the entrys in the database. 

It is almost time to start crafting our own barcodes to exploit the system 
with SQL injection. Before doing that, another hint about the system is found
by scanning the barcodes in the wand shop with your phone. This way, you 
understand which columns the system expects to get from the barcode. It seems
like it expects an ID, like this snippet: 
`f9f90ce4-5dfa-11e9-8647-d663bd873d93`.

By trial and failure, and gaining SQL query knowledge, we find that generating 
a barcode with the following text will fetch the flag for you:
```
test' OR '1' = '1'; --
```

The text `test` is just a random text. It is followed by the `OR` operator
which has the equation `'1' = '1'` on its right side. We end the text with
a semicolon (`;`) which ends an SQL query, and two hyphens (`--`) which is the
way to comment out text in SQL. The query on the server side probably looks
something like 

```
SELECT Id, Name, Description
FROM Wands
WHERE Id = {input}
```

... so when we insert our query, it looks like the following snippet:

```
SELECT Id, Name, Description
FROM Wands
WHERE Id = 'test' OR '1' = '1'; --
```

Now, this SQL query selects all the rows in the table because 1 _always_
equals to 1! 

Generate a barcode of the input, scan the barcode and get the flag!

```
TG19{flag_wand_seems_to_be_addictive_madness}
```
