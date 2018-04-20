"""Transform SFrame data into csv -- more human-friendly and universal
"""
import os
import subprocess

import turicreate as tc


def main():
    dirname = os.path.dirname(os.path.realpath(__file__))
    for rootdir, _, _ in os.walk(dirname):
        if not rootdir.endswith('.gl') and not rootdir.endswith('_data'):
            continue
        print('Preparing to transform {}'.format(rootdir))
        try:
            transform_data(rootdir)
        except Exception as err:
            print('Error during transformation: {}'.format(err))
        else:
            print('Done with transforming {}'.format(rootdir))


def transform_data(data_dir):
    data = tc.SFrame(data_dir)
    parent_dir, data_name = os.path.split(data_dir)
    if data_name.endswith('.gl'):
        data_name = data_name[:-3]
    csv_path = os.path.join(parent_dir, data_name)
    data.save(csv_path, format='csv')
    proc = subprocess.Popen(
        'xz {}'.format(csv_path + '.csv'), shell=True, stderr=subprocess.PIPE
    )
    _, stderr = proc.communicate()
    if stderr:
        raise ValueError('Compression error: {}'.format(stderr))
    proc.wait()


if __name__ == '__main__':
    main()
