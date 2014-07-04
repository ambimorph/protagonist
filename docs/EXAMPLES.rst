==========
 Examples
==========

Here are usage examples

.. code::

   $ mkdir test; cd test

Make some trivial files

.. code::

   $ echo hi > hi.txt
   $ echo hello > hello.txt
   $ echo goodbye > goodbye.txt
   $ echo "Happy birthday" > hb.txt
   $ echo amber > amber.txt

Tag them all with the tag "greeting".

.. code::

   $ for f in *; do protag tag $f greetings; done
   $ tree -a

   .
   ├── amber.txt
   ├── goodbye.txt
   ├── hb.txt
   ├── hello.txt
   ├── hi.txt
   └── .protagonist
       ├── tags
       │   └── greetings
       │       ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │       ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
       │       ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │       ├── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
       │       └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       └── truenames
           ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
           ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
           ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
           ├── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
           └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt

Protagonist is now tracking all the tagged files in truenames with unique ids (described in the README -- don't worry, you'll be able to list with human-readable names), and it has a single tag directory for the "greetings" tag.

But "amber.txt" doesn't contain a greeting.   Let's untag that.

.. code::

   $ protag untag amber.txt greetings
   $ tree -a

   .
   ├── amber.txt
   ├── goodbye.txt
   ├── hb.txt
   ├── hello.txt
   ├── hi.txt
   └── .protagonist
       ├── tags
       │   └── greetings
       │       ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │       ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
       │       ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │       └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       └── truenames
           ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
           ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
           ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
           └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt

Now the id corresponding to amber.txt is no longer in the system.
Let's add some more tags.

.. code::

   $ protag tag amber.txt name
   $ protag tag hi.txt enter
   $ protag tag hello.txt enter
   $ protag tag goodbye.txt exit

   $ tree -a
   .
   ├── amber.txt
   ├── goodbye.txt
   ├── hb.txt
   ├── hello.txt
   ├── hi.txt
   └── .protagonist
       ├── tags
       │   ├── enter
       │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   │   └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       │   ├── exit
       │   │   └── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   ├── greetings
       │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   │   ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
       │   │   ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   │   └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       │   └── name
       │       └── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
       └── truenames
           ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
           ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.txt
           ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
           ├── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
           └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt

Now let's try listing.

.. code::

   $ protag ls greetings

   /home/amber/test/hb.txt
   /home/amber/test/hello.txt
   /home/amber/test/goodbye.txt
   /home/amber/test/hi.txt

   $ protag ls name OR exit

   /home/amber/test/goodbye.txt
   /home/amber/test/amber.txt

   $ protag ls greetings AND NOT \( enter OR exit \)

   /home/amber/test/hb.txt

Because truenames indexes the original paths of the files, if a file is renamed with `mv`, we would like Protagonist to reflect that.  So we have `protag mv` wrap the syatem call.
Let's give hb.txt a better name:

.. code::

   $ protag mv hb.txt happy_birthday.rst
   $ tree -a

   .
   ├── amber.txt
   ├── goodbye.txt
   ├── happy_birthday.rst
   ├── hello.txt
   ├── hi.txt
   └── .protagonist
       ├── tags
       │   ├── enter
       │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   │   └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       │   ├── exit
       │   │   └── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   ├── greetings
       │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   │   ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.rst
       │   │   ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   │   └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt
       │   └── name
       │       └── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
       └── truenames
           ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
           ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.rst
           ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
           ├── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
           └── d2f799bb9610968a2efa8f7682d5f2f1d45163d7.txt

   
Similarly, if a file is removed from the filsystem, we want Protagonist to release the hard links, and remove its entry from truenames:

.. code::

   $ protag rm hello.txt 
   $ tree -a
   .
   ├── amber.txt
   ├── goodbye.txt
   ├── happy_birthday.rst
   ├── hi.txt
   └── .protagonist
       ├── tags
       │   ├── enter
       │   │   └── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   ├── exit
       │   │   └── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   ├── greetings
       │   │   ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
       │   │   ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.rst
       │   │   └── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
       │   └── name
       │       └── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt
       └── truenames
           ├── 07b26f762733aefe9456cabd0ec4bd85be19ff3f.txt
           ├── 356cb60775049e5f87a2e580b5eafe531dfa214d.rst
           ├── 875e88d3892f23ec5e90c6d13718edfb3310447e.txt
           └── b55a1b6a6b7cb3fe5d77a9c8f903c054308f4d74.txt


