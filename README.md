## calcurse-load

Personal hooks/scripts for calcurse. This integrates [`calcurse`](https://github.com/lfos/calcurse) with Google Calendar, and [`todo.txt`](http://todotxt.org/).

- pre-load:
  - Looks at the locally indexed Google Calendar JSON dump, adds events as `calcurse` appointments; adds summary/HTML links as appointment notes.
  - Replace `calcurse`s todos with my current [`todo.txt`](http://todotxt.org/), converting priorities accordingly.
- post-save
  - If any new todos are added, write those back to my `todo.txt` file.

This doesn't write back to Google Calendar, its only used to source events.

Should be mentioned that deleting a todo in calcurse does nothing, because the corresponding `todotxt` still exists. Only reason for me to load my todos into `calcurse` is to remind me what they are, and to possibly add new ones. I have [other ways](https://sean.fish/d/todo-prompt?dark) I mark todos as done.

## Setup

```bash
git clone https://github.com/seanbreckenridge/calcurse-load && cd ./calcurse-load
# copy over calcurse hooks
# assuming its not overwriting any hooks, else youd have to manually copy in parts of the scripts
cp ./hooks/* ~/.config/calcurse/hooks/
pip install .  # install current directory with pip
```

This installs 2 python scripts/modules, `gcal_index`, and `calcurse_load`.

`gcal_index` has nothing to do with calcurse inherently, it could be used on its own to export all your current data from Google Calendar.

The data for calcurse is typically kept in `$XDG_DATA_HOME/calcurse` (`$HOME/.local/share/calcurse`). In addition to that, this maintains a data directory in `$XDG_DATA_HOME/calcurse_load`.

---

The `gcal` calcurse hook tries to read any `gcal_index`-created JSON files in the `$XDG_DATA_HOME/calcurse_load/gcal/` directory. If theres description/extra information for events from Google Calendar, this attaches corresponding notes to each calcurse event. Specifically, it:

- Loads the calcurse appointments file
- Removes any Google Calendar events (which are tagged with `[gcal]`)
- Generates Google Calendar events from the JSON
- Adds the newly created events and writes back to the appointments file.

---

The `post-save` `todotxt` hook converts the `calcurse` todos back to `todotxt` todos, and updates the `todotxt` file if any todos were added. A `todo.txt` is searched for in one of the common locations (`~/.config/todo/todo.txt`, `~/.todo/todo.txt` (or specify with the `TODOTXT_FILE` environment variable)).

If you wanted to disable one of the `todotxt` or `gcal` extension, you could remove or rename the corresponding scripts in the `hooks` directory.

### Google Calendar Update Process

`gcal_index` saves an index of Google Calendar events for a Google Account locally as a JSON file.

To setup credentials, see [here](https://google-calendar-simple-api.readthedocs.io/en/latest/getting_started.html).

Put the downloaded credentials in `~/.credentials/`, and specify the location with the `--credential-file`. I'd recommend wrapping in a script, and then setting up a job to run in the background, to update the local JSON index of Google Calendar events.

Its possible to put the command to update the local JSON index in your `pre-load` hook as well, before the call to `python3 -m calcurse_load`, but that would cause some noticeable lag on calcurse start-up.

```
usage: gcal_index [-h] --email EMAIL --credential-file CREDENTIAL_FILE
                  [--end-days END_DAYS]

Export Google Calendar events

optional arguments:
  -h, --help            show this help message and exit
  --end-days END_DAYS   Specify how many days into the future to get
                        events for (if we went forever, repeating
                        events would be there in 2050) [default: 90]

required options:
  --email EMAIL         Google Email to export
  --credential-file CREDENTIAL_FILE
                        Google credential file
```

Prints the JSON dump to STDOUT; example:

`python3 -m gcal_index --email <your_email> --credential-file ~/.credentials/<credential>.json`

For an example script one might put under cron, see [`example_update_google_cal`](./example_update_google_cal)

### Todo.txt Priority Conversion

| Todo.txt | Calcurse |
| -------- | -------- |
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

If you want to use this for other purposes; I defined a `Extension` base class in `calcurse_load.ext.abstract`, you'd just have to add a subclass in a file there, and then add it to the dictionary in `calcurse_load.ext`
