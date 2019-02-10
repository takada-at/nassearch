import click
from pathlib import Path

from . import search


default_savepath = Path(__file__).parent / '../data'


@click.group()
def cli():
    pass


@click.command()
@click.argument('setting')
@click.option('-o', '--output',
              default=default_savepath)
def save(setting, output):
    output_ = Path(output)
    if not output_.exists():
        output_.mkdir(parents=True)
    search.save(output_ / 'files.csv', Path(str(setting)))


cli.add_command(save)
