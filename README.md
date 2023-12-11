### py-abi-compliance-checker

If you maintain packages written in C or C++, chances are you're already familiar with the `abi-compliance-checker` and `abi-dumper` tools.

If you're not, please click the links and read more about them, they're great tools.

There are two modes in which `abi-compliance-checker` may be executed:

1. It may run in a mode that requires binaries/libraries to be compiled including debuginfo.
   This mode is more accurate, and it's easier to use, but it requires debuginfo, so it's not always practical.

2. It may also run in a mode that doesn't require debuginfo.
   This mode is less accurate, but also good, the downside is that it requires specially crafted XML files.

Mode 2 is the mode this tool focuses on.

#### What does this even do?

For now, this tool does the following:

1. Creates the two XML files required for `abi-compliance-checker` to compare two versions of a given package without requiring debuinfo (mode 2).

2. Invokes `abi-compliance-checker` with the correct command line arguments, providing the XML files. Thus, the report is generated.

At some point, it may support better OBS/IBS integration, so it should be able to download the RPM packages, extract them, get their versions, write the XML files and produce the reports.

#### How can I use it?

1. Install `abi-compliance-checker` using `zypper`.

2. Clone this repository, maybe place its scripts in your `$PATH`. Make sure they're executable. `extract-rpm` is a tiny, convenient Bash script that extracts RPMs.

3. Download the RPMs you want to compare, move them to their dedicated directory, and extract them. For this example, we'd be comparing a fictional package `libfoo` from `openSUSE:Factory` to an older version on IBS:

   `osc getbinaries openSUSE:Factory libfoo`
   `mv binaries libfoo-1.10`
   `cd libfoo-1.10`
   `extract-rpm *.rpm`
   `cd ..`

   `isc getbinaries SUSE:Factory:head libfoo`
   `mv binaries libfoo-1.3`
   `cd libfoo-1.3`
   `extract-rpm *.rpm`
   `cd ..`

4. We should now have two directories: `libfoo-1.10` and `libfoo-1.3`, with those packages' contents.

5. Now you can finally use this tool :D

   The syntax is:
   `py-abi-compliance-checker <package name> <old version> <old version directory> <new version> <new version directory>`.

   So we could do:
   `py-abi-compliance-checker libfoo 1.3 libfoo-1.3 1.10 libfoo-1.10`.

   And the report should be generated inside the `compat_reports` directory.
   The XML files in this case will be named `1.3.xml` and `1.10.xml`, if you feel like checking them out.
