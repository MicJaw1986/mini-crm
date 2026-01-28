"""
Management command do generowania danych demonstracyjnych dla MiniCRM

Użycie:
    python manage.py generate_demo_data
    python manage.py generate_demo_data --clear  # Usuń stare dane przed generowaniem

CZYTAJ KOMENTARZE - Dowiesz się jak tworzyć management commands!
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from contacts.models import Contact, Company
from interactions.models import Interaction
from tasks.models import Task


class Command(BaseCommand):
    """
    Klasa Command dla Django management command

    UWAGA: Każdy management command musi:
    1. Dziedziczyć po BaseCommand
    2. Mieć metodę handle()
    3. Być w pliku w folderze management/commands/
    """

    # Opis komendy (pokazuje się w --help)
    help = 'Generuje dane demonstracyjne dla aplikacji MiniCRM'

    def add_arguments(self, parser):
        """
        Dodawanie argumentów wiersza poleceń

        Przykłady użycia argumentów:
        - python manage.py generate_demo_data --clear
        - python manage.py generate_demo_data --users 5
        """
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Usuń wszystkie istniejące dane przed generowaniem',
        )

        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Liczba użytkowników testowych do utworzenia (domyślnie: 3)',
        )

    def handle(self, *args, **options):
        """
        Główna metoda komendy

        Ta metoda uruchamia się gdy wywołasz:
        python manage.py generate_demo_data
        """

        # self.stdout.write() - odpowiednik print() w management commands
        # Używa kolorów dla lepszej czytelności
        self.stdout.write(self.style.SUCCESS('>> Rozpoczynam generowanie danych demonstracyjnych...'))

        # Sprawdzamy czy użytkownik chce wyczyścić dane
        if options['clear']:
            self.clear_data()

        # Generujemy dane
        users = self.create_users(options['users'])
        self.stdout.write(self.style.SUCCESS(f'>> Utworzono {len(users)} uzytkownikow'))

        companies = self.create_companies(users)
        self.stdout.write(self.style.SUCCESS(f'>> Utworzono {len(companies)} firm'))

        contacts = self.create_contacts(users, companies)
        self.stdout.write(self.style.SUCCESS(f'>> Utworzono {len(contacts)} kontaktow'))

        interactions = self.create_interactions(users, contacts, companies)
        self.stdout.write(self.style.SUCCESS(f'>> Utworzono {len(interactions)} interakcji'))

        tasks = self.create_tasks(users, contacts, companies)
        self.stdout.write(self.style.SUCCESS(f'>> Utworzono {len(tasks)} zadan'))

        # Podsumowanie
        self.stdout.write(self.style.SUCCESS('\n>> Generowanie danych zakonczone pomyslnie!'))
        self.stdout.write(self.style.WARNING('\n>> Dane logowania:'))
        for user in users:
            self.stdout.write(f'   Login: {user.username} | Hasło: demo123')

    def clear_data(self):
        """Usuwa wszystkie istniejące dane demonstracyjne"""
        self.stdout.write(self.style.WARNING('>> Usuwam stare dane...'))

        # Usuwamy tylko użytkowników demo (nie admina!)
        User.objects.filter(username__startswith='demo').delete()

        # Kaskadowe usuwanie usunie też powiązane obiekty
        # dzięki on_delete=models.CASCADE w modelach

        self.stdout.write(self.style.SUCCESS('>> Dane wyczyszczone'))

    def create_users(self, count):
        """
        Tworzy użytkowników testowych

        Args:
            count: Liczba użytkowników do utworzenia

        Returns:
            Lista utworzonych użytkowników
        """
        users = []

        # Polskie imiona i nazwiska
        first_names = ['Jan', 'Anna', 'Piotr', 'Katarzyna', 'Tomasz', 'Magdalena', 'Michał', 'Agnieszka']
        last_names = ['Kowalski', 'Nowak', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik']

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f'demo{i+1}'

            # Sprawdzamy czy użytkownik już istnieje
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                self.stdout.write(self.style.WARNING(f'>> Uzytkownik {username} juz istnieje - uzywam istniejacego'))
            else:
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@minicrm.pl',
                    password='demo123',  # UWAGA: W produkcji NIE używaj prostych haseł!
                    first_name=first_name,
                    last_name=last_name
                )

            users.append(user)

        return users

    def create_companies(self, users):
        """Tworzy firmy"""
        companies = []

        # Przykładowe nazwy firm
        company_names = [
            'Tech Solutions Sp. z o.o.',
            'Digital Marketing Pro',
            'Innowacyjne Systemy IT',
            'Consulting Partners',
            'E-Commerce Masters',
            'Creative Agency',
            'Software Development House',
            'Cloud Services Polska',
            'Data Analytics Group',
            'Mobile Apps Factory',
            'Web Design Studio',
            'Business Intelligence Ltd',
            'AI & Machine Learning Lab',
            'Cyber Security Solutions',
            'Startup Accelerator'
        ]

        # Branże
        industries = ['IT', 'Marketing', 'Consulting', 'E-commerce', 'Finance', 'Healthcare', 'Education']

        # Miasta
        cities = ['Warszawa', 'Kraków', 'Wrocław', 'Poznań', 'Gdańsk', 'Łódź', 'Katowice']

        for name in company_names[:12]:  # Tworzymy 12 firm
            company = Company.objects.create(
                name=name,
                nip=f'{random.randint(1000000000, 9999999999)}',
                industry=random.choice(industries),
                street=f'ul. {random.choice(["Testowa", "Przykładowa", "Główna", "Długa"])} {random.randint(1, 100)}',
                postal_code=f'{random.randint(10, 99)}-{random.randint(100, 999)}',
                city=random.choice(cities),
                country='Polska',
                website=f'www.{name.lower().replace(" ", "").replace(".", "")[:15]}.pl',
                owner=random.choice(users)  # Losowy właściciel
            )
            companies.append(company)

        return companies

    def create_contacts(self, users, companies):
        """Tworzy kontakty"""
        contacts = []

        # Polskie imiona
        male_names = ['Jan', 'Piotr', 'Tomasz', 'Michał', 'Krzysztof', 'Andrzej', 'Marcin', 'Łukasz', 'Jakub', 'Adam']
        female_names = ['Anna', 'Katarzyna', 'Magdalena', 'Agnieszka', 'Joanna', 'Ewa', 'Monika', 'Barbara', 'Aleksandra', 'Karolina']
        last_names = ['Kowalski', 'Nowak', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik', 'Kamiński', 'Zieliński', 'Szymański', 'Woźniak']

        # Stanowiska
        positions = ['CEO', 'CTO', 'CFO', 'Marketing Manager', 'Sales Director', 'Product Manager', 'Developer', 'Designer', 'Consultant', 'Analyst']

        # Statusy
        statuses = ['lead', 'prospect', 'customer', 'churned']
        status_weights = [30, 25, 40, 5]  # Więcej klientów niż leadów

        # Tagi
        tags_options = [
            'vip,partner',
            'nowy klient',
            'vip',
            'partner strategiczny',
            'potencjał rozwoju',
            'wymaga uwagi',
            '',  # Niektóre bez tagów
        ]

        for i in range(45):  # 45 kontaktów
            # Losujemy płeć i imię
            is_male = random.choice([True, False])
            first_name = random.choice(male_names if is_male else female_names)
            last_name = random.choice(last_names)

            # Email
            email = f'{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com'

            contact = Contact.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=f'+48 {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(100, 999)}',
                mobile=f'+48 {random.randint(500, 799)} {random.randint(100, 999)} {random.randint(100, 999)}',
                company=random.choice(companies) if random.random() > 0.2 else None,  # 80% ma firmę
                position=random.choice(positions),
                status=random.choices(statuses, weights=status_weights)[0],
                tags=random.choice(tags_options),
                notes=f'Kontakt dodany automatycznie w celach demonstracyjnych.\n{"Bardzo aktywny klient." if random.random() > 0.7 else ""}',
                owner=random.choice(users)
            )
            contacts.append(contact)

        return contacts

    def create_interactions(self, users, contacts, companies):
        """Tworzy interakcje"""
        interactions = []

        # Typy interakcji
        types = ['email', 'phone', 'meeting', 'note', 'call']

        # Przykładowe tematy
        email_subjects = [
            'Spotkanie w sprawie projektu',
            'Oferta handlowa',
            'Pytanie o produkt',
            'Feedback po prezentacji',
            'Zaproszenie na webinar',
            'Podsumowanie rozmowy',
        ]

        phone_subjects = [
            'Rozmowa telefoniczna - weryfikacja wymagań',
            'Konsultacja techniczna',
            'Cold call - nowy lead',
            'Follow-up po spotkaniu',
            'Rozwiązanie problemu',
        ]

        meeting_subjects = [
            'Spotkanie biznesowe w biurze',
            'Prezentacja produktu',
            'Warsztat strategiczny',
            'Negocjacje umowy',
            'Demo systemu',
        ]

        # Generujemy 80 interakcji
        for i in range(80):
            interaction_type = random.choice(types)

            # Wybieramy temat w zależności od typu
            if interaction_type == 'email':
                subject = random.choice(email_subjects)
                description = f'Email dotyczący: {subject.lower()}. Klient wyraził zainteresowanie naszą ofertą.'
            elif interaction_type in ['phone', 'call']:
                subject = random.choice(phone_subjects)
                description = f'Rozmowa trwała {random.randint(5, 45)} minut. Omówiono kluczowe punkty projektu.'
            elif interaction_type == 'meeting':
                subject = random.choice(meeting_subjects)
                description = f'Spotkanie w biurze klienta. Obecni: {random.randint(2, 5)} osób. Bardzo produktywna dyskusja.'
            else:
                subject = 'Notatka wewnętrzna'
                description = 'Ważna informacja do zapamiętania o tym kliencie.'

            # Data interakcji - losowa w ciągu ostatnich 90 dni
            days_ago = random.randint(0, 90)
            interaction_date = timezone.now() - timedelta(days=days_ago, hours=random.randint(8, 18))

            # Przypisujemy do kontaktu LUB firmy
            contact = random.choice(contacts) if random.random() > 0.3 else None
            company = random.choice(companies) if contact is None else contact.company

            interaction = Interaction.objects.create(
                contact=contact,
                company=company,
                interaction_type=interaction_type,
                subject=subject,
                description=description,
                interaction_date=interaction_date,
                is_important=random.random() > 0.85,  # 15% oznaczonych jako ważne
                owner=random.choice(users)
            )
            interactions.append(interaction)

        return interactions

    def create_tasks(self, users, contacts, companies):
        """Tworzy zadania"""
        tasks = []

        # Tytuły zadań
        task_titles = [
            'Przygotuj ofertę handlową',
            'Zadzwoń do klienta - follow-up',
            'Przygotuj prezentację produktu',
            'Wysłać dokumentację techniczną',
            'Umówić spotkanie demo',
            'Przygotować raport miesięczny',
            'Zweryfikować wymagania projektowe',
            'Zaktualizować CRM',
            'Przeprowadzić analizę konkurencji',
            'Utworzyć propozycję współpracy',
            'Wysłać newsletter',
            'Zaplanować kampanię marketingową',
            'Sprawdzić status płatności',
            'Przygotować kontrakt',
            'Zorganizować webinar',
        ]

        # Statusy - więcej "do zrobienia" i "w trakcie"
        statuses = ['todo', 'in_progress', 'done', 'cancelled']
        status_weights = [40, 30, 25, 5]

        # Priorytety
        priorities = ['low', 'medium', 'high', 'urgent']
        priority_weights = [20, 50, 25, 5]

        for i in range(35):  # 35 zadań
            title = random.choice(task_titles)
            status = random.choices(statuses, weights=status_weights)[0]
            priority = random.choices(priorities, weights=priority_weights)[0]

            # Termin - losowa data w przyszłości lub przeszłości
            if status == 'done':
                # Zadania wykonane - termin w przeszłości
                due_date = timezone.now() - timedelta(days=random.randint(1, 30))
            elif status == 'cancelled':
                # Zadania anulowane - różne daty
                due_date = timezone.now() + timedelta(days=random.randint(-15, 15))
            else:
                # Zadania aktywne - niektóre przeterminowane, niektóre w przyszłości
                if random.random() > 0.7:
                    # 30% przeterminowanych
                    due_date = timezone.now() - timedelta(days=random.randint(1, 10))
                else:
                    # 70% w przyszłości
                    due_date = timezone.now() + timedelta(days=random.randint(1, 60))

            # Przypisanie do kontaktu lub firmy
            contact = random.choice(contacts) if random.random() > 0.4 else None
            company = random.choice(companies) if contact is None else contact.company

            task = Task.objects.create(
                title=title,
                description=f'Zadanie wygenerowane automatycznie w celach demonstracyjnych.\n\nPriorytet: {priority}\nStatus: {status}',
                status=status,
                priority=priority,
                due_date=due_date,
                contact=contact,
                company=company,
                assigned_to=random.choice(users),
                owner=random.choice(users)
            )
            tasks.append(task)

        return tasks


# PODSUMOWANIE - Co się nauczyłeś o management commands:
# 1. Klasa musi dziedziczyć po BaseCommand
# 2. Główna logika w metodzie handle()
# 3. add_arguments() - dodawanie parametrów CLI
# 4. self.stdout.write() - wypisywanie komunikatów
# 5. self.style.SUCCESS/WARNING/ERROR - kolory w terminalu
# 6. Komenda uruchamia się: python manage.py nazwa_pliku
# 7. Przydatne do: generowania danych, migracji, zadań cron, etc.
