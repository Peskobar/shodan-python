Wkład w rozwój
==============

Instalacja środowiska
---------------------

1. Zainstaluj wymagania:

   .. code-block:: bash

      python -m pip install -r requirements.txt

2. Zainstaluj skrypty pre-commit:

   .. code-block:: bash

      pre-commit install

Sprawdzanie zmian
-----------------

Przed wysłaniem poprawek uruchom wszystkie testy statyczne i skanery bezpieczeństwa:

.. code-block:: bash

   pre-commit run --all-files

Wytyczne dotyczące commitów
---------------------------

Do tworzenia wiadomości commit używaj narzędzia Commitizen zgodnego ze standardem Conventional Commits:

.. code-block:: bash

   cz commit

Powyższe polecenie poprowadzi Cię przez proces tworzenia prawidłowej wiadomości commit i automatycznie zweryfikuje format.
