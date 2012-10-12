GFWList2Privoxy
=================

Overview
--------

As we all know, gfwlist contains the sites that blocked by the fucking GFW.
But the rules in gfwlist can't be used in privoxy, so I decided to convert all
these rules so that it can be used by privoxy.

This project is motivated by [AutoProxy2Privoxy](ttps://github.com/cckpg/autoproxy2privoxy).
The author uses BASH script to do the job. I am not good at BASH script, and his/her
script contains some mistakes(mine contains some mistakes also), so I decided to use
python to do the conversion.

The conversion is tedious, and I don't know how to convert some special rules.
These are still some problems in this script, you are all welcomed to fix the
problem if you have time.

How to Use
----------

This script is written in python, so it can be used on most platforms.

First, open GFWList2Privoxy.py, and modify the variable PROXY to your settings.
I am using SSH, so the rule is like below:
	{+forward-override{forward-socks5 127.0.0.1:7070 .}}

Then, issue the following command:
	python GFWList2Privoxy.py

Wait for a few seconds or minutes before the gfwlist.txt is downloaded from the web.

After that, edit `config.txt`, adding this line:

	actionsfile gfwlist.action

Now, privoxy will make use of gfwlist.action to forward your traffic. Enjoy it.

Links
-----

* [autoproxy2privoxy](https://github.com/cckpg/autoproxy2privoxy)
* [AutoProxy Rules](https://autoproxy.org/zh-CN/Rules)
* [Privoxy Patterns](http://www.privoxy.org/user-manual/actions-file.html#AF-PATTERNS)
* [Set Up SSH to Bypass GFW - The Definitive Guide](http://cckpg.blogspot.com/2011/05/set-up-ssh-to-bypass-gfw-definitive.html#privoxy-as-http-proxy)