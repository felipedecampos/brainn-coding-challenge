from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
from core.models import Repository


# Create your views here.
def getRepositories(username, page=False):
    pagination = "" if not page else ', after: "' + page + '"'
    query = '''
      query {
        user(login: "%s") {
          starredRepositories(first: 10%s) {
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
      }''' % (username, pagination)

    headers = {'Authorization': 'bearer {0}'.format(os.getenv('GITHUB_API_TOKEN'))}
    url = 'https://api.github.com/graphql'
    transport = RequestsHTTPTransport(url, headers=headers, use_json=True)
    client = Client(transport=transport)
    resp = client.execute(gql(query))
    repositories = resp.get('user').get('starredRepositories')

    for repository in repositories.get('edges'):
        languages = []

        for language in repository.get('node').get('languages').get('edges'):
            if language.get('node').get('name') not in languages:
                languages.append(language.get('node').get('name'))

        try:
            entityRepository = Repository(
                username=username,
                repository_id=repository.get('node').get('id'),
                name=repository.get('node').get('name'),
                url=repository.get('node').get('url'),
                languages=", ".join(languages),
                tags="",
            )
            entityRepository.save()
        except IntegrityError:
            continue

        if repositories.get('pageInfo').get('hasNextPage'):
            getRepositories(username, repositories.get('pageInfo').get('endCursor'))

    return True
