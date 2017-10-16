# features/steps/steps.py
import re
from behave import given, when, then, step
import subprocess


# GIT
@given(u'que temos GIT instalado')
def step_impl(context):
    pass


@when(u'eu executo o comando "{command}" no terminal para verificar a versao do GIT')
def step_impl(context, command):
    context.completed_subprocess = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT, close_fds=True)


@then(u'eu deveria ver {version} mais a versao do GIT')
def step_impl(context, version):
    assert version.strip('"') in context.completed_subprocess.stdout.readline().decode("utf-8")


# Python
@given(u'que temos Python instalado')
def step_impl(context):
    pass


@when(u'eu executo o comando "{command}" no terminal para verificar a versao do Python')
def step_impl(context, command):
    context.completed_subprocess = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT, close_fds=True)


@then(u'eu deveria ver "{version}" mais a versao do Python')
def step_impl(context, version):
    assert version in context.completed_subprocess.stdout.readline().decode("utf-8")


# Django
@given(u'que temos o Django instalado')
def step_impl(context):
    pass


@when(
    u'eu executo os seguintes comando "{command1}" "{command2}" "{command3}" no terminal para verificar a versao do Django')
def step_impl(context, command1, command2, command3):
    context.completed_subprocess = subprocess.Popen([command1, command2, command3], shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT, close_fds=True)


@then(u'eu deveria ver a versao do django')
def step_impl(context):
    assert context.completed_subprocess.stdout.readline().decode("utf-8")
