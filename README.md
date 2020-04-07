# Test sample server

Testing over a single server that allow to just to add user and get users.

This server, does not persist user between different server executions. It's just a server to expose how to test it.  

## Server image

In order to build the server image execute the following command:
```bash
docker build -f Dockerfile -t test_sample_server:local .
```

In order to delete the server image execute the following command:
```bash
docker rmi test_sample_server:local
```


## Run the server

In order to run the server, after its image creation, execute the following command:
```bash
docker run --name test_sample_server -p 8080:8080 test_sample_server:local script/run
```
Note that the command that actually runs the server is **script/run**

To stop the server, execute the following command:
```bash
docker stop $(docker ps -a -f 'name=test_sample_server' -q --no-trunc)
```

To remove the server container, execute the following command:
```bash
docker rm -f $(docker ps -a -f 'name=test_sample_server' -q --no-trunc)
```

## Manually check if server API is working

After run the server:

Do a **GET** to http://127.0.0.1:8080/users you should receive the list of user.

Do a **POST** to http://127.0.0.1:8080/user/add with body:
```bash
{
    "username": "tester",
    "name": "Tester",
    "surname": "Guy",
    "email": "tester_guy@yopmail.com",
    "birthday": "01/11/2000",
    "address": "111 Some st"
}
```

You should get a **201 (Created)**. 

If you now try to list all users (GET mentioned before) you'll see the user in the list.


## Run server unit tests

In order to run the server, after its image creation, execute the following command:
```bash
docker run test_sample_server:local script/unit
```
Note that the command that actually runs the server is **script/unit**

The previous command will only show in the screen the unit test results. 
In order to get their results stored in ``test/result`` folder, add the volume when running the unit tests:
```bash
docker run -v $PWD:/test_sample_source test_sample_server:local script/unit
```


## Edit server or test code

To edit server or test code in your local machine and reflect it in the server container, 
add ``ti`` (terminal interactive) and the volume when attaching to the server container:

```bash
docker run --rm -ti -v $PWD:/test_sample_source test_sample_server:local /bin/bash
```


## Run server system tests

### Pre-condition:

You will need to have already built a ``test_runner`` image:
- Test runner source: https://github.com/fmihaich/test_sample_test_runner

Steps to build test runner image:

```bash
git clone https://github.com/fmihaich/test_sample_test_runner.git
cd test_sample_test_runner
docker build -f Dockerfile -t test_sample_test_runner:local .
```

### Steps to run the system tests:

You can simply run ``script/system`` :)

If you manually want to run or edit system tests, start the ``system_tests.yml`` docker-compose environment by running:

```bash
docker-compose -f system_tests.yml up &
```

After that, to run all defined system tests, execute:

```bash
docker-compose -f system_tests.yml exec test_sample_test_runner script/run
```

If you want to edit or add new system tests, then run the following command and work on your any editor locally:
```bash
docker-compose -f system_tests.yml exec test_sample_test_runner /bin/bash
```

After everything is done, down the docker-compose environment:

```bash
docker-compose -f system_tests.yml down -v
```
