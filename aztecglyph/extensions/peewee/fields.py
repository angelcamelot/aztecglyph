from peewee import CharField
from aztecglyph import AztecGlyph
from playhouse.signals import pre_save
import threading
import time

class AztecGlyphField(CharField):
    description = "Aztec Glyph field"
    content_type_counters = {}
    id_generation_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        super(AztecGlyphField, self).__init__(*args, **kwargs)

    def python_value(self, value):
        if value is None or value == "":
            return value
        return AztecGlyph(value)

    def db_value(self, value):
        if value is None or value == "":
            return value
        return str(value)

    def get_unique_aztec_glyph_id(self, model_class):
        with self.id_generation_lock:
            content_type_id = model_class.__name__
            now = int(time.time() * 1000)
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

@pre_save()
def on_pre_save(sender, instance, created):
    for field in instance._meta.sorted_fields:
        if isinstance(field, AztecGlyphField) and field.primary_key:
            value = getattr(instance, field.name)
            if value == "":
                value = field.get_unique_aztec_glyph_id(instance.__class__)
                setattr(instance, field.name, value)
