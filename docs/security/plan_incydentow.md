# Plan reagowania na incydenty

## Cel
Zapewnienie spójnego i skutecznego postępowania podczas incydentów bezpieczeństwa w organizacji.

## Zakres
Plan obejmuje wszystkie systemy produkcyjne, dane klientów i infrastrukturę wspierającą.

## Role personelu
- **Koordynator Bezpieczeństwa** – prowadzi cały proces, odpowiada za kontakt z zarządem i organami zewnętrznymi.
- **Analityk SOC** – monitoruje zdarzenia, inicjuje proces identyfikacji i oceny incydentu.
- **Administrator Systemów** – wykonuje działania techniczne związane z ograniczeniem i eradykacją.
- **Zespół Prawny** – ocenia obowiązki prawne związane z incydentem.
- **PR & Komunikacja** – przygotowuje komunikaty dla mediów i klientów.

## Procedury eskalacji
1. **Incydent o niskiej istotności** – analityk SOC rozwiązuje problem, informuje koordynatora w raporcie dziennym.
2. **Incydent o średniej istotności** – analityk SOC powiadamia koordynatora natychmiast i tworzy zgłoszenie w systemie JIRA; administrator systemów przeprowadza ograniczenie.
3. **Incydent o wysokiej istotności lub naruszenie danych osobowych** – koordynator natychmiast informuje zarząd, zespół prawny oraz PR, a także uruchamia komunikację kryzysową zgodnie z wymogami RODO.

## Wzory powiadomień
### Powiadomienie e-mail do kierownictwa
Temat: [INC] Wykryto incydent bezpieczeństwa {{ID_ZGLOSZENIA}}

Treść:
- Data i godzina wykrycia: {{DATA_WYKRYCIA}}
- System: {{SYSTEM}}
- Krótki opis: {{OPIS}}
- Podjęte działania: {{DZIALANIA}}
- Osoba kontaktowa: {{OSOBA}}

### Powiadomienie do użytkowników końcowych
Temat: Informacja o incydencie bezpieczeństwa

Treść:
Szanowni Państwo,

w dniu {{DATA_WYKRYCIA}} doszło do incydentu bezpieczeństwa w systemie {{SYSTEM}}. Podjęliśmy niezwłoczne działania ograniczające oraz zabezpieczające. Więcej informacji uzyskają Państwo kontaktując się z {{OSOBA}} pod adresem {{EMAIL_OSOBY}}.

## Etapy postępowania
### Przygotowanie
- Utrzymywanie aktualnej listy zasobów i właścicieli systemów.
- Regularne testy kopii zapasowych oraz aktualizacje procedur.
- Konfiguracja monitoringu i alertów we wszystkich systemach krytycznych.
- Utrzymywanie kontaktów do zespołów wewnętrznych i zewnętrznych partnerów.
- Szkolenia personelu z zakresu reagowania na incydenty.

### Identyfikacja
- Monitorowanie dzienników zdarzeń i alertów.
- Weryfikacja zgłoszeń z systemów IDS/IPS oraz od użytkowników.
- Określenie zakresu i wpływu incydentu na podstawie analizy danych.
- Rejestracja incydentu w JIRA z wykorzystaniem szablonu `SEC-INC`.

### Ograniczenie
- Natychmiastowe odseparowanie zainfekowanych hostów od sieci.
- Blokowanie kont użytkowników powiązanych z incydentem.
- Wprowadzenie reguł zapory sieciowej ograniczających dalsze rozprzestrzenianie.
- Aktualizacja statusu zgłoszenia w JIRA na `Ograniczanie` z automatyczną etykietą `confine`.

### Eradykacja
- Usunięcie złośliwego oprogramowania i artefaktów.
- Przywrócenie konfiguracji bezpieczeństwa do stanu sprzed incydentu.
- Weryfikacja integralności systemów po działaniach naprawczych.
- W JIRA zmiana etapu na `Eradykacja` oraz dodanie etykiety `eradicate`.

### Odzyskiwanie
- Przywrócenie usług do normalnego działania z wykorzystaniem sprawdzonych kopii zapasowych.
- Monitorowanie systemów pod kątem ponownego wystąpienia incydentu.
- W JIRA zmiana statusu na `Odzyskiwanie` oraz dodanie etykiety `recovery`.

### Wnioski
- Analiza przyczyn źródłowych incydentu (root cause analysis).
- Aktualizacja procedur oraz konfiguracji zabezpieczeń.
- Szkolenie personelu na podstawie zdobytych doświadczeń.
- Zamknięcie zgłoszenia w JIRA z etykietą `closed` oraz dołączenie raportu końcowego.

## Integracja z systemem zgłoszeń JIRA
### Szablon zgłoszenia `SEC-INC`
- Projekt: `BEZPIECZENSTWO`
- Typ zgłoszenia: `Incydent`
- Tytuł: `[INC] Krótki opis zdarzenia`
- Pola obowiązkowe:
  - Opis: pełny opis incydentu wraz z czasem wykrycia.
  - Priorytet: `Wysoki`, `Średni` lub `Niski` zgodnie z oceną wpływu.
  - Środowisko: `Produkcja`, `Test`, `Rozwój`.
  - Systemy dotknięte incydentem.
- Automatyczne etykiety: `security`, `incident`.
- Automatyczne utworzenie zadania podrzędnego `Analiza` przypisanego do analityka SOC.

### Automatyczne etykiety etapów
W zależności od bieżącego etapu pracy nad incydentem, system JIRA dodaje poniższe etykiety:
- `identify` – etap Identyfikacji
- `confine` – etap Ograniczenia
- `eradicate` – etap Eradykacji
- `recovery` – etap Odzyskiwania
- `closed` – zgłoszenie zamknięte po analizie powyincydentalnej

## Rejestrowanie i przechowywanie danych
- Wszystkie logi i artefakty związane z incydentem przechowywane są przez minimum 12 miesięcy w bezpiecznym repozytorium z ograniczonym dostępem.
- Raporty końcowe są wersjonowane i udostępniane jedynie uprawnionym osobom.

## Przegląd planu
Plan przeglądany jest co 12 miesięcy lub po każdym incydencie wysokiej istotności. Aktualizacje są zatwierdzane przez koordynatora bezpieczeństwa i zarząd.
