## calcurse-load

---

# WIP

Currently:

* todo.txt extension is done; hooks load properly
* gcal_index exports google calendar data

need to:
  * create gcal extension to convert JSON into calcurse events
  * document stuff a bit more, how to install

---

Personal hooks/scripts for calcurse. This integrates [`calcurse`](https://github.com/lfos/calcurse) with Google Calendar, and [`todo.txt`](http://todotxt.org/).

* pre-load:
  * Looks at the locally indexed Google Calendar JSON dump, adds events as `calcurse` appointments.
  * Replace `calcurse`s todos with my current [`todo.txt`](http://todotxt.org/), converting priorities accordingly.
* post-save
  * If any new todos are added, write those back to my `todo.txt` file.

This doesn't write back to Google Calendar, its only used to source events.

### Google Calendar Update Process

`gcal_index` saves an index of Google Calendar events locally as a JSON file, which is then imported into calcurse, with duplicate events removed.

To setup credentials, see [here](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html).

Put the downloaded credentials in `~/.credentials/`, or specify the location with the `--credential-file`. I'd recommend wrapping in a script, and then setting up a job to run in the background, to update the local JSON index of Google Calendar events (or just update it before you launch calcurse).

```
usage: gcal_index [-h] --email EMAIL [--credential-file CREDENTIAL_FILE]
                  [--end-days END_DAYS]

Export Google Calendar events

optional arguments:
  -h, --help            show this help message and exit
  --email EMAIL         Google Email to export
  --credential-file CREDENTIAL_FILE
                        Google credential file
  --end-days END_DAYS   Specify how many days into the future to get events
                        for (if we went forever, repeating events would be
                        there in 2050) [default: 90]
```

Prints the JSON dump to STDOUT; example:

`python3 -m gcal_index --email <your_email> --credential-file ~/.credentials/<credential>.json`

For an example script one might put under cron, see [`example_update_google_cal`](./example_update_google_cal)

## Structure

This installs 2 modules, `gcal_index`, and `calcurse_load`.

The data for calcurse is typically kept in `$XDG_DATA_HOME/calcurse` (`$HOME/.local/share/calcurse`). In addition to that, this maintains a data directory in `$XDG_DATA_HOME/calcurse_load`, which is what `gcal` hook reads from.

`gcal_index` has nothing to do with calcurse inherently, it could be used on its own to export all your current data from Google Calendar.

The `post-save` `todotxt` hook converts the `calcurse` todos back to `todotxt` todos, and updates the `todotxt` file if any todos were added. A `todo.txt` is searched for in one of the common locations (`~/.config/todo/todo.txt`, `~/.todo/todo.txt` (or specify with `TODOTXT_FILE`)).

If you wanted to disable one of the `todotxt` or `gcal` extension, you could remove or rename the corresponding scripts in the `hooks` directory.

### Todo.txt Priority Conversion

| Todo.txt | Calcurse |
|----------|----------|
| (A)      | 1 - 3    |
| (B)      | 4 - 6    |
| (C)      | 7 - 9    |
| None     | 0        |


### calcurse_load reference

Probably won't use `calcurse_load` directly except for testing, the `pre-load`/`post-save` hooks automatically call out to the corresponding scripts.

`calcurse_load` accepts either a flag to signify pre/post hook, and an extension name. There are individual [`hooks`](./hooks) for for each extension (`gcal`/`todotxt`)

```
usage: calcurse_load (--pre-load|--post-save) (gcal|todotxt)...

Load extra data into calcurse

optional arguments:
  -h, --help   show this help message and exit

required arguments:
  --pre-load   Execute the preload action for the extension
  --post-save  Execute the postsave action for the extension
```

