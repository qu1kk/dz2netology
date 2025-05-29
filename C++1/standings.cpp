#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <string>
#include <limits>
#include <cctype>
#include <sstream>
#include <ctime>
#include <regex>

using namespace std;

// Валидация даты
bool isValidDate(const string& date) {
    regex pattern(R"((0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.\d{4})");
    return regex_match(date, pattern);
}

/**
 * @class Match
 * @brief Представляет футбольный матч с датой и результатом.
 */
class Match {
public:
    Match(string d, char r, string t1, string t2)
        : date(std::move(d)), result(r), team1(std::move(t1)), team2(std::move(t2)) {}

    string getDate() const { return date; }
    char getResult() const { return result; }
    string getTeam1() const { return team1; }
    string getTeam2() const { return team2; }
    
    void setTeam1(const string& name) { team1 = name; }
    void setTeam2(const string& name) { team2 = name; }

    void print() const {
        cout << date << " | "
             << team1 << " vs " << team2 << " | "
             << (result == 'V' ? "Победа " + team1 : "Ничья");
    }

private:
    string date;    ///< Дата матча (ДД.ММ.ГГГГ)
    char result;    ///< Результат (V/D)
    string team1;   ///< Команда 1
    string team2;   ///< Команда 2
};

/**
 * @class Team
 * @brief Представляет команду в турнирной таблице.
 */
class Team {
public:
    Team() : name(""), wins(0), draws(0), losses(0), position(0) {}
    explicit Team(string name) : name(std::move(name)), wins(0), draws(0), losses(0), position(0) {}

    // Геттеры
    string getName() const { return name; }
    unsigned int getWins() const { return wins; }
    unsigned int getDraws() const { return draws; }
    unsigned int getLosses() const { return losses; }
    unsigned int getGames() const { return wins + draws + losses; }
    unsigned int getPoints() const { return 3 * wins + draws; }
    unsigned int getPosition() const { return position; }

    // Сеттеры
    void setName(const string& newName) { name = newName; }
    void setWins(unsigned int w) { wins = w; }
    void setDraws(unsigned int d) { draws = d; }
    void setLosses(unsigned int l) { losses = l; }
    void setPosition(unsigned int pos) { position = pos; }

    void addWin() { wins++; }
    void addDraw() { draws++; }
    void addLoss() { losses++; }

    bool operator<(const Team& other) const {
        if (getPoints() != other.getPoints())
            return getPoints() > other.getPoints();
        if (wins != other.wins)
            return wins > other.wins;
        if (losses != other.losses)
            return losses < other.losses;
        return name < other.name;
    }

private:
    string name;
    unsigned int wins;
    unsigned int draws;
    unsigned int losses;
    unsigned int position;
};

/**
 * @class Tournament
 * @brief Управляет турнирной таблицей и операциями с ней.
 */
class Tournament {
public:
    /**
     * @brief Загружает данные о командах из файла.
     */
    void loadFromFile(const string& filename) {
        ifstream file(filename);
        if (!file.is_open()) {
            throw runtime_error("Ошибка открытия файла: " + filename);
        }

        teams.clear();
        matches.clear();

        string line;
        while (getline(file, line)) {
            if (line.empty()) continue;

            if (line[0] == '#') {
                // Загрузка матчей
                char result;
                string date, team1, team2;
                stringstream ss(line.substr(1));
                ss >> date >> result;
                getline(ss, team1);
                getline(ss, team2);
                matches.emplace_back(date, result, team1, team2);
            } else {
                // Загрузка команд
                string name;
                unsigned int pos, wins, draws, losses;
                stringstream ss(line);
                ss >> name >> pos >> wins >> draws >> losses;
                
                Team team(name);
                team.setPosition(pos);
                team.setWins(wins);
                team.setDraws(draws);
                team.setLosses(losses);
                teams.push_back(team);
            }
        }

        if (teams.size() < 25) {
            generateDemoTeams(25 - teams.size());
        }

        sortTeams();
        cout << "Данные загружены. Команд: " << teams.size() 
             << ", Матчей: " << matches.size() << endl;
    }

    /**
     * @brief Сохраняет данные о командах в файл.
     */
    void saveToFile(const string& filename) const {
        ofstream file(filename);
        if (!file.is_open()) {
            throw runtime_error("Ошибка создания файла: " + filename);
        }

        // Сохранение команд
        for (const auto& team : teams) {
            file << team.getName() << " "
                 << team.getPosition() << " "
                 << team.getWins() << " "
                 << team.getDraws() << " "
                 << team.getLosses() << "\n";
        }

        // Сохранение матчей
        for (const auto& match : matches) {
            file << "#" << match.getDate() << " "
                 << match.getResult() << " "
                 << match.getTeam1() << " "
                 << match.getTeam2() << "\n";
        }

        cout << "Данные сохранены в файл: " << filename 
             << " (команд: " << teams.size() 
             << ", матчей: " << matches.size() << ")\n";
    }

    /**
     * @brief Добавляет новую команду в таблицу.
     */
    void addTeam(const string& name) {
        if (findTeamIterator(name) != teams.end()) {
            throw invalid_argument("Команда '" + name + "' уже существует!");
        }
        teams.emplace_back(name);
        sortTeams();
        cout << "Команда '" << name << "' добавлена." << endl;
    }

    /**
     * @brief Удаляет команду из таблицы.
     */
    void removeTeam(const string& name) {
        auto it = findTeamIterator(name);
        if (it == teams.end()) {
            throw invalid_argument("Команда '" + name + "' не найдена!");
        }
        
        // Удаляем связанные матчи
        matches.erase(
            remove_if(matches.begin(), matches.end(),
                [&](const Match& m) {
                    return m.getTeam1() == name || m.getTeam2() == name;
                }),
            matches.end()
        );
        
        teams.erase(it);
        sortTeams();
        cout << "Команда '" << name << "' и связанные матчи удалены." << endl;
    }

    /**
     * @brief Редактирует название команды.
     */
    void editTeam(const string& oldName, const string& newName) {
        auto it = findTeamIterator(oldName);
        if (it == teams.end()) {
            throw invalid_argument("Команда '" + oldName + "' не найдена!");
        }
        
        if (!newName.empty() && findTeamIterator(newName) == teams.end()) {
            // Обновляем матчи
            for (auto& match : matches) {
                if (match.getTeam1() == oldName) {
                    match.setTeam1(newName);
                }
                if (match.getTeam2() == oldName) {
                    match.setTeam2(newName);
                }
            }
            
            it->setName(newName);
            sortTeams();
            cout << "Команда '" << oldName << "' переименована в '" << newName << "'." << endl;
        } else {
            throw invalid_argument("Новое название не может быть пустым или совпадать с существующей командой!");
        }
    }

    /**
     * @brief Обновляет результаты матчей текущего тура.
     */
    void updateRoundResults() {
        unsigned int matchCount;
        cout << "Введите количество матчей в туре: ";
        
        // Валидация ввода
        while (!(cin >> matchCount) || matchCount < 0) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Ошибка! Введите неотрицательное число: ";
        }
        cin.ignore();

        for (unsigned int i = 0; i < matchCount; ++i) {
            cout << "\nМатч " << i + 1 << ":\n";
            
            string date;
            do {
                cout << "Дата матча (ДД.ММ.ГГГГ): ";
                getline(cin, date);
            } while (!isValidDate(date));

            char result;
            do {
                cout << "Результат (V - победа, D - ничья): ";
                cin >> result;
                result = toupper(result);
                cin.ignore();
            } while (result != 'V' && result != 'D');

            string team1, team2;
            cout << "Команда 1: ";
            getline(cin, team1);
            cout << "Команда 2: ";
            getline(cin, team2);

            auto it1 = findTeamIterator(team1);
            auto it2 = findTeamIterator(team2);

            if (it1 == teams.end() || it2 == teams.end()) {
                cerr << "Ошибка: ";
                if (it1 == teams.end()) cerr << "команда '" << team1 << "' не найдена. ";
                if (it2 == teams.end()) cerr << "команда '" << team2 << "' не найдена.";
                cerr << " Матч пропущен.\n";
                continue;
            }

            // Сохраняем матч
            matches.emplace_back(date, result, team1, team2);

            // Обновляем статистику
            if (result == 'V') {
                it1->addWin();
                it2->addLoss();
            } else {
                it1->addDraw();
                it2->addDraw();
            }
        }

        sortTeams();
        cout << "\nРезультаты тура обновлены. Добавлено матчей: " << matchCount << "\n";
    }

    /**
     * @brief Выводит полную турнирную таблицу.
     */
    void printTable() const {
        if (teams.empty()) {
            cout << "Таблица пуста!\n";
            return;
        }

        const int colWidth[] = {8, 25, 5, 5, 5, 5, 10, 10};
        const char* headers[] = {
            "Место", "Команда", "И", "В", "Н", "П", "Очки", "Форма"
        };

        // Заголовки
        for (int i = 0; i < 8; ++i) {
            cout << left << setw(colWidth[i]) << headers[i] << " | ";
        }
        cout << "\n" << string(88, '-') << "\n";

        // Данные команд
        for (const auto& team : teams) {
            cout << setw(colWidth[0]) << team.getPosition() << " | "
                 << setw(colWidth[1]) << team.getName() << " | "
                 << setw(colWidth[2]) << team.getGames() << " | "
                 << setw(colWidth[3]) << team.getWins() << " | "
                 << setw(colWidth[4]) << team.getDraws() << " | "
                 << setw(colWidth[5]) << team.getLosses() << " | "
                 << setw(colWidth[6]) << team.getPoints() << " | "
                 << setw(colWidth[7]) << getTeamForm(team.getName(), 3) << "\n";
        }
    }

    /**
     * @brief Выводит топ-3 команды турнира.
     */
    void printTop3() const {
        if (teams.empty()) {
            cout << "Таблица пуста!\n";
            return;
        }

        cout << "\nТоп-3 команды:\n";
        cout << string(60, '-') << "\n";
        cout << "Место | Команда            | Очки | Последние матчи\n";
        cout << string(60, '-') << "\n";

        int count = min(3, static_cast<int>(teams.size()));
        for (int i = 0; i < count; ++i) {
            cout << setw(5) << teams[i].getPosition() << " | "
                 << setw(18) << teams[i].getName() << " | "
                 << setw(4) << teams[i].getPoints() << " | "
                 << getTeamForm(teams[i].getName(), 5) << "\n";
        }
    }

    /**
     * @brief Ищет команду по названию и выводит информацию.
     */
    void findTeam(const string& name) const {
        auto it = find_if(teams.begin(), teams.end(),
            [&](const Team& t) { return t.getName() == name; });

        if (it == teams.end()) {
            cout << "Команда '" << name << "' не найдена.\n";
            return;
        }

        cout << "\nРезультаты поиска:\n";
        cout << "Команда: " << it->getName() << "\n"
             << "Место: " << it->getPosition() << "\n"
             << "Игры: " << it->getGames() << "\n"
             << "Победы: " << it->getWins() << "\n"
             << "Ничьи: " << it->getDraws() << "\n"
             << "Поражения: " << it->getLosses() << "\n"
             << "Очки: " << it->getPoints() << "\n"
             << "Форма: " << getTeamForm(name, 5) << "\n\n";
        
        printTeamMatches(name);
    }

    /**
     * @brief Выводит историю матчей команды.
     */
    void printTeamMatches(const string& name) const {
        cout << "Последние матчи:\n";
        int count = 0;
        for (auto it = matches.rbegin(); it != matches.rend() && count < 5; ++it) {
            if (it->getTeam1() == name || it->getTeam2() == name) {
                it->print();
                cout << "\n";
                count++;
            }
        }
        if (count == 0) {
            cout << "Матчи не найдены\n";
        }
    }

private:
    vector<Team> teams;
    vector<Match> matches;

    /**
     * @brief Сортирует команды и обновляет их позиции.
     */
    void sortTeams() {
        sort(teams.begin(), teams.end());
        
        if (!teams.empty()) {
            teams[0].setPosition(1);
            for (size_t i = 1; i < teams.size(); ++i) {
                if (teams[i].getPoints() == teams[i-1].getPoints() &&
                    teams[i].getWins() == teams[i-1].getWins() &&
                    teams[i].getLosses() == teams[i-1].getLosses()) {
                    teams[i].setPosition(teams[i-1].getPosition());
                } else {
                    teams[i].setPosition(i + 1);
                }
            }
        }
    }

    /**
     * @brief Возвращает форму команды (последние результаты).
     */
    string getTeamForm(const string& name, int count) const {
        string form;
        int found = 0;
        
        for (auto it = matches.rbegin(); it != matches.rend() && found < count; ++it) {
            if (it->getTeam1() == name) {
                form += (it->getResult() == 'V' ? 'W' : 'D');
                found++;
            } else if (it->getTeam2() == name) {
                form += (it->getResult() == 'V' ? 'L' : 'D');
                found++;
            }
        }
        
        return form.empty() ? "-" : form;
    }

    /**
     * @brief Ищет команду по названию.
     */
    vector<Team>::iterator findTeamIterator(const string& name) {
        return find_if(teams.begin(), teams.end(),
            [&](Team& t) { return t.getName() == name; });
    }

    /**
     * @brief Генерирует демо-команды.
     */
    void generateDemoTeams(int count) {
        for (int i = 1; i <= count; ++i) {
            ostringstream name;
            name << "Team_Demo_" << i;
            teams.emplace_back(name.str());
        }
    }
};

/**
 * @brief Отображает главное меню программы.
 */
void printMainMenu() {
    cout << "\n=== Турнирная таблица ===";
    cout << "\n1. Загрузить из файла";
    cout << "\n2. Сохранить в файл";
    cout << "\n3. Показать таблицу";
    cout << "\n4. Добавить команду";
    cout << "\n5. Удалить команду";
    cout << "\n6. Редактировать команду";
    cout << "\n7. Обновить результаты тура";
    cout << "\n8. Показать топ-3 команды";
    cout << "\n9. Найти команду";
    cout << "\n0. Выход";
    cout << "\nВыберите действие: ";
}

int main() {
    Tournament tournament;
    int choice;
    string filename, teamName, newName;

    setlocale(LC_ALL, "ru_RU.UTF-8");

    do {
        printMainMenu();
        cin >> choice;
        cin.ignore();

        try {
            switch (choice) {
                case 1:
                    cout << "Введите имя файла: ";
                    getline(cin, filename);
                    tournament.loadFromFile(filename);
                    break;
                    
                case 2:
                    cout << "Введите имя файла: ";
                    getline(cin, filename);
                    tournament.saveToFile(filename);
                    break;
                    
                case 3:
                    tournament.printTable();
                    break;
                    
                case 4:
                    cout << "Введите название команды: ";
                    getline(cin, teamName);
                    tournament.addTeam(teamName);
                    break;
                    
                case 5:
                    cout << "Введите название команды: ";
                    getline(cin, teamName);
                    tournament.removeTeam(teamName);
                    break;
                    
                case 6:
                    cout << "Введите текущее название команды: ";
                    getline(cin, teamName);
                    cout << "Введите новое название: ";
                    getline(cin, newName);
                    tournament.editTeam(teamName, newName);
                    break;
                    
                case 7:
                    tournament.updateRoundResults();
                    break;
                    
                case 8:
                    tournament.printTop3();
                    break;
                    
                case 9:
                    cout << "Введите название команды: ";
                    getline(cin, teamName);
                    tournament.findTeam(teamName);
                    break;
                    
                case 0:
                    cout << "Завершение программы...\n";
                    break;
                    
                default:
                    cout << "Неверный выбор!\n";
            }
        } catch (const exception& e) {
            cerr << "\nОшибка: " << e.what() << "\n";
        }
    } while (choice != 0);

    return 0;
}