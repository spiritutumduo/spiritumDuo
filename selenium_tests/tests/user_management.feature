Feature: User management
    Scenario: A new user needs to be created
        Given the user is logged in
        Given the user is on the user creation page
        Then the user fills the form in with valid data
        When the user submits the form
        Then the user should see the confirmation modal
    Scenario: A user needs to be updated
        Given the user is logged in
        Given the user is on the users list page
        When the user selects a user
        Then the user should see a modal to edit the user
        Then the user changes values in this form
        When the user submits the edit form
        Then the user is shown a confirmation modal