![AztecGlyph](AztecGlyph.png)
# Aztec Glyph

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aztecglyph)
![PyPI](https://img.shields.io/pypi/v/aztecglyph)
![License](https://img.shields.io/github/license/angelcamelot/aztecglyph)

## Contents

- [Introduction and Features](#introduction-and-features)
- [Requirements and Installation](#requirements-and-installation)
- [Usage and Examples](#usage-and-examples)
- [Attributes and Methods](#attributes-and-methods)
- [AztecGlyphField - Django Extension](#aztecglyphfield---django-extension)
- [Contributing and Collaboration](#contributing-and-collaboration)
- [License and Credits](#license-and-credits)

## Introduction and Features
The Python AztecGlyph package is a useful tool for generating unique and secure IDs and keys in the form of 64-bit UUIDs. The AztecGlyph class represents UUIDs that are immutable, hashable, and can be used as dictionary keys. Converting an AztecGlyph object to a string using str() yields a base58-encoded string (URL-safe) that is 11 characters long.

The AztecGlyph class constructor accepts four possible forms of arguments: a string (base58 encoded), a bytes object, an integer, a hexadecimal string, or the values for counter, content type, and timestamp.



The AztecGlyph UUID is divided into three parts: timestamp (41 bits), counter (11 bits), and content type (12 bits).

| Property     | Bits | Min           | Max                  | description                                                                                                                      |
|--------------|------|---------------|----------------------|----------------------------------------------------------------------------------------------------------------------------------|
| Timestamp    | 41   | 1577836800000 | 3776860055551        | The timestamp is the number of milliseconds elapsed since January 1, 2020.                                                       |
| Counter      | 11   | 0             | 2047                 | The counter is a number incremented each time a new AztecGlyph is created and reset to 0 each time the timestamp is incremented. |
| Content Type | 12   | 0             | 4095                 | The content type is used to identify the type of data stored in the AztecGlyph.                                                  |

## Requirements and Installation

To use this package, you should have Python 3.x installed. You can install the package using pip:

 ```bash
 pip install aztecglyph
 ```

## Usage and Examples

```python
from aztecglyph import AztecGlyph

# Create a new AztecGlyph from a base58-encoded string (11111111111 to jpXCZedGfVQ)
glyph1 = AztecGlyph(s=base58_string)

# Create a new AztecGlyph from a bytes object
# (b'\x00\x00\x00\x00\x00\x00\x00\x00' to b'\xff\xff\xff\xff\xff\xff\xff\xff')
glyph2 = AztecGlyph(b=byte_object)

# Create a new AztecGlyph from an integer (0 to 18446744073709551615)
glyph3 = AztecGlyph(i=integer_value)

# Create a new AztecGlyph from a hexadecimal string
glyph4 = AztecGlyph(h=hex_string)

# Create a new AztecGlyph with specific counter, content type, and timestamp values
glyph5 = AztecGlyph(counter=counter_value, content_type=content_type_value, now=timestamp_value)
```

## Attributes and Methods

The AztecGlyph class objects have several read-only attributes and methods:

| Name                 | Return Type | Description          |
|----------------------|-------------|----------------------|
| `glyph.content_type` | int         | Content Type ID      |
| `glyph.str`          | str         | String 11 characters |
| `glyph.int`          | int         | Integer              |
| `glyph.bytes`        | bytes       | Bytes object         |
| `glyph.hex`          | str         | Hexadecimal string   |
| `glyph.timestamp`    | datetime    | Timestamp            |
| `glyph.datetime`     | datetime    | Datetime             |
| `glyph.counter`      | int         | Counter              |

### Comparing AztecGlyph Objects

`AztecGlyph` objects can be compared using standard comparison operators such as==, <, <=, >, and >=`. For example:

```python
# Equality check
if glyph1 == glyph2:
    print("glyph1 is equal to glyph2")

# Less than check
if glyph1 < glyph2:
    print("glyph1 is less than glyph2")

# Greater than or equal to check
if glyph1 >= glyph2:
    print("glyph1 is greater than or equal to glyph2")
```

## AztecGlyphField - Django Extension

AztecGlyphField is a Django extension that enables seamless integration of the AztecGlyph library with Django models for generating unique and reliable 64-bit identifiers.

### Features and Usage

- Inherits from Django's Field class for easy integration with Django models.
- Generates a unique AztecGlyph UUID for each new model instance.
- Automatically detects ContentType.
- Automatically detects the current timestamp and resets the counter if the timestamp changes.
- One Counter per ContentType per Timestamp.
- Requires Python 3.8 or higher, Django 2.2 or higher, and AztecGlyph 1.0.0 or higher.

To use AztecGlyphField, include it in your models.py file:

```python
from aztecglyph.extensions.django import AztecGlyphField
from django.db import models

class MyModel(models.Model):
   id = AztecGlyphField(primary_key=True)
```

Then, use it like any other Django model field:

```python
my_object = MyModel()
my_object.save()
print(my_object.id)  # Output: 326ZtZ1QLEJ
```

## Contributing and Collaboration

Contributions to the AztecGlyph project are always welcome! If you're interested in contributing, please read the [Contributing](CONTRIBUTING.md) file for guidelines and best practices. Feel free to submit issues and pull requests, or join the discussion on the project's GitHub page.

## License and Credits

This project is licensed under the [MIT License](LICENSE). The AztecGlyph was created by [AngelCamelot](https://github.com/angelcamelot).