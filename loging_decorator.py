from datetime import datetime
import requests
import time


def log_decor(path_to_file):

    def _log_decor(old_function):

        def new_function(*args, **kwargs):

            call_func = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            result = old_function(*args, **kwargs)
            func_name = old_function.__name__

            with open(f'{path_to_file}data.log', 'a', encoding='utf-8') as file:
                file.write(f"{call_func} - {func_name} - {args, kwargs} - {result}\n")

            return result

        return new_function

    return _log_decor


@log_decor('./')
def get_newest_question(*tags):
    url = 'https://api.stackexchange.com/2.3/questions'
    links_list = []
    for tag in tags:
        params = {'tagged': tag,
                  'pagesize': 1,
                  'site': 'stackoverflow.com'
                  }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise SystemExit(error)

        data = response.json()['items'][0]
        links_list.append((data['link'], data['title']))
    return links_list


if __name__ == '__main__':
    get_newest_question('python', 'sql', 'orm')

