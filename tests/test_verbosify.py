from logging import getLogger
from unittest.mock import call, patch

import pytest

from verbosify import verbosify, verbosify_with


@patch('builtins.print')
def test_verbosify(mocked_print):
    @verbosify
    def hello_word(uppercase=False):
        if uppercase:
            # verbose: return hello word in uppercase
            return 'HELLO WORD'
        # this commentary should not be printed
        else:
            # verbose: return hello word in lowercase
            return 'hello word'

    assert hello_word(verbose=True) == 'hello word'
    assert hello_word(uppercase=True, verbose=True) == 'HELLO WORD'
    assert hello_word() == 'hello word'
    assert hello_word(uppercase=True) == 'HELLO WORD'

    assert mocked_print.mock_calls == [
        call('return hello word in lowercase'),
        call('return hello word in uppercase'),
    ]


@patch('builtins.print')
def test_verbosify_with(mocked_print):
    @verbosify_with(' ')
    def hello_word(uppercase=False):
        # This is the hello_word function
        if uppercase:
            # verbose: return hello word in uppercase
            return 'HELLO WORD'
        else:
            # verbose: return hello word in lowercase
            return 'hello word'

    assert hello_word(verbose=True) == 'hello word'
    assert hello_word(uppercase=True, verbose=True) == 'HELLO WORD'
    assert hello_word() == 'hello word'
    assert hello_word(uppercase=True) == 'HELLO WORD'

    assert mocked_print.mock_calls == [
        call('This is the hello_word function'),
        call('verbose: return hello word in lowercase'),
        call('This is the hello_word function'),
        call('verbose: return hello word in uppercase'),
    ]


def test_verbosify_not_a_func():
    with pytest.raises(TypeError) as execinfo:
        verbosify(1)
    assert str(execinfo.value) == 'verbosify can only be applied to a function'


@patch.object(getLogger('verbosify'), 'warning')
@patch('builtins.exec')
def test_verbosify_exec_fail(mock_exec, mock_warning):
    mock_exec.side_effect = Exception('Boom!')

    @verbosify
    def hello_word(uppercase=False):
        if uppercase:
            # verbose: return hello word in uppercase
            return 'HELLO WORD'
        # this commentary should not be printed
        else:
            # verbose: return hello word in lowercase
            return 'hello word'

    mock_warning.assert_called_with(
        """
The following error has occurred wile verbosifying 'hello_word' function:
>>> Boom!
The function was return unverbosified.
"""
    )

    assert hello_word() == 'hello word'
    assert hello_word(uppercase=True) == 'HELLO WORD'

    with pytest.raises(TypeError) as execinfo:
        hello_word(verbose=True)
    assert (
        str(execinfo.value)
        == "hello_word() got an unexpected keyword argument 'verbose'"
    )
