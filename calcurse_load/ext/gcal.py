import warnings

from .abstract import Extension

# loads any JSON files in ~/.local/data/calcurse_load/*.json,
# extracts event data from them and removes duplicates
class gcal_ext(Extension):

    def pre_load(self):
        print("running gcal pre-load hook...")

    def post_save(self):
        warnings.warn("gcal doesn't have a post-save hook!")
