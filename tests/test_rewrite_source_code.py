import os
from logging import getLogger

from verbosify.rewrite_source_code import pipeline, rewrite_source_code

snapshot_warning = getLogger('snapshot').warning
SEP = '\n------\n'


def test_pipeline_function():
    snapshot_warning('test')
    for file_name in os.listdir('./tests/input_source_codes'):
        with open(f'./tests/input_source_codes/{file_name}', 'r') as f:
            source_code = f.read()

        if not os.path.isfile(f'./tests/output_expected/{file_name}'):
            snapshot_warning(
                f'Writing {file_name} snapshot because it does not exists yet'
            )
            outputs = None
        else:
            with open(f'./tests/output_expected/{file_name}', 'r') as f:
                data = f.read().split(SEP)
                outputs = dict(zip(data[1::2], data[2::2]))

        sourcelines = source_code.split('\n')

        for func in pipeline:
            func_name = func.__name__
            sourcelines = func(sourcelines)

            if outputs is None:
                with open(f'./tests/output_expected/{file_name}', 'a') as f:
                    f.write(f'{SEP}{func_name}{SEP}')
                    f.write('\n'.join(sourcelines))

            else:
                assert outputs[func_name] == '\n'.join(sourcelines)

        assert rewrite_source_code(source_code) == '\n'.join(sourcelines)
