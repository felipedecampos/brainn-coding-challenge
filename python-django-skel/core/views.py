import re
from django.shortcuts import render
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import os
from django.db import IntegrityError
from django.core import serializers
from django.http import HttpResponse, JsonResponse
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


def repository_list_as_json(request):
    object_list = Repository.objects.all()
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')


def repository_add_tags(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            repository_id = request.POST.get('repository_id')
            regex = "\s*,\s*"
            stored_tags_as_list = split_str_to_list(
                list(
                    Repository.objects.values_list('tags', flat=True).filter(repository_id=repository_id)
                ).pop(0).lower(),
                regex
            )
            posted_tags_as_list = split_str_to_list(
                str(request.POST.get('tags')).lower(),
                regex
            )
            tags = list(set(stored_tags_as_list) | set(posted_tags_as_list))
            repository = Repository.objects.get(repository_id=repository_id)
            repository.tags = ', '.join(tags)
            repository.save()
            return JsonResponse({
                'status': 'success',
                'msg': 'Tags: ' + request.POST.get('tags') + ', successfully added'
            })
        except Repository.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': 'Repository does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def repository_delete_tag(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            repository_id = request.POST.get('repository_id')
            regex = "\s*,\s*"
            tags = split_str_to_list(
                list(
                    Repository.objects.values_list('tags', flat=True).filter(repository_id=repository_id)
                ).pop(0).lower(),
                regex
            )
            deleted_tag = str(request.POST.get('tag')).lower()
            tags.remove(deleted_tag)
            repository = Repository.objects.get(repository_id=repository_id)
            repository.tags = ', '.join(tags)
            repository.save()
            return JsonResponse({
                'status': 'success',
                'msg': 'Tag: ' + request.POST.get('tag') + ', successfully removed'
            })
        except Repository.DoesNotExist:
            return JsonResponse({'status': 'fail', 'msg': 'Repository does not exist'})
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def split_str_to_list(string, regex):
    return list(filter(lambda x: x, re.compile(regex).split(string)))
