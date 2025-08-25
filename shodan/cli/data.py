import click
import requests
import shodan
import shodan.helpers as helpers

from shodan.cli.helpers import get_api_key


@click.group()
def data():
    """Masowy dostęp do danych Shodan"""
    pass


@data.command(name='list')
@click.option('--dataset', help='Wyświetl dostępne pliki w podanym zbiorze', default=None, type=str)
def data_list(dataset):
    """Wyświetl dostępne zbiory danych lub pliki w ich ramach."""
    # Skonfiguruj połączenie z API
    key = get_api_key()
    api = shodan.Shodan(key)

    if dataset:
        # Wyświetl pliki w tym zbiorze
        files = api.data.list_files(dataset)

        for file in files:
            click.echo(click.style(u'{:20s}'.format(file['name']), fg='cyan'), nl=False)
            click.echo(click.style('{:10s}'.format(helpers.humanize_bytes(file['size'])), fg='yellow'), nl=False)

            # Wyświetl sumę SHA1, jeśli dostępna
            if file.get('sha1'):
                click.echo(click.style('{:42s}'.format(file['sha1']), fg='green'), nl=False)

            click.echo('{}'.format(file['url']))
    else:
        # Jeśli nie podano zbioru, pokaż listę wszystkich zbiorów
        datasets = api.data.list_datasets()

        for ds in datasets:
            click.echo(click.style('{:15s}'.format(ds['name']), fg='cyan'), nl=False)
            click.echo('{}'.format(ds['description']))


@data.command(name='download')
@click.option('--chunksize', help='Rozmiar części pobieranych do pamięci przed zapisem na dysk.', default=1024, type=int)
@click.option('--filename', '-O', help='Zapisz plik pod podaną nazwą zamiast domyślnej.')
@click.argument('dataset', metavar='<dataset>')
@click.argument('name', metavar='<file>')
def data_download(chunksize, filename, dataset, name):
    # Skonfiguruj połączenie z API
    key = get_api_key()
    api = shodan.Shodan(key)

    # Pobierz obiekt pliku wskazany przez użytkownika, zawierający adres URL i rozmiar
    file = None
    try:
        files = api.data.list_files(dataset)
        for tmp in files:
            if tmp['name'] == name:
                file = tmp
                break
    except shodan.APIError as e:
        raise click.ClickException(e.value)

    # Plik nie jest dostępny
    if not file:
        raise click.ClickException('Nie znaleziono pliku')

    # Rozpocznij pobieranie pliku
    try:
        odpowiedz = requests.get(file['url'], stream=True, timeout=30)
        odpowiedz.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise click.ClickException(f'Błąd pobierania: {exc}')

    # Ustal rozmiar pliku na podstawie nagłówków
    filesize = odpowiedz.headers.get('content-length', None)
    if not filesize:
        # Wróć do rozmiaru podanego przez API
        filesize = file['size']
    else:
        filesize = int(filesize)

    chunk_size = 1024
    limit = filesize / chunk_size

    # Utwórz domyślną nazwę pliku na podstawie datasetu i nazwy pliku w nim
    if not filename:
        filename = '{}-{}'.format(dataset, name)

    # Otwórz plik wyjściowy i zapisuj go w kawałkach
    with open(filename, 'wb') as fout:
        with click.progressbar(odpowiedz.iter_content(chunk_size=chunk_size), length=limit) as bar:
            for chunk in bar:
                if chunk:
                    fout.write(chunk)

    click.echo(click.style('Pobieranie zakończone: {}'.format(filename), 'green'))
