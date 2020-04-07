Feature: Server APIs


    @API @GET_USERS @ADD_USER @SMOKE
    Scenario Outline: All stored users are returned when they were previously added
        Given I successfully add "<user_count>" users
        When I get all users
        Then All the recent added users are returned

        Examples:
            | user_count |
            | 1          |
            | 3          |


    @API @ADD_USER
    Scenario: Only one user per username is stored
        When I add "user_1" user
        Then I get "HTTP_CREATED" status code
        When I try to add other user which "username" is the same than "user_1" username
        Then I get "HTTP_SERVER_ERROR" status code
        When I get all users
        Then I see only "1" user with "user_1" "username"


    @API @ADD_USER
    Scenario: User without a mandatory attribute is not stored
        Given I try to add a user without specifying the "email"
        When I get all users
        Then The user is not returned


    @API @ADD_USER
    Scenario: User with incomplete data is not stored
        Given I try to add a user with incomplete data
        When I get all users
        Then The user is not returned
