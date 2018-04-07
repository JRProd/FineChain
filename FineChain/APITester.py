from FineChainAPI import API
from rx import Observable, Observer

from pprint import pprint


if __name__ == '__main__':
    print('STARTING API TESTING')
    session = {'refresh': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MjMxNDQzNjAsImlkZW50aXR5Ijp7InVzZXJfaWQiOjQ4fSwianRpIjoiNTVhYjc4MjgtZWU3Mi00OTY3LWI5Y2MtMjJlZTUwMjdmYzJiIiwibmJmIjoxNTIzMTQ0MzYwLCJleHAiOjE1MjU3MzYzNjAsInR5cGUiOiJyZWZyZXNoIn0.jSo8Ts92ZQcWMLtfE5zYTThGtF8WFsPKV0_jwt3y_Wk',
               'session': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1MjMxNDQzNjAsImlkZW50aXR5Ijp7InVzZXJfaWQiOjQ4fSwidHlwZSI6ImFjY2VzcyIsImp0aSI6IjIwMmMwMzkzLTk5MzgtNGU2Mi1hMTI2LWE5YmFiNzE3NTgyZSIsIm5iZiI6MTUyMzE0NDM2MCwiZXhwIjoxNTIzMTQ1MjYwLCJmcmVzaCI6ZmFsc2V9.qO83bH9OQ60_cTNl7oO_jxCdDpYLP3htELcuL-nvfZM'}

    response = API.createCompany('WootWootInc', session).subscribe(on_next=lambda r: {
        print(r)
    })