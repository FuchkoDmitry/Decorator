import requests
import logging

logger = logging.getLogger()
logging.getLogger('urllib3').setLevel('CRITICAL')


def log_decor(path_to_file):

    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level='DEBUG',
                        filename=f'{path_to_file}data_.log',
                        datefmt='%d %b %Y - %H:%M:%S'
                        )

    def _log_decor(old_function):

        def new_function(*args, **kwargs):

            result = old_function(*args, **kwargs)
            func_name = old_function.__name__
            logger.debug(f'Function {func_name} was called with {args, kwargs} arguments. Result: {result}.')

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
            logger.error(f'Request with parameters {params} if failed. {SystemExit(error)}')
            raise SystemExit(error)
        data = response.json()['items'][0]
        links_list.append((data['link'], data['title']))
    return links_list


if __name__ == '__main__':
    get_newest_question('python', 'sql', 'orm')
