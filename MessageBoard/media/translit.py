import unicodedata2
import pytils
from django.core.files.storage import FileSystemStorage

class Translit(FileSystemStorage):
    def get_valid_name(self, name):
        name_parts = name.split('.')
        name = unicodedata2.normalize('NFKD', pytils.translit.slugify(name_parts[0])).encode('ascii', 'ignore').decode('utf-8')
        name = '{}.{}'.format(name, name_parts[-1])
        return super(Translit, self).get_valid_name(name)
    