from django.shortcuts import render
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
from django.db import IntegrityError
from core.models import Repository


# Create your views here.
def get_repositories(username, page=False):
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
            get_repositories(username, repositories.get('pageInfo').get('endCursor'))

    return True


def repository_list(request):
    repositories = Repository.objects.all()
    return render(request, 'core/repository_list.html', {'repositories': repositories})
