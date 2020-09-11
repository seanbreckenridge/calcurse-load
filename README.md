## calcurse-load

---

# WIP

Currently:

todo.txt extension is done; hooks load properly

[on hold; waiting for [this](https://github.com/kuzmoyev/google-calendar-simple-api/issues/35)]

need to:
  * create `gcal_index`
  * create gcal extension
  * automatically install hooks with setup.py
  * document stuff a bit more

---

Personal hooks/scripts for calcurse. This integrates [`calcurse`](https://github.com/lfos/calcurse) with Google Calendar, and [`todo.txt`](http://todotxt.org/).

* pre-load:
  * Connects to Google Calendar and pulls down any new events. Saves those to an index and adds those events to `calcurse` appointments.
  * Replace `calcurse`s todos with my current [`todo.txt`](http://todotxt.org/), converting priorities accordingly.
* post-save
  * If any new todos are added, write those back to my `todo.txt` file.

This doesn't write back to Google Calendar, its only used to source events.

### Google Calendar Update Process

To setup credentials, see [here](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html).

Put the downloaded credentials in `~/.credentials/google_calendar_credentials.json`, or specify the location with the `--credential-file`.

```
```

You can either:

* setup a job to run in the background, to update the local index of Google Calendar (`gcal_index`)
* run calcurse as normal. The `pre-load` hook will check if the local index has been updated in the last 6 hours. If it hasn't it requests out to Google Calendar.

`gcal_index` saves an index of Google Calendar events locally as an `ics` file, which is then imported into calcurse, with duplicate events removed.

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


### CLI reference

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

