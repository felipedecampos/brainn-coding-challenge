from django.shortcuts import render
from django.http import HttpResponse

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os


# Create your views here.
def getRepositories(username):
    query = '''
      query {
        user(login: "%s") {
          starredRepositories(first: 1) {
            totalCount
            edges {
              node {
                id
                name
                url
                languages(first: 10) {
                  edges {
                    node {
                      name
                    }
                  }
                }
              }
              cursor
            }
            pageInfo {
              hasNextPage
              hasPreviousPage
              endCursor
            }
          }
        }
      }''' % username
    headers = {'Authorization': 'bearer {0}'.format(os.getenv('GITHUB_API_TOKEN'))}
    url = 'https://api.github.com/graphql'
    transport = RequestsHTTPTransport(url, headers=headers, use_json=True)
    client = Client(transport=transport)
    resp = client.execute(gql(query))
    repositories = resp.get('user').get('starredRepositories')
    return repositories
