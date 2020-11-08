---
layout: post
title: RtlWriteDecodedUcsDataIntoSmartLBlobUcsWritingContext and Other Long Function Names
date: 2010-02-27 07:21:27 +05:30
categories: humor
description: This post records some unusually names of functions exported by "system" DLLs in the Windows directory
keywords: humor, Microsoft, Windows, programming, naming, API, long function names, MSDN
---

I find long functions names charming -- I think they impart a certain personality to the API and add to the _fun_ of programming. And while I try to avoid excessively long names in my own code at work (unless they add to clarity), I never fail to get a good kick seeing such names used by other programmers!

> Every reader should ask himself periodically "Toward what end, toward what end?" -- but do not ask it too often lest you pass up the fun of programming for the constipation of bittersweet philosophy.
-- Alan J. Perlis [foreword to SICP](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-5.html)

I've often wondered what the longest names would look like. So I decided to explore a large system -- the system DLLs in `C:\Windows` directory -- and dig up some of the biggies. My plan was to write a script that walked through the installed DLLs and looked at their exported functions list for interesting candidates.

### The Winners
Here are the longer ones I could find:

* RtlWriteDecodedUcsDataIntoSmartLBlobUcsWritingContext [wcp.dll], with 53-characters, was the longest one (but this function is not documented)
* (52) _[ConvertSecurityDescriptorToStringSecurityDescriptor{A,W} [advapi32.dll]](http://msdn.microsoft.com/en-us/library/aa376397%28VS.85%29.aspx)_, the function that  [Raymond Chen](http://en.wikipedia.org/wiki/Raymond_Chen)  admitted was the reason for  [his post on security descriptors](http://blogs.msdn.com/oldnewthing/archive/2004/03/12/88572.aspx) .
* (52) _[ConvertStringSecurityDescriptorToSecurityDescriptor{A,W} [advapi32.dll]](http://msdn.microsoft.com/en-us/library/aa376397%28VS.85%29.aspx)_, the complement of the above.
* (50) _[CreatePrivateObjectSecurityWithMultipleInheritance [advapi32.dll]](http://msdn.microsoft.com/en-us/library/aa446582%28VS.85%29.aspx)_, another security function.
* (50) _[CertCreateCTLEntryFromCertificateContextProperties [crypt32.dll]](http://msdn.microsoft.com/en-us/library/aa376038%28VS.85%29.aspx)_.
* (50) _[EapHostPeerQueryUIBlobFromInteractiveUIInputFields [eappcfg.dll]](http://msdn.microsoft.com/en-us/library/bb204685%28VS.85%29.aspx)_.
* (49) _[AccessCheckByTypeResultListAndAuditAlarmByHandle{A,W} [advapi32.dll]](http://msdn.microsoft.com/en-us/library/aa374843%28VS.85%29.aspx)_, yet another security API -- I guess the security API programmers get a good kick from long names, just like me!
* (47) _[GetNumberOfPhysicalMonitorsFromIDirect3DDevice9 [Dxva2.lib]](http://msdn.microsoft.com/en-us/library/dd692949%28VS.85%29.aspx)_.
* (43) _[SetupRemoveInstallSectionFromDiskSpaceList{A,W} [Setupapi.dll]](http://msdn.microsoft.com/en-us/library/aa377432%28VS.85%29.aspx)_.
And just so that no one thinks I’m making these up, I’ve linked to their documentation!

Curious on seeing these names, I dug through the other “operating system” I had access to — GNU EMACS. The longest interactive command there is `slime-compiler-notes-default-action-or-show-details/mouse`: Counting punctuations, this beats the longest Windows export by 4 characters.

### The Method
I used the [pefile Python library](http://code.google.com/p/pefile/)  to parse all DLLs in my windows directory. I only considered “system” DLLs (ignoring any third-party drivers etc.) by checking for “Microsoft” in the DLL copyright-string. In addition, I discarded any C++-ish exports, because the  [C++ name-mangling](http://en.wikipedia.org/wiki/Name_mangling)  skewed the results too much and I was too lazy to hook in a “undecoratify” procedure.

Finally, on my 64-bit windows installation, there are both 32-bit and 64-bit versions of many core DLLs (in System32 and SysWOW64 directories respectively), and I encountered duplicates. A similar thing happened with [SxS](http://msdn.microsoft.com/en-us/library/aa376307%28VS.85%29.aspx) DLLs.

Using [this Python script I coded](https://gist.github.com/230c3f53261a20340118), I generated a delimitered text-file with around 1500 entries that I manually scanned (I had some time to waste!) for “interesting” names. Below is a histogram of the function-name lengths. The rough bell shape gives me confidence that script wasn’t totally off the mark.

{% include postimg.html url="funcnames/histogram_large.png" desc="Histogram of function name lengths" %}

### Functions Taking Lots of Parameters

A second axis to dig “interesting” functions would be to count the _number of function params_.

This one is a bit of fuzzy due to questions like “Do you count /deep/“? That is, when a function accepts a pointer to a struct, do you count the struct members as inputs too? For instance, _[CreateFontIndirectEx [gdi32.dll]](http://msdn.microsoft.com/en-us/library/dd183501%28VS.85%29.aspx)_ takes a pointer to [ENUMLOGFONTEXDV](http://msdn.microsoft.com/en-us/library/dd162628%28VS.85%29.aspx) structure that holds about two dozen items (all things considered).

Counting params is also more work, at least for DLL exports (where you need to cross-reference with documentation/headers if the export is, at all, public). Otherwise, the problem can be approached differently by forgetting DLL exports entirely and instead using a crawler that walks the the locally installed MSDN and parses the "Syntax" section to count the number of params — just assuming num_params = num_commas + 1 might be good enough.

Anyway, manually browsing through some of MSDN, I chanced upon a few gems:

*  [AccessCheckByTypeResultListAndAuditAlarmByHandle](http://msdn.microsoft.com/en-us/library/aa374843%28VS.85%29.aspx), our friend from above, true to its character, takes 17 parameters!
*  [OleCreateFromFileEx](http://msdn.microsoft.com/en-us/library/ms690529%28VS.85%29.aspx)  takes in a filename, interface ID, flags, sink, connection, site, ... 13 in all.

### On a Serious Note

Well named functions (just like well named variables) are good instant documentation. _Descriptive_ function are important when:

* Such functions all belong to a flat namespace (DLL exports or C code)
* Several of them have very similar purpose (like the six or so AccessCheck* APIs)
Such names become even more relevant when they define the public API of your library/system.

Some people (“constipated by bittersweet philosophy”?) dislike long function names, and I wonder why. The argument that longer functions take longer to type seems mostly dud: Visual Studio with the awesome [Visual Assist X](http://www.wholetomato.com/)  addon does Intellisense beautifully; Emacs with [hippie-expand](http://www.emacswiki.org/emacs/HippieExpand) does some good magic. So typing isn’t a problem.

### Links
While researching for this entry, I came across the [Brad Abrams's "Best" method names ever](https://docs.microsoft.com/en-us/archive/blogs/brada/best-method-names-ever) that has some interesting ones.

