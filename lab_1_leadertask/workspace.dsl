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

            userService = container "User Service" {
                description "Сервис управления пользователями"
                technology "Java Spring Boot"
            }

            goalService = container "Goal Service" {
                description "Сервис управления целями"
                technology "Java Spring Boot"
            }

            taskService = container "Task Service" {
                description "Сервис управления задачами"
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
            apiGateway -> userService "Запросы на управление пользователями" "HTTPS"
            apiGateway -> goalService "Запросы на управление целями" "HTTPS"
            apiGateway -> taskService "Запросы на управление задачами" "HTTPS"
            userService -> database "Чтение/Запись данных" "JDBC"
            goalService -> database "Чтение/Запись данных" "JDBC"
            taskService -> database "Чтение/Запись данных" "JDBC"

            // Основные сценарии использования
            user -> webApp "Создание нового пользователя"
            webApp -> apiGateway "POST /users"
            apiGateway -> userService "POST /users"
            userService -> database "INSERT INTO users"

            user -> webApp "Поиск пользователя по логину"
            webApp -> apiGateway "GET /users?login={login}"
            apiGateway -> userService "GET /users?login={login}"
            userService -> database "SELECT * FROM users WHERE login={login}"

            user -> webApp "Поиск пользователя по маске имени и фамилии"
            webApp -> apiGateway "GET /users?name={name}&surname={surname}"
            apiGateway -> userService "GET /users?name={name}&surname={surname}"
            userService -> database "SELECT * FROM users WHERE name LIKE {name} AND surname LIKE {surname}"

            user -> webApp "Создание новой цели"
            webApp -> apiGateway "POST /goals"
            apiGateway -> goalService "POST /goals"
            goalService -> database "INSERT INTO goals"

            user -> webApp "Получение списка всех целей"
            webApp -> apiGateway "GET /goals"
            apiGateway -> goalService "GET /goals"
            goalService -> database "SELECT * FROM goals"

            user -> webApp "Создание новой задачи на пути к цели"
            webApp -> apiGateway "POST /goals/{goalId}/tasks"
            apiGateway -> taskService "POST /goals/{goalId}/tasks"
            taskService -> database "INSERT INTO tasks"

            user -> webApp "Получение всех задач цели"
            webApp -> apiGateway "GET /goals/{goalId}/tasks"
            apiGateway -> taskService "GET /goals/{goalId}/tasks"
            taskService -> database "SELECT * FROM tasks WHERE goalId={goalId}"

            user -> webApp "Изменение статуса задачи в цели"
            webApp -> apiGateway "PUT /tasks/{taskId}"
            apiGateway -> taskService "PUT /tasks/{taskId}"
            taskService -> database "UPDATE tasks SET status = {status} WHERE taskId={taskId}"
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
            system.apiGateway -> system.userService "POST /users"
            system.userService -> system.database "INSERT INTO users"
            autolayout lr
        }

        dynamic system "findUserByLogin" "Поиск пользователя по логину" {
            user -> system.webApp "Ищет пользователя по логину"
            system.webApp -> system.apiGateway "GET /users?login={login}"
            system.apiGateway -> system.userService "GET /users?login={login}"
            system.userService -> system.database "SELECT * FROM users WHERE login={login}"
            autolayout lr
        }

        dynamic system "findUserByName" "Поиск пользователя по маске имени и фамилии" {
            user -> system.webApp "Ищет пользователя по имени и фамилии"
            system.webApp -> system.apiGateway "GET /users?name={name}&surname={surname}"
            system.apiGateway -> system.userService "GET /users?name={name}&surname={surname}"
            system.userService -> system.database "SELECT * FROM users WHERE name LIKE {name} AND surname LIKE {surname}"
            autolayout lr
        }

        dynamic system "createGoal" "Создание новой цели" {
            user -> system.webApp "Создаёт новую цель"
            system.webApp -> system.apiGateway "POST /goals"
            system.apiGateway -> system.goalService "POST /goals"
            system.goalService -> system.database "INSERT INTO goals"
            autolayout lr
        }

        dynamic system "getGoals" "Получение списка всех целей" {
            user -> system.webApp "Запрашивает список целей"
            system.webApp -> system.apiGateway "GET /goals"
            system.apiGateway -> system.goalService "GET /goals"
            system.goalService -> system.database "SELECT * FROM goals"
            autolayout lr
        }

        dynamic system "createTask" "Создание новой задачи на пути к цели" {
            user -> system.webApp "Создаёт новую задачу"
            system.webApp -> system.apiGateway "POST /goals/{goalId}/tasks"
            system.apiGateway -> system.taskService "POST /goals/{goalId}/tasks"
            system.taskService -> system.database "INSERT INTO tasks"
            autolayout lr
        }

        dynamic system "getTasks" "Получение всех задач цели" {
            user -> system.webApp "Запрашивает задачи цели"
            system.webApp -> system.apiGateway "GET /goals/{goalId}/tasks"
            system.apiGateway -> system.taskService "GET /goals/{goalId}/tasks"
            system.taskService -> system.database "SELECT * FROM tasks WHERE goalId={goalId}"
            autolayout lr
        }

        dynamic system "updateTaskStatus" "Изменение статуса задачи в цели" {
            user -> system.webApp "Изменяет статус задачи"
            system.webApp -> system.apiGateway "PUT /tasks/{taskId}"
            system.apiGateway -> system.taskService "PUT /tasks/{taskId}"
            system.taskService -> system.database "UPDATE tasks SET status = {status} WHERE taskId={taskId}"
            autolayout lr
        }

        theme default
    }
}
