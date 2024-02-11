# NOI.PH editorials repo

Please visit https://noi.ph/


# How to upload editorials

Suppose your editorials are in `../path/to/repo-name/2023/my-contest/editorials`. Note that it is important for the last three parts of the path to be `[year]/[contestname]/editorials`.[^1] Here's what you do to upload:

1. Copy and compile everything.

    ```bash
    $ cd editorials
    $ ./copyall.py ../path/to/repo-name 2023 my-contest
    $ ./compileall.py
    ```

    Note that "`editorials`" is gone in the `copyall` command, and there's a space between `repo-name` and `2023`.

    If all goes well, you should see your files in the appropriate folder in this repo, along with .html files for every .md file.

2. You then git add, git commit then git push everything. (**Including** the .html files.)

3. After that, wait for Github Pages to finish building and deploying. You can see the status at https://github.com/noi-ph/editorials . You can see a status icon at the right of the commit message at the top.

Note that the scripts require `python3.10`; if you have an earlier version of Python, I think they should still work. Anyway, if the command above doesn't work, just run `python3 copyall.py` and `python3 compileall.py` directly instead.



# TODOs

- add favicon



[^1]: `[year]/editorials/[contestname]` is also OK.
