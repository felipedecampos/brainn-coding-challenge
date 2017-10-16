# language: pt

# features/environment.feature
Funcionalidade: Verificando instalacao do GIT
    Cenario: Verificar se possui GIT
        Dado que temos GIT instalado
        Quando eu executo o comando "git --version" no terminal para verificar a versao do GIT
        Entao eu deveria ver "git version" mais a versao do GIT
    Cenario: Verificar se possui Python
        Dado que temos Python instalado
        Quando eu executo o comando "python3 -V" no terminal para verificar a versao do Python
        Entao eu deveria ver "Python" mais a versao do Python
    Cenario: Verificar se existe o package Django instalado
        Dado que temos o Django instalado
        Quando eu executo os seguintes comando "python" "import django" "django.get_version()" no terminal para verificar a versao do Django
        Entao eu deveria ver a versao do django