import click
from pathlib import Path
import psycopg2
import os
from subprocess import run as subrun
import sys


@click.command()
@click.option('--mimic_zip_path', prompt='Full path of MIMIC-III database ZIP file', required=True)
@click.option('--mimic_code_path', prompt='Full path of mimic-code repository', required=True)
@click.option('--mimic_extract_path', prompt='Full path of MIMIC-Extract repository', required=True)
@click.option('--pg_host', prompt='PostgreSQL database host', required=True, default='localhost')
@click.option('--pg_db', prompt='PostgreSQL database name', required=True, default='mimic')
@click.option('--pg_user', prompt='PostgreSQL database user', required=True, default=os.getlogin())
@click.option('--pg_password', prompt='PostgreSQL database password', required=True, default='')
@click.option('--pg_port', prompt='PostgreSQL database port', required=True, default=5432, type=int)
def run(mimic_zip_path, mimic_code_path, mimic_extract_path, pg_host, pg_user, pg_password, pg_port, pg_db):
    """Setup the MIMIC-III database and MIMIC-Extract resources."""

    # Check file inputs
    if not Path(mimic_zip_path).is_dir():
        click.echo(f'\nMIMIC-III ZIP does not exist at {mimic_zip_path}')
        raise click.Abort
    if not Path(mimic_code_path).is_dir():
        click.echo(
            f'\nmimic-code directory does not exist at {mimic_code_path}')
        raise click.Abort
    if not Path(mimic_extract_path).is_dir():
        click.echo(
            f'\nMIMIC-Extract directory does not exist at {mimic_extract_path}')
        raise click.Abort

    try:
        conn = psycopg2.connect(
            host=pg_host,
            user=pg_user,
            password=pg_password,
            port=pg_port
        )
    except psycopg2.OperationalError:
        click.echo(
            'Error connecting to PostgreSQL database. Check connection inputs.')
        raise click.Abort

    click.echo('-'*50)
    click.echo('Building MIMIC-III Database')
    click.echo('-'*50)
    subrun(f'make -C "{mimic_code_path}/mimic-iii/buildmimic/postgres/" create-user mimic-gz datadir="{mimic_zip_path}" DBNAME="{pg_db}" DBUSER="{pg_user}" DBPASS="{pg_password}" DBHOST="{pg_host}" DBPORT="{pg_port}"',
           stdout=sys.stdout, stderr=sys.stderr, shell=True)

    

if __name__ == '__main__':
    run()
