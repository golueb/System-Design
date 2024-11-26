workspace {
    name "Система управления целями и задачами"
    description "Система для управления целями и задачами пользователей"

    !identifiers hierarchical

    model {
        user = person "Пользователь" {
            description "Пользователь системы"
        }

        admin = person "Администратор" {
            description "Администратор системы"
        }

        system = softwareSystem "Система управления целями и задачами" {
            description "Система для управления целями и задачами пользователей"

            webApp = container "Web-приложение" {
                description "Позволяет пользователям взаимодействовать с сервисом через браузер"
                technology "React, JavaScript"
            }

            apiGateway = container "API Gateway" {
                description "Обеспечивает доступ к бизнес-логике"
                technology "Node.js, Express"
            }

            coreService = container "Core Service" {
                description "Сервис управления пользователями, целями и задачами"
                technology "Java Spring Boot"
            }

            database = container "База данных" {
                description "Хранит информацию о пользователях, целях и задачах"
                technology "PostgreSQL"
            }

            // Взаимодействие пользователя с системой
            user -> webApp "Использует для взаимодействия"
            admin -> webApp "Использует для управления"
            webApp -> apiGateway "Запросы к API"
            apiGateway -> coreService "Запросы на управление" "HTTPS"
            coreService -> database "Чтение/Запись данных" "JDBC"

            // Основные сценарии использования
            user -> webApp "Создание нового пользователя"
            webApp -> apiGateway "POST /users"
            apiGateway -> coreService "POST /users"
            coreService -> database "INSERT INTO users"

            user -> webApp "Поиск пользователя по логину"
            webApp -> apiGateway "GET /users?login={login}"
            apiGateway -> coreService "GET /users?login={login}"
            coreService -> database "SELECT * FROM users WHERE login={login}"

            user -> webApp "Поиск пользователя по маске имени и фамилии"
            webApp -> apiGateway "GET /users?name={name}&surname={surname}"
            apiGateway -> coreService "GET /users?name={name}&surname={surname}"
            coreService -> database "SELECT * FROM users WHERE name LIKE {name} AND surname LIKE {surname}"

            user -> webApp "Создание новой цели"
            webApp -> apiGateway "POST /goals"
            apiGateway -> coreService "POST /goals"
            coreService -> database "INSERT INTO goals"

            user -> webApp "Получение списка всех целей"
            webApp -> apiGateway "GET /goals"
            apiGateway -> coreService "GET /goals"
            coreService -> database "SELECT * FROM goals"

            user -> webApp "Создание новой задачи на пути к цели"
            webApp -> apiGateway "POST /goals/{goalId}/tasks"
            apiGateway -> coreService "POST /goals/{goalId}/tasks"
            coreService -> database "INSERT INTO tasks"

            user -> webApp "Получение всех задач цели"
            webApp -> apiGateway "GET /goals/{goalId}/tasks"
            apiGateway -> coreService "GET /goals/{goalId}/tasks"
            coreService -> database "SELECT * FROM tasks WHERE goalId={goalId}"

            user -> webApp "Изменение статуса задачи в цели"
            webApp -> apiGateway "PUT /tasks/{taskId}"
            apiGateway -> coreService "PUT /tasks/{taskId}"
            coreService -> database "UPDATE tasks SET status = {status} WHERE taskId={taskId}"
        }
    }
    
    views {
        themes default

        systemContext system {
            include *
            autolayout lr
        }

        container system {
            include *
            autolayout lr
        }

        dynamic system "createUser" "Создание нового пользователя" {
            user -> system.webApp "Создаёт нового пользователя"
            system.webApp -> system.apiGateway "POST /users"
            system.apiGateway -> system.coreService "POST /users"
            system.coreService -> system.database "INSERT INTO users"
            autolayout lr
        }

        dynamic system "findUserByLogin" "Поиск пользователя по логину" {
            user -> system.webApp "Ищет пользователя по логину"
            system.webApp -> system.apiGateway "GET /users?login={login}"
            system.apiGateway -> system.coreService "GET /users?login={login}"
            system.coreService -> system.database "SELECT * FROM users WHERE login={login}"
            autolayout lr
        }

        dynamic system "findUserByName" "Поиск пользователя по маске имени и фамилии" {
            user -> system.webApp "Ищет пользователя по имени и фамилии"
            system.webApp -> system.apiGateway "GET /users?name={name}&surname={surname}"
            system.apiGateway -> system.coreService "GET /users?name={name}&surname={surname}"
            system.coreService -> system.database "SELECT * FROM users WHERE name LIKE {name} AND surname LIKE {surname}"
            autolayout lr
        }

        dynamic system "createGoal" "Создание новой цели" {
            user -> system.webApp "Создаёт новую цель"
            system.webApp -> system.apiGateway "POST /goals"
            system.apiGateway -> system.coreService "POST /goals"
            system.coreService -> system.database "INSERT INTO goals"
            autolayout lr
        }

        dynamic system "getGoals" "Получение списка всех целей" {
            user -> system.webApp "Запрашивает список целей"
            system.webApp -> system.apiGateway "GET /goals"
            system.apiGateway -> system.coreService "GET /goals"
            system.coreService -> system.database "SELECT * FROM goals"
            autolayout lr
        }

        dynamic system "createTask" "Создание новой задачи на пути к цели" {
            user -> system.webApp "Создаёт новую задачу"
            system.webApp -> system.apiGateway "POST /goals/{goalId}/tasks"
            system.apiGateway -> system.coreService "POST /goals/{goalId}/tasks"
            system.coreService -> system.database "INSERT INTO tasks"
            autolayout lr
        }

        dynamic system "getTasks" "Получение всех задач цели" {
            user -> system.webApp "Запрашивает задачи цели"
            system.webApp -> system.apiGateway "GET /goals/{goalId}/tasks"
            system.apiGateway -> system.coreService "GET /goals/{goalId}/tasks"
            system.coreService -> system.database "SELECT * FROM tasks WHERE goalId={goalId}"
            autolayout lr
        }

        dynamic system "updateTaskStatus" "Изменение статуса задачи в цели" {
            user -> system.webApp "Изменяет статус задачи"
            system.webApp -> system.apiGateway "PUT /tasks/{taskId}"
            system.apiGateway -> system.coreService "PUT /tasks/{taskId}"
            system.coreService -> system.database "UPDATE tasks SET status = {status} WHERE taskId={taskId}"
            autolayout lr
        }

        theme default
    }
}