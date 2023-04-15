from django.db import models
from aztecglyph import AztecGlyph
from django.contrib.contenttypes.models import ContentType
import threading
import time

class AztecGlyphField(models.Field):
    description = "Aztec Glyph field"
    content_type_counters = {}
    id_generation_lock = threading.Lock()
    content_type_cache = {}
    last_time = 0

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        super(AztecGlyphField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return "char(11)"

    def from_db_value(self, value, expression, connection):
        if value is None or value == "":
            return value
        return AztecGlyph(value)

    def to_python(self, value):
        if isinstance(value, AztecGlyph):
            return value
        if value is None or value == "":
            return value
        return AztecGlyph(value)

    def get_prep_value(self, value):
        return str(value)

    def get_unique_aztec_glyph_id(self, model_class):
        with self.id_generation_lock:
            if model_class not in self.content_type_cache:
                self.content_type_cache[model_class] = ContentType.objects.get_for_model(model_class)
            content_type_id = self.content_type_cache[model_class].id
            now = int(time.time() * 1000)

            if self.last_time != now:
                self.content_type_counters = {}

            self.last_time = now

            if content_type_id not in self.content_type_counters:
                self.content_type_counters[content_type_id] = {"timestamp": now, "counter": 0}
            else:
                if now > self.content_type_counters[content_type_id]["timestamp"]:
                    self.content_type_counters[content_type_id]["timestamp"] = now
                    self.content_type_counters[content_type_id]["counter"] = 0
                else:
                    self.content_type_counters[content_type_id]["counter"] += 1

            unique_id = AztecGlyph(
                counter=self.content_type_counters[content_type_id]["counter"],
                content_type=content_type_id,
                now=now
            )
        return unique_id

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if self.primary_key and value == "":
            value = self.get_unique_aztec_glyph_id(model_instance.__class__)
            setattr(model_instance, self.attname, value)
        return value
