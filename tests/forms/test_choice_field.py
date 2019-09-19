import pytest

from slivka.server.forms.fields import ChoiceField, ValidationError


CHOICES = [
    ('foo', 'FOO'),
    ('bar', 'BAR'),
    ('baz', 'BAZ')
]


@pytest.fixture('module')
def default_field():
    return ChoiceField('name', choices=CHOICES)


# to_python tests

def test_number_to_python(default_field):
    assert default_field.to_python(18) == 18
    assert default_field.to_python(-54) == -54
    assert default_field.to_python(3.1415) == 3.1415


def test_str_to_python(default_field):
    assert default_field.to_python('foobar') == 'foobar'
    assert default_field.to_python('hello world') == 'hello world'


def test_bool_to_python(default_field):
    assert default_field.to_python(False) == False
    assert default_field.to_python(True) == True


def test_none_to_python(default_field):
    assert default_field.to_python(None) is None


def test_empty_to_python(default_field):
    for val in ('', (), {}, set(), []):
        assert default_field.to_python(val) is None


# default value
def test_invalid_default():
    with pytest.raises(Exception):
        ChoiceField('name', choices=CHOICES, default='qux')


# choice validation

def test_text_choices():
    field = ChoiceField('name', choices=CHOICES)
    assert field.validate('BAZ') == 'BAZ'
    assert field.validate('foo') == 'foo'
    assert field.validate('bar') == 'bar'
    with pytest.raises(ValidationError):
        field.validate('quz')


def test_numerical_choices():
    field = ChoiceField('name', choices=[(1, -5), (0.33, 3.1415)])
    assert field.validate(1) == 1
    assert field.validate(0.33) == 0.33
    assert field.validate(3.1415)
    with pytest.raises(ValidationError):
        field.validate(0.34)


# empty value validation

def test_validate_none(default_field):
    with pytest.raises(ValidationError):
        default_field.validate(None)


def test_validate_empty_required():
    field = ChoiceField('name', required=True)
    with pytest.raises(ValidationError):
        field.validate(None)


def test_validate_empty_not_required():
    field = ChoiceField(ValidationError, required=False)
    assert field.validate(None) is None


# validation with default

def test_validate_none_with_default():
    field = ChoiceField('name', choices=CHOICES, default='foo')
    assert field.validate(None) == 'foo'


def test_validate_empty_with_default():
    field = ChoiceField('name', choices=CHOICES, default='FOO')
    assert field.validate(()) == 'FOO'
    assert field.validate([]) == 'FOO'


def test_valid_value_with_default():
    field = ChoiceField('name', choices=CHOICES, default='bar')
    assert field.validate('foo') == 'foo'
    assert field.validate('bar') == 'bar'


def test_invalid_value_with_default():
    field = ChoiceField('name', choices=CHOICES, default='bar')
    with pytest.raises(ValidationError):
        field.validate('QUX')